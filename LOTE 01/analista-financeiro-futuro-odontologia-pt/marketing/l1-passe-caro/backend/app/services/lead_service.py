from datetime import datetime, timezone
from typing import Optional, List

from app.database.connection import get_db
from app.models.lead import Lead


class LeadService:
    def listar(
        self,
        etapa: Optional[str] = None,
        fonte: Optional[str] = None,
        score_min: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Lead]:
        db = get_db()
        query = "SELECT * FROM leads WHERE 1=1"
        params: list = []
        if etapa:
            query += " AND etapa_funil = ?"
            params.append(etapa)
        if fonte:
            query += " AND fonte = ?"
            params.append(fonte)
        if score_min is not None:
            query += " AND score >= ?"
            params.append(score_min)
        query += " ORDER BY score DESC, created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        rows = db.execute(query, params).fetchall()
        return [Lead.from_row(dict(r)) for r in rows]

    def contar(
        self,
        etapa: Optional[str] = None,
        fonte: Optional[str] = None,
        score_min: Optional[int] = None,
    ) -> int:
        db = get_db()
        query = "SELECT COUNT(*) as cnt FROM leads WHERE 1=1"
        params: list = []
        if etapa:
            query += " AND etapa_funil = ?"
            params.append(etapa)
        if fonte:
            query += " AND fonte = ?"
            params.append(fonte)
        if score_min is not None:
            query += " AND score >= ?"
            params.append(score_min)
        row = db.execute(query, params).fetchone()
        return row["cnt"]

    def obter(self, lead_id: int) -> Optional[Lead]:
        db = get_db()
        row = db.execute("SELECT * FROM leads WHERE id = ?", [lead_id]).fetchone()
        if not row:
            return None
        return Lead.from_row(dict(row))

    def criar(self, lead: Lead) -> Lead:
        db = get_db()
        now = datetime.now(timezone.utc).isoformat()
        cur = db.execute(
            """INSERT INTO leads (nome, email, telefone, empresa, cargo, fonte, etapa_funil, score, tags, notas, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [lead.nome, lead.email, lead.telefone, lead.empresa, lead.cargo,
             lead.fonte, lead.etapa_funil, lead.score, lead.tags, lead.notas, now, now],
        )
        db.commit()
        lead.id = cur.lastrowid
        lead.created_at = now
        lead.updated_at = now
        return lead

    def criar_de_dict(self, data: dict) -> Lead:
        lead = Lead(
            nome=data.get("nome", ""),
            email=data.get("email", ""),
            telefone=data.get("telefone", ""),
            empresa=data.get("empresa", ""),
            cargo=data.get("cargo", ""),
            fonte=data.get("fonte", "webhook"),
            etapa_funil=data.get("etapa_funil", "novo"),
            tags=data.get("tags", ""),
            notas=data.get("notas", ""),
        )
        from app.services.scoring_service import calcular_score
        lead.score = calcular_score(lead)
        return self.criar(lead)

    def atualizar(self, lead: Lead):
        db = get_db()
        now = datetime.now(timezone.utc).isoformat()
        db.execute(
            """UPDATE leads SET nome=?, email=?, telefone=?, empresa=?, cargo=?,
               fonte=?, etapa_funil=?, score=?, tags=?, notas=?, updated_at=?
               WHERE id=?""",
            [lead.nome, lead.email, lead.telefone, lead.empresa, lead.cargo,
             lead.fonte, lead.etapa_funil, lead.score, lead.tags, lead.notas, now, lead.id],
        )
        db.commit()
        lead.updated_at = now

    def deletar(self, lead_id: int):
        db = get_db()
        db.execute("DELETE FROM interacoes WHERE lead_id = ?", [lead_id])
        db.execute("DELETE FROM leads WHERE id = ?", [lead_id])
        db.commit()
