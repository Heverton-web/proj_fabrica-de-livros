import smtplib
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

from app.config import settings
from app.database.connection import get_db
from app.models.campanha import Campanha
from app.services.lead_service import LeadService


class EmailService:
    def __init__(self):
        self.lead_service = LeadService()

    def listar_campanhas(self, status: Optional[str] = None) -> List[Campanha]:
        db = get_db()
        query = "SELECT * FROM campanhas"
        params: list = []
        if status:
            query += " WHERE status = ?"
            params.append(status)
        query += " ORDER BY created_at DESC"
        rows = db.execute(query, params).fetchall()
        return [Campanha.from_row(dict(r)) for r in rows]

    def criar_campanha(self, camp: Campanha) -> Campanha:
        db = get_db()
        now = datetime.now(timezone.utc).isoformat()
        cur = db.execute(
            """INSERT INTO campanhas (nome, descricao, tipo, status, template_assunto, template_corpo, segmento_tags, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [camp.nome, camp.descricao, camp.tipo, camp.status,
             camp.template_assunto, camp.template_corpo, camp.segmento_tags, now, now],
        )
        db.commit()
        camp.id = cur.lastrowid
        camp.created_at = now
        return camp

    def enviar_campanha(self, campanha_id: int) -> dict:
        db = get_db()
        row = db.execute("SELECT * FROM campanhas WHERE id = ?", [campanha_id]).fetchone()
        if not row:
            return {"erro": "Campanha não encontrada"}
        camp = Campanha.from_row(dict(row))

        tags = [t.strip() for t in camp.segmento_tags.split(",") if t.strip()]
        leads = []
        for tag in tags:
            leads.extend(self.lead_service.listar(limit=1000))

        enviados = 0
        erros = 0
        for lead in leads:
            assunto = camp.template_assunto.replace("{{nome}}", lead.nome)
            corpo = camp.template_corpo.replace("{{nome}}", lead.nome).replace("{{empresa}}", lead.empresa)
            ok = self._enviar_email(lead.email, assunto, corpo)
            self._registrar_envio(lead.id, campanha_id, assunto, corpo, ok)
            if ok:
                enviados += 1
            else:
                erros += 1

        db.execute("UPDATE campanhas SET status = 'finalizada', updated_at = ? WHERE id = ?",
                   [datetime.now(timezone.utc).isoformat(), campanha_id])
        db.commit()
        return {"enviados": enviados, "erros": erros, "total": len(leads)}

    def listar_enviados(self, lead_id: Optional[int] = None, campanha_id: Optional[int] = None) -> list:
        db = get_db()
        query = "SELECT * FROM emails_enviados WHERE 1=1"
        params: list = []
        if lead_id:
            query += " AND lead_id = ?"
            params.append(lead_id)
        if campanha_id:
            query += " AND campanha_id = ?"
            params.append(campanha_id)
        query += " ORDER BY sent_at DESC"
        rows = db.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def _enviar_email(self, to: str, subject: str, body: str) -> bool:
        if not settings.SMTP_USER:
            return True  # modo dev — não envia de verdade
        try:
            msg = MIMEMultipart()
            msg["From"] = settings.SMTP_FROM
            msg["To"] = to
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            return True
        except Exception:
            return False

    def _registrar_envio(self, lead_id: int, campanha_id: int, assunto: str, corpo: str, sucesso: bool):
        db = get_db()
        now = datetime.now(timezone.utc).isoformat()
        db.execute(
            """INSERT INTO emails_enviados (lead_id, campanha_id, assunto, corpo, status, sent_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [lead_id, campanha_id, assunto, corpo, "enviado" if sucesso else "erro", now],
        )
        db.commit()
