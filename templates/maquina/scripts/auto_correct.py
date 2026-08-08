#!/usr/bin/env python3
"""
Auto-Correct — Correção automática de testes A/B.
Monitora métricas de variantes e ajusta tráfego/alocação
quando uma variante supera a outra com significância estatística.
"""

import json
import sqlite3
import math
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
DB_PATH = BASE_DIR / "database" / "leads.db"
EXPERIMENTS_PATH = BASE_DIR / "database" / "experiments.json"

LOG_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FMT)
log = logging.getLogger("auto_correct")

SIGNIFICANCE_LEVEL = 0.05  # 95% confiança
MIN_SAMPLE_SIZE = 30


# ---------------------------------------------------------------------------
# Teste de Significância Estatística
# ---------------------------------------------------------------------------
def z_score(p1: float, p2: float, n1: int, n2: int) -> float:
    """Calcula z-score para diferença entre duas proporções."""
    if n1 == 0 or n2 == 0:
        return 0.0
    p_pool = (p1 * n1 + p2 * n2) / (n1 + n2)
    if p_pool == 0 or p_pool == 1:
        return 0.0
    se = math.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    if se == 0:
        return 0.0
    return (p1 - p2) / se


def p_value_from_z(z: float) -> float:
    """Aproximação do p-value a partir do z-score (two-tailed)."""
    # Aproximação usando a função de erro
    return 2 * (1 - _norm_cdf(abs(z)))


def _norm_cdf(x: float) -> float:
    """CDF da distribuição normal padrão (aproximação de Abramowitz e Stegun)."""
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    sign = 1 if x >= 0 else -1
    x = abs(x) / math.sqrt(2)
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return 0.5 * (1.0 + sign * y)


def teste_significativo(conversao_a: int, total_a: int, conversao_b: int, total_b: int) -> dict:
    """Verifica se há diferença significativa entre A e B."""
    if total_a < MIN_SAMPLE_SIZE or total_b < MIN_SAMPLE_SIZE:
        return {
            "significativo": False,
            "motivo": f"Amostra insuficiente (min={MIN_SAMPLE_SIZE})",
            "amostra_a": total_a,
            "amostra_b": total_b,
        }

    p_a = conversao_a / total_a if total_a > 0 else 0
    p_b = conversao_b / total_b if total_b > 0 else 0

    z = z_score(p_a, p_b, total_a, total_b)
    p_val = p_value_from_z(z)

    vencedor = None
    if p_val < SIGNIFICANCE_LEVEL:
        vencedor = "A" if p_a > p_b else "B"

    lift = ((max(p_a, p_b) / min(p_a, p_b)) - 1) * 100 if min(p_a, p_b) > 0 else 0

    return {
        "significativo": p_val < SIGNIFICANCE_LEVEL,
        "p_value": round(p_val, 6),
        "z_score": round(z, 4),
        "conversao_a": round(p_a * 100, 2),
        "conversao_b": round(p_b * 100, 2),
        "lift": round(lift, 2),
        "vencedor": vencedor,
        "amostra_a": total_a,
        "amostra_b": total_b,
    }


# ---------------------------------------------------------------------------
# Gerenciador de Experimentos
# ---------------------------------------------------------------------------
class ExperimentManager:
    def __init__(self, db: sqlite3.Connection):
        self.db = db
        self._ensure_tables()

    def _ensure_tables(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS experiments (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                slug        TEXT UNIQUE NOT NULL,
                nome        TEXT NOT NULL,
                tipo        TEXT DEFAULT 'email_subject',
                variante_a  TEXT NOT NULL,
                variante_b  TEXT NOT NULL,
                metrica     TEXT DEFAULT 'conversao',
                status      TEXT DEFAULT 'ativo',
                trafego_a   REAL DEFAULT 50.0,
                trafego_b   REAL DEFAULT 50.0,
                created_at  TEXT DEFAULT (datetime('now')),
                updated_at  TEXT DEFAULT (datetime('now'))
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS experiment_results (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_id   INTEGER NOT NULL,
                variante        TEXT NOT NULL,
                impressoes      INTEGER DEFAULT 0,
                cliques         INTEGER DEFAULT 0,
                conversoes      INTEGER DEFAULT 0,
                receita         REAL DEFAULT 0.0,
                updated_at      TEXT DEFAULT (datetime('now')),
                UNIQUE(experiment_id, variante),
                FOREIGN KEY (experiment_id) REFERENCES experiments(id)
            )
        """)
        self.db.commit()

    def criar_experimento(self, slug: str, nome: str, tipo: str, variante_a: str, variante_b: str, metrica: str = "conversao"):
        try:
            self.db.execute("""
                INSERT INTO experiments (slug, nome, tipo, variante_a, variante_b, metrica)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (slug, nome, tipo, variante_a, variante_b, metrica))
            exp_id = self.db.execute("SELECT last_insert_rowid()").fetchone()[0]
            for v in ["A", "B"]:
                self.db.execute("""
                    INSERT INTO experiment_results (experiment_id, variante)
                    VALUES (?, ?)
                """, (exp_id, v))
            self.db.commit()
            log.info(f"Experimento '{slug}' criado")
            return exp_id
        except sqlite3.IntegrityError:
            log.warning(f"Experimento '{slug}' já existe")
            return None

    def registrar_evento(self, experiment_slug: str, variante: str, tipo: str, valor: float = 0):
        """Registra um evento (impressão, clique, conversão)."""
        exp = self.db.execute(
            "SELECT id FROM experiments WHERE slug = ?", (experiment_slug,)
        ).fetchone()
        if not exp:
            log.error(f"Experimento '{experiment_slug}' não encontrado")
            return

        col_map = {
            "impressao": "impressoes",
            "clique": "cliques",
            "conversao": "conversoes",
        }
        col = col_map.get(tipo)
        if not col:
            log.error(f"Tipo de evento desconhecido: {tipo}")
            return

        self.db.execute(f"""
            UPDATE experiment_results
            SET {col} = {col} + 1, receita = receita + ?, updated_at = datetime('now')
            WHERE experiment_id = ? AND variante = ?
        """, (valor, exp["id"], variante.upper()))
        self.db.commit()

    def listar_experimentos(self) -> list[dict]:
        rows = self.db.execute("""
            SELECT e.*, er_a.impressoes as imp_a, er_a.cliques as cliques_a, er_a.conversoes as conv_a, er_a.receita as rec_a,
                   er_b.impressoes as imp_b, er_b.cliques as cliques_b, er_b.conversoes as conv_b, er_b.receita as rec_b
            FROM experiments e
            LEFT JOIN experiment_results er_a ON er_a.experiment_id = e.id AND er_a.variante = 'A'
            LEFT JOIN experiment_results er_b ON er_b.experiment_id = e.id AND er_b.variante = 'B'
            WHERE e.status = 'ativo'
        """).fetchall()
        return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Auto-Correct Engine
# ---------------------------------------------------------------------------
class AutoCorrectEngine:
    def __init__(self, db: sqlite3.Connection):
        self.db = db
        self.manager = ExperimentManager(db)

    def analisar_e_corrigir(self) -> list[dict]:
        """Analisa todos os experimentos ativos e ajusta tráfego."""
        experimentos = self.manager.listar_experimentos()
        correcoes = []

        for exp in experimentos:
            resultado = self._analisar_experimento(exp)
            if resultado.get("corrigido"):
                correcoes.append(resultado)

        return correcoes

    def _analisar_experimento(self, exp: dict) -> dict:
        """Analisa um experimento e decide se corrige."""
        resultado = {
            "experimento": exp["slug"],
            "nome": exp["nome"],
            "corrigido": False,
        }

        metrica = exp.get("metrica", "conversao")
        if metrica == "conversao":
            conv_a = exp.get("conv_a", 0)
            total_a = exp.get("imp_a", 0) or exp.get("cliques_a", 0) or 1
            conv_b = exp.get("conv_b", 0)
            total_b = exp.get("imp_b", 0) or exp.get("cliques_b", 0) or 1
        elif metrica == "clique":
            conv_a = exp.get("cliques_a", 0)
            total_a = exp.get("imp_a", 1) or 1
            conv_b = exp.get("cliques_b", 0)
            total_b = exp.get("imp_b", 1) or 1
        else:
            resultado["motivo"] = f"Métrica desconhecida: {metrica}"
            return resultado

        teste = teste_significativo(conv_a, total_a, conv_b, total_b)
        resultado["teste"] = teste

        if teste["significativo"] and teste.get("vencedor"):
            vencedor = teste["vencedor"]
            lift = teste.get("lift", 0)

            if lift >= 20:
                # Vitória clara: 100% para vencedor
                novo_a = 100.0 if vencedor == "A" else 0.0
                novo_b = 100.0 - novo_a
                acao = "promovido"
            elif lift >= 10:
                # Vitória moderada: 80/20
                novo_a = 80.0 if vencedor == "A" else 20.0
                novo_b = 100.0 - novo_a
                acao = "ajustado"
            else:
                # Vitória marginal: 70/30
                novo_a = 70.0 if vencedor == "A" else 30.0
                novo_b = 100.0 - novo_a
                acao = "ajustado_leve"

            self.db.execute("""
                UPDATE experiments
                SET trafego_a = ?, trafego_b = ?, updated_at = datetime('now')
                WHERE id = ?
            """, (novo_a, novo_b, exp["id"]))
            self.db.commit()

            resultado.update({
                "corrigido": True,
                "acao": acao,
                "vencedor": vencedor,
                "trafego_anterior": {"A": exp.get("trafego_a", 50), "B": exp.get("trafego_b", 50)},
                "trafego_novo": {"A": novo_a, "B": novo_b},
                "lift": lift,
            })

            log.info(
                f"Experimento '{exp['slug']}': variante {vencedor} venceu "
                f"(lift={lift:.1f}%, p={teste['p_value']:.4f}) → "
                f"tráfego A={novo_a}% B={novo_b}%"
            )
        else:
            resultado["motivo"] = teste.get("motivo", "Sem significância estatística")

        return resultado


# ---------------------------------------------------------------------------
# Funil Auto-Correct (correções de funil além de A/B)
# ---------------------------------------------------------------------------
class FunnelAutoCorrect:
    """Correções automáticas baseadas em métricas do funil."""

    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def corrigir_leads_frios(self, dias_inativo: int = 7):
        """Move leads inativos para estágio 'frio'."""
        cutoff = (datetime.utcnow() - timedelta(days=dias_inativo)).isoformat()
        cursor = self.db.execute("""
            UPDATE leads
            SET stage = 'frio', updated_at = datetime('now')
            WHERE stage IN ('novo', 'contatado')
              AND contacted = 0
              AND captured_at < ?
        """, (cutoff,))
        self.db.commit()
        count = cursor.rowcount
        if count > 0:
            log.info(f"{count} leads marcados como 'frio' (inativos >{dias_inativo} dias)")
        return count

    def reativar_leads_frios(self, max_reativacoes: int = 50):
        """Seleciona leads frios para reativação."""
        leads = self.db.execute("""
            SELECT id, email, username, persona_match
            FROM leads
            WHERE stage = 'frio'
              AND email IS NOT NULL
            ORDER BY score DESC
            LIMIT ?
        """, (max_reativacoes,)).fetchall()

        count = 0
        for lead in leads:
            self.db.execute("""
                INSERT OR IGNORE INTO email_sequence (lead_id, funnel, step, next_send)
                VALUES (?, 'reativacao', 0, datetime('now'))
            """, (lead["id"],))
            self.db.execute(
                "UPDATE leads SET stage = 'reativacao', updated_at = datetime('now') WHERE id = ?",
                (lead["id"],)
            )
            count += 1

        self.db.commit()
        if count > 0:
            log.info(f"{count} leads frios enviados para reativação")
        return count


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Auto-Correct — Testes A/B e Funil")
    sub = parser.add_subparsers(dest="comando")

    # Analisar experimentos
    analisar = sub.add_parser("analisar", help="Analisa experimentos e corrige")
    analisar.add_argument("--dry-run", action="store_true")

    # Criar experimento
    criar = sub.add_parser("criar", help="Cria novo experimento")
    criar.add_argument("--slug", required=True)
    criar.add_argument("--nome", required=True)
    criar.add_argument("--tipo", default="email_subject")
    criar.add_argument("--variante-a", required=True)
    criar.add_argument("--variante-b", required=True)
    criar.add_argument("--metrica", default="conversao")

    # Registrar evento
    evento = sub.add_parser("evento", help="Registra evento em experimento")
    evento.add_argument("--experimento", required=True)
    evento.add_argument("--variante", required=True, choices=["A", "B"])
    evento.add_argument("--tipo", required=True, choices=["impressao", "clique", "conversao"])
    evento.add_argument("--valor", type=float, default=0)

    # Corrigir funil
    funil = sub.add_parser("funil", help="Correções automáticas do funil")
    funil.add_argument("--frios", action="store_true", help="Marcar leads inativos como frios")
    funil.add_argument("--reativar", action="store_true", help="Reativar leads frios")
    funil.add_argument("--dias", type=int, default=7)
    funil.add_argument("--max", type=int, default=50)

    # Listar
    sub.add_parser("listar", help="Lista experimentos ativos")

    args = parser.parse_args()

    if not args.comando:
        parser.print_help()
        return

    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row

    if args.comando == "analisar":
        engine = AutoCorrectEngine(db)
        correcoes = engine.analisar_e_corrigir()
        if args.dry_run:
            print(json.dumps(correcoes, indent=2, ensure_ascii=False))
        else:
            for c in correcoes:
                if c.get("corrigido"):
                    log.info(f"Corrigido: {c['experimento']} → {c['acao']}")
            log.info(f"Total: {len(correcoes)} correções aplicadas")

    elif args.comando == "criar":
        manager = ExperimentManager(db)
        manager.criar_experimento(args.slug, args.nome, args.tipo, args.variante_a, args.variante_b, args.metrica)

    elif args.comando == "evento":
        manager = ExperimentManager(db)
        manager.registrar_evento(args.experimento, args.variante, args.tipo, args.valor)

    elif args.comando == "funil":
        corrector = FunnelAutoCorrect(db)
        if args.frios:
            corrector.corrigir_leads_frios(args.dias)
        if args.reativar:
            corrector.reativar_leads_frios(args.max)

    elif args.comando == "listar":
        manager = ExperimentManager(db)
        exps = manager.listar_experimentos()
        for e in exps:
            print(f"  {e['slug']:20s} | {e['nome']:30s} | A={e.get('trafego_a',50):.0f}% B={e.get('trafego_b',50):.0f}%")


if __name__ == "__main__":
    main()
