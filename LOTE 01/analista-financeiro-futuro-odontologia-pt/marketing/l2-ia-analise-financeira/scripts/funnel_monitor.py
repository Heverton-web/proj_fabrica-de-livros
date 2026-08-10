#!/usr/bin/env python3
"""
Funnel Monitor — Daemon de métricas do funil de vendas.
Coleta estatísticas do banco a cada N segundos e exporta
para stdout/JSON, com suporte a alertas via webhook.
"""

import json
import sqlite3
import time
import logging
import signal
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
DB_PATH = BASE_DIR / "database" / "leads.db"
METRICS_PATH = BASE_DIR / "database" / "metrics.json"

LOG_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FMT)
log = logging.getLogger("funnel_monitor")

RUNNING = True


def signal_handler(sig, frame):
    global RUNNING
    log.info("Sinal de parada recebido, finalizando...")
    RUNNING = False


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------------------
# Coletor de Métricas
# ---------------------------------------------------------------------------
class MetricsCollector:
    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def coletar(self) -> dict:
        """Coleta todas as métricas do funil."""
        now = datetime.utcnow()
        hoje = now.strftime("%Y-%m-%d")
        semana_atras = (now - timedelta(days=7)).isoformat()
        mes_atras = (now - timedelta(days=30)).isoformat()

        metrics = {
            "timestamp": now.isoformat(),
            "periodo": {
                "hoje": hoje,
                "semana": semana_atras,
                "mes": mes_atras,
            },
        }

        # --- Leads ---
        try:
            total_leads = self.db.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
            leads_novos_hoje = self.db.execute(
                "SELECT COUNT(*) FROM leads WHERE captured_at >= ?", (hoje,)
            ).fetchone()[0]
            leads_novos_semana = self.db.execute(
                "SELECT COUNT(*) FROM leads WHERE captured_at >= ?", (semana_atras,)
            ).fetchone()[0]
            leads_novos_mes = self.db.execute(
                "SELECT COUNT(*) FROM leads WHERE captured_at >= ?", (mes_atras,)
            ).fetchone()[0]

            metrics["leads"] = {
                "total": total_leads,
                "novos_hoje": leads_novos_hoje,
                "novos_semana": leads_novos_semana,
                "novos_mes": leads_novos_mes,
            }

            # Por estágio
            stages = self.db.execute(
                "SELECT stage, COUNT(*) as cnt FROM leads GROUP BY stage"
            ).fetchall()
            metrics["leads"]["por_estagio"] = {r["stage"]: r["cnt"] for r in stages}

            # Por persona
            personas = self.db.execute(
                "SELECT persona_match, COUNT(*) as cnt FROM leads WHERE persona_match IS NOT NULL GROUP BY persona_match"
            ).fetchall()
            metrics["leads"]["por_persona"] = {r["persona_match"]: r["cnt"] for r in personas}

            # Score médio
            avg_score = self.db.execute(
                "SELECT AVG(score) FROM leads WHERE score > 0"
            ).fetchone()[0]
            metrics["leads"]["score_medio"] = round(avg_score or 0, 2)
        except sqlite3.OperationalError as e:
            log.warning(f"Erro ao consultar leads: {e}")
            metrics["leads"] = {"erro": str(e)}

        # --- E-mail Sequences ---
        try:
            total_seq = self.db.execute("SELECT COUNT(*) FROM email_sequence").fetchone()[0]
            seq_ativas = self.db.execute(
                "SELECT COUNT(*) FROM email_sequence WHERE status = 'ativo'"
            ).fetchone()[0]
            seq_concluidas = self.db.execute(
                "SELECT COUNT(*) FROM email_sequence WHERE status = 'concluido'"
            ).fetchone()[0]

            metrics["email"] = {
                "total_sequencias": total_seq,
                "ativas": seq_ativas,
                "concluidas": seq_concluidas,
            }

            # Por funil
            por_funil = self.db.execute(
                "SELECT funnel, status, COUNT(*) as cnt FROM email_sequence GROUP BY funnel, status"
            ).fetchall()
            funil_metrics: dict = {}
            for r in por_funil:
                if r["funnel"] not in funil_metrics:
                    funil_metrics[r["funnel"]] = {}
                funil_metrics[r["funnel"]][r["status"]] = r["cnt"]
            metrics["email"]["por_funil"] = funil_metrics
        except sqlite3.OperationalError:
            metrics["email"] = {"total_sequencias": 0, "ativas": 0, "concluidas": 0}

        # --- Interações ---
        try:
            total_interactions = self.db.execute(
                "SELECT COUNT(*) FROM lead_interactions"
            ).fetchone()[0]
            interactions_hoje = self.db.execute(
                "SELECT COUNT(*) FROM lead_interactions WHERE created_at >= ?", (hoje,)
            ).fetchone()[0]

            por_canal = self.db.execute(
                "SELECT channel, COUNT(*) as cnt FROM lead_interactions GROUP BY channel"
            ).fetchall()

            metrics["interacoes"] = {
                "total": total_interactions,
                "hoje": interactions_hoje,
                "por_canal": {r["channel"]: r["cnt"] for r in por_canal},
            }
        except sqlite3.OperationalError:
            metrics["interacoes"] = {"total": 0, "hoje": 0, "por_canal": {}}

        # --- Conversões (calculadas) ---
        try:
            if total_leads > 0:
                taxa_novo_para_contatado = round(
                    self.db.execute("SELECT COUNT(*) FROM leads WHERE contacted = 1").fetchone()[0]
                    / total_leads * 100, 2
                )
                taxa_conversao = round(
                    self.db.execute("SELECT COUNT(*) FROM leads WHERE stage = 'convertido'").fetchone()[0]
                    / total_leads * 100, 2
                )
            else:
                taxa_novo_para_contatado = 0
                taxa_conversao = 0

            metrics["conversao"] = {
                "taxa_novo_para_contatado": taxa_novo_para_contatado,
                "taxa_conversao_geral": taxa_conversao,
            }
        except sqlite3.OperationalError:
            metrics["conversao"] = {"taxa_novo_para_contatado": 0, "taxa_conversao_geral": 0}

        return metrics


# ---------------------------------------------------------------------------
# Alertas
# ---------------------------------------------------------------------------
class AlertManager:
    def __init__(self, webhook_url: str = "", thresholds: dict | None = None):
        self.webhook_url = webhook_url
        self.thresholds = thresholds or {}

    def verificar(self, metrics: dict):
        """Verifica condições de alerta."""
        alerts = []

        # Leads caindo
        leads_semana = metrics.get("leads", {}).get("novos_semana", 0)
        min_leads = self.thresholds.get("min_leads_semana", 10)
        if leads_semana < min_leads:
            alerts.append({
                "tipo": "leads_baixos",
                "mensagem": f"Apenas {leads_semana} leads novos esta semana (mínimo: {min_leads})",
                "severidade": "warning",
            })

        # Conversão caindo
        taxa = metrics.get("conversao", {}).get("taxa_conversao_geral", 0)
        min_taxa = self.thresholds.get("min_taxa_conversao", 1.0)
        if taxa < min_taxa and metrics.get("leads", {}).get("total", 0) > 50:
            alerts.append({
                "tipo": "conversao_baixa",
                "mensagem": f"Taxa de conversão em {taxa}% (mínimo: {min_taxa}%)",
                "severidade": "critical",
            })

        # Enviar alertas
        for alert in alerts:
            log.warning(f"ALERTA [{alert['severidade']}]: {alert['mensagem']}")
            if self.webhook_url:
                self._enviar_webhook(alert)

    def _enviar_webhook(self, alert: dict):
        try:
            requests.post(self.webhook_url, json={
                "text": f"🚨 [{alert['severidade'].upper()}] {alert['mensagem']}",
                "alert": alert,
            }, timeout=10)
        except requests.RequestException as e:
            log.error(f"Falha ao enviar webhook: {e}")


# ---------------------------------------------------------------------------
# Exportadores
# ---------------------------------------------------------------------------
def exportar_json(metrics: dict, path: Path):
    """Salva métricas em JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)

    # Manter histórico (últimas 100 entradas)
    history = []
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            history = data.get("history", [])
        except (json.JSONDecodeError, KeyError):
            history = []

    history.append(metrics)
    history = history[-100:]

    output = {
        "current": metrics,
        "history": history,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


def imprimir_resumo(metrics: dict):
    """Imprime resumo legível no terminal."""
    leads = metrics.get("leads", {})
    email = metrics.get("email", {})
    conv = metrics.get("conversao", {})

    print(f"\n{'='*60}")
    print(f"  FUNNEL MONITOR — {metrics['timestamp'][:19]}")
    print(f"{'='*60}")
    print(f"\n  LEADS:")
    print(f"    Total:          {leads.get('total', 0)}")
    print(f"    Novos hoje:     {leads.get('novos_hoje', 0)}")
    print(f"    Novos semana:   {leads.get('novos_semana', 0)}")
    print(f"    Novos mês:      {leads.get('novos_mes', 0)}")
    print(f"    Score médio:    {leads.get('score_medio', 0)}")

    if leads.get("por_estagio"):
        print(f"\n    Por estágio:")
        for stage, cnt in leads["por_estagio"].items():
            print(f"      {stage:20s} → {cnt}")

    print(f"\n  E-MAIL:")
    print(f"    Sequências:     {email.get('total_sequencias', 0)}")
    print(f"    Ativas:         {email.get('ativas', 0)}")
    print(f"    Concluídas:     {email.get('concluidas', 0)}")

    print(f"\n  CONVERSÃO:")
    print(f"    Lead→Contato:   {conv.get('taxa_novo_para_contatado', 0)}%")
    print(f"    Conversão:      {conv.get('taxa_conversao_geral', 0)}%")
    print(f"{'='*60}\n")


# ---------------------------------------------------------------------------
# Daemon Loop
# ---------------------------------------------------------------------------
def executar_daemon(intervalo: int = 60):
    """Loop principal do daemon."""
    db = get_db()
    collector = MetricsCollector(db)

    alert_config = load_json(CONFIG_DIR / "funis.json")
    webhook_url = alert_config.get("webhook_alertas", "")
    thresholds = alert_config.get("thresholds", {})
    alert_manager = AlertManager(webhook_url, thresholds)

    log.info(f"Funnel Monitor iniciado (intervalo: {intervalo}s)")

    while RUNNING:
        try:
            metrics = collector.coletar()
            imprimir_resumo(metrics)
            exportar_json(metrics, METRICS_PATH)
            alert_manager.verificar(metrics)
        except Exception as e:
            log.error(f"Erro na coleta: {e}")

        # Aguardar com check de parada
        for _ in range(intervalo):
            if not RUNNING:
                break
            time.sleep(1)

    log.info("Funnel Monitor finalizado")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Funnel Monitor — Métricas")
    parser.add_argument("--intervalo", type=int, default=60, help="Intervalo em segundos")
    parser.add_argument("--once", action="store_true", help="Executa uma vez e sai")
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    args = parser.parse_args()

    if args.once:
        db = get_db()
        collector = MetricsCollector(db)
        metrics = collector.coletar()
        if args.json:
            print(json.dumps(metrics, indent=2, ensure_ascii=False))
        else:
            imprimir_resumo(metrics)
        exportar_json(metrics, METRICS_PATH)
    else:
        executar_daemon(args.intervalo)


if __name__ == "__main__":
    main()
