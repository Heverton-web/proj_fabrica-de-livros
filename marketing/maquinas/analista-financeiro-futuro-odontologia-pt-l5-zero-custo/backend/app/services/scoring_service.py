from datetime import datetime, timezone

from app.config import settings
from app.database.connection import get_db
from app.models.lead import Lead


def calcular_score(lead: Lead) -> int:
    """Calcula score 0-100 baseado nas interações do lead."""
    db = get_db()
    rows = db.execute(
        "SELECT tipo, COUNT(*) as cnt FROM interacoes WHERE lead_id = ? GROUP BY tipo",
        [lead.id or 0],
    ).fetchall()

    score = 0.0
    pesos = {
        "email_aberto": settings.SCORING_PESO_ABERTURA,
        "email_clicado": settings.SCORING_PESO_CLIQUE,
        "resposta": settings.SCORING_PESO_RESPOSTA,
        "visita_site": settings.SCORING_PESO_VISITA,
        "download": settings.SCORING_PESO_download,
    }

    for row in rows:
        tipo = row["cnt"]
        peso = pesos.get(row["tipo"], 5.0)
        score += peso * tipo

    if lead.fonte == "referral":
        score += 10
    if lead.empresa:
        score += 5

    return min(100, max(0, int(score)))


def registrar_interacao_e_recalcular(lead_id: int, tipo: str, descricao: str = ""):
    """Registra uma interação e recalcula o score do lead."""
    db = get_db()
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "INSERT INTO interacoes (lead_id, tipo, descricao, created_at) VALUES (?, ?, ?, ?)",
        [lead_id, tipo, descricao, now],
    )
    db.commit()

    lead = Lead(id=lead_id)
    novo_score = calcular_score(lead)
    db.execute(
        "UPDATE leads SET score = ?, updated_at = ? WHERE id = ?",
        [novo_score, now, lead_id],
    )
    db.commit()
