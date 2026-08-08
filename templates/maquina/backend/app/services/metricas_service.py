from datetime import datetime, timezone, timedelta

from app.database.connection import get_db


class MetricasService:
    def taxas_conversao(self) -> dict:
        db = get_db()
        etapas = ["novo", "qualificado", "proposta", "negociacao", "ganho", "perdido"]
        contagens = {}
        for etapa in etapas:
            row = db.execute(
                "SELECT COUNT(*) as cnt FROM leads WHERE etapa_funil = ?", [etapa]
            ).fetchone()
            contagens[etapa] = row["cnt"]

        total = sum(contagens.values())
        ganhos = contagens.get("ganho", 0)
        taxa_fechamento = (ganhos / total * 100) if total > 0 else 0

        return {
            "contagens": contagens,
            "total_leads": total,
            "taxa_fechamento": round(taxa_fechamento, 1),
        }

    def dashboard_geral(self) -> dict:
        db = get_db()

        # Leads novos últimos 7 dias
        semana_atras = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        row = db.execute(
            "SELECT COUNT(*) as cnt FROM leads WHERE created_at >= ?", [semana_atras]
        ).fetchone()
        leads_semana = row["cnt"]

        # Vendas ganhas e receita total
        row = db.execute(
            "SELECT COUNT(*) as cnt, COALESCE(SUM(valor), 0) as total FROM vendas WHERE status = 'aceita'"
        ).fetchone()
        vendas_ganhas = row["cnt"]
        receita_total = row["total"]

        # Top 5 leads por score
        rows = db.execute(
            "SELECT id, nome, email, score, etapa_funil FROM leads ORDER BY score DESC LIMIT 5"
        ).fetchall()
        top_leads = [dict(r) for r in rows]

        # Interações últimos 7 dias
        row = db.execute(
            "SELECT COUNT(*) as cnt FROM interacoes WHERE created_at >= ?", [semana_atras]
        ).fetchone()
        interacoes_semana = row["cnt"]

        return {
            "leads_novos_semana": leads_semana,
            "vendas_ganhas": vendas_ganhas,
            "receita_total": receita_total,
            "interacoes_semana": interacoes_semana,
            "top_leads": top_leads,
        }

    def registrar_metrica_diaria(self):
        """Snapshot diário para gráficos de tendência."""
        db = get_db()
        hoje = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        conv = self.taxas_conversao()
        db.execute(
            """INSERT OR REPLACE INTO metricas_diarias
               (data, total_leads, leads_novos, leads_qualificados, leads_ganhos, receita_dia)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [hoje, conv["total_leads"], conv["contagens"].get("novo", 0),
             conv["contagens"].get("qualificado", 0), conv["contagens"].get("ganho", 0), 0],
        )
        db.commit()
