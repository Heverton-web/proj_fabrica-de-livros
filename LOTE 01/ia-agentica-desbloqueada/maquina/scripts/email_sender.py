#!/usr/bin/env python3
"""
Email Sender — Sequência automatizada de e-mails via SMTP.
Lê leads do banco, aplica funis com delays e templates,
rastreia aberturas/cliques via pixel e UTM.
"""

import json
import sqlite3
import smtplib
import logging
import os
import sys
import time
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate, make_msgid
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
TEMPLATE_DIR = BASE_DIR / "templates" / "emails"
DB_PATH = BASE_DIR / "database" / "leads.db"

LOG_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FMT)
log = logging.getLogger("email_sender")


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


# ---------------------------------------------------------------------------
# Template Engine (simples, sem dependências)
# ---------------------------------------------------------------------------
def render_template(template_path: Path, variables: dict) -> str:
    """Substitui {{VARIAVEL}} no template."""
    with open(template_path, encoding="utf-8") as f:
        content = f.read()
    for key, value in variables.items():
        content = content.replace(f"{{{{{key}}}}}", str(value))
    return content


# ---------------------------------------------------------------------------
# SMTP Client
# ---------------------------------------------------------------------------
class EmailSender:
    def __init__(self, config: dict):
        self.host = config["smtp_host"]
        self.port = config["smtp_port"]
        self.user = config["smtp_user"]
        self.password = config["smtp_password"]
        self.from_name = config.get("from_name", "Equipe")
        self.from_email = config.get("from_email", self.user)
        self.use_tls = config.get("use_tls", True)
        self.unsubscribe_url = config.get("unsubscribe_url", "")
        self.tracking_domain = config.get("tracking_domain", "")
        self.utm_source = config.get("utm_source", "email")
        self.utm_medium = config.get("utm_medium", "sequence")
        self._conn: Optional[smtplib.SMTP] = None

    def connect(self):
        self._conn = smtplib.SMTP(self.host, self.port)
        if self.use_tls:
            self._conn.starttls()
        self._conn.login(self.user, self.password)
        log.info(f"Conectado a {self.host}:{self.port}")

    def disconnect(self):
        if self._conn:
            self._conn.quit()
            self._conn = None

    def send(
        self,
        to_email: str,
        to_name: str,
        subject: str,
        html_body: str,
        text_body: str = "",
        lead_id: int | None = None,
        funnel_step: int | None = None,
    ) -> bool:
        """Envia um e-mail e registra no banco."""
        msg = MIMEMultipart("alternative")
        msg["From"] = formataddr((self.from_name, self.from_email))
        msg["To"] = formataddr((to_name, to_email))
        msg["Subject"] = subject
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain=self.from_email.split("@")[-1])
        msg["List-Unsubscribe"] = f"<{self.unsubscribe_url}>"

        # Texto plano
        if text_body:
            msg.attach(MIMEText(text_body, "plain", "utf-8"))

        # Tracking pixel
        if self.tracking_domain and lead_id:
            pixel = (
                f'<img src="{self.tracking_domain}/open?lid={lead_id}'
                f'&step={funnel_step}" width="1" height="1"'
                f' style="display:none" alt="" />'
            )
            html_body = html_body.replace("</body>", f"{pixel}</body>")

        # UTM nos links
        if self.utm_source:
            import re
            utm = f"utm_source={self.utm_source}&utm_medium={self.utm_medium}&utm_campaign=funnel_step_{funnel_step}"
            html_body = re.sub(
                r'href="(https?://[^"]+)"',
                lambda m: f'href="{m.group(1)}{"&" if "?" in m.group(1) else "?"}{utm}"',
                html_body
            )

        msg.attach(MIMEText(html_body, "html", "utf-8"))

        try:
            if not self._conn:
                self.connect()
            self._conn.sendmail(self.from_email, [to_email], msg.as_string())
            log.info(f"Enviado para {to_email} | step={funnel_step}")
            return True
        except smtplib.SMTPException as e:
            log.error(f"Falha ao enviar para {to_email}: {e}")
            self._conn = None  # Forçar reconexão
            return False


# ---------------------------------------------------------------------------
# Funnel Sequencer
# ---------------------------------------------------------------------------
class FunnelSequencer:
    def __init__(self, db: sqlite3.Connection, sender: EmailSender, funis: dict):
        self.db = db
        self.sender = sender
        self.funis = funis

    def get_due_leads(self, funnel_slug: str) -> list[dict]:
        """Retorna leads que devem receber o próximo e-mail agora."""
        # Garantir tabela de sequência
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS email_sequence (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id     INTEGER NOT NULL,
                funnel      TEXT NOT NULL,
                step        INTEGER DEFAULT 0,
                next_send   TEXT,
                status      TEXT DEFAULT 'ativo',
                opened_at   TEXT,
                clicked_at  TEXT,
                created_at  TEXT DEFAULT (datetime('now')),
                updated_at  TEXT DEFAULT (datetime('now')),
                UNIQUE(lead_id, funnel),
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            )
        """)
        self.db.commit()

        now = datetime.utcnow().isoformat()
        rows = self.db.execute("""
            SELECT es.*, l.username, l.email, l.full_name, l.persona_match
            FROM email_sequence es
            JOIN leads l ON l.id = es.lead_id
            WHERE es.funnel = ?
              AND es.status = 'ativo'
              AND es.next_send <= ?
              AND l.email IS NOT NULL
              AND l.contacted = 0
            ORDER BY es.next_send
            LIMIT 100
        """, (funnel_slug, now)).fetchall()
        return [dict(r) for r in rows]

    def processar_step(self, lead_seq: dict) -> bool:
        """Envia o próximo e-mail da sequência para um lead."""
        funnel_slug = lead_seq["funnel"]
        step = lead_seq["step"]
        funnel = self.funis.get(funnel_slug)
        if not funnel:
            log.error(f"Funil '{funnel_slug}' não encontrado")
            return False

        steps = funnel.get("steps", [])
        if step >= len(steps):
            # Sequência concluída
            self.db.execute(
                "UPDATE email_sequence SET status='concluido', updated_at=datetime('now') WHERE id=?",
                (lead_seq["id"],)
            )
            self.db.commit()
            log.info(f"Sequência concluída para lead {lead_seq['lead_id']}")
            return True

        step_config = steps[step]
        template_file = step_config.get("template")
        if not template_file:
            log.warning(f"Step {step} sem template definido")
            return False

        template_path = TEMPLATE_DIR / template_file
        if not template_path.exists():
            log.error(f"Template não encontrado: {template_path}")
            return False

        # Variáveis para o template
        variables = {
            "NOME": lead_seq.get("full_name") or lead_seq.get("username", ""),
            "USERNAME": lead_seq.get("username", ""),
            "PERSONA": lead_seq.get("persona_match", ""),
            "PRODUTO_NOME": funnel.get("produto", ""),
            "PRODUTO_LINK": funnel.get("produto_link", ""),
            "PRODUTO_PRECO": funnel.get("produto_preco", ""),
            "DESCONTO_CODIGO": funnel.get("desconto_codigo", ""),
            "DESCONTO_PORCENTO": funnel.get("desconto_porcento", ""),
            "EMPRESA_NOME": funnel.get("empresa", ""),
            "UNSUBSCRIBE_URL": self.sender.unsubscribe_url,
        }

        html_body = render_template(template_path, variables)
        subject = step_config.get("subject", "Mensagem importante para você")

        # Enviar
        ok = self.sender.send(
            to_email=lead_seq["email"],
            to_name=variables["NOME"],
            subject=subject,
            html_body=html_body,
            lead_id=lead_seq["lead_id"],
            funnel_step=step,
        )

        if ok:
            # Avançar step
            next_step = step + 1
            delay_hours = step_config.get("delay_hours", 24)
            next_send = (datetime.utcnow() + timedelta(hours=delay_hours)).isoformat()

            if next_step >= len(steps):
                status = "concluido"
            else:
                status = "ativo"

            self.db.execute("""
                UPDATE email_sequence
                SET step=?, next_send=?, status=?, updated_at=datetime('now')
                WHERE id=?
            """, (next_step, next_send, status, lead_seq["id"]))
            self.db.commit()

        return ok

    def executar(self, funnel_slug: str):
        """Executa todos os envios pendentes de um funil."""
        leads = self.get_due_leads(funnel_slug)
        log.info(f"Funil '{funnel_slug}': {len(leads)} leads pendentes")

        enviados, falhas = 0, 0
        for lead in leads:
            ok = self.processar_step(lead)
            if ok:
                enviados += 1
            else:
                falhas += 1
            time.sleep(1)  # Rate limit

        log.info(f"Resultado: {enviados} enviados, {falhas} falhas")


# ---------------------------------------------------------------------------
# Inscrição de leads no funil
# ---------------------------------------------------------------------------
def inscrever_leads(db: sqlite3.Connection, funnel_slug: str, persona: str | None = None):
    """Inscreve leads elegíveis no funil de e-mail."""
    db.execute("""
        CREATE TABLE IF NOT EXISTS email_sequence (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id     INTEGER NOT NULL,
            funnel      TEXT NOT NULL,
            step        INTEGER DEFAULT 0,
            next_send   TEXT,
            status      TEXT DEFAULT 'ativo',
            opened_at   TEXT,
            clicked_at  TEXT,
            created_at  TEXT DEFAULT (datetime('now')),
            updated_at  TEXT DEFAULT (datetime('now')),
            UNIQUE(lead_id, funnel),
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
    """)
    db.commit()

    where = "WHERE l.email IS NOT NULL AND l.stage = 'novo'"
    params: list = []
    if persona:
        where += " AND l.persona_match = ?"
        params.append(persona)

    leads = db.execute(f"""
        SELECT l.id FROM leads l
        {where}
        AND l.id NOT IN (
            SELECT lead_id FROM email_sequence WHERE funnel = ?
        )
    """, params + [funnel_slug]).fetchall()

    now = datetime.utcnow().isoformat()
    count = 0
    for row in leads:
        try:
            db.execute("""
                INSERT INTO email_sequence (lead_id, funnel, next_send)
                VALUES (?, ?, ?)
            """, (row["id"], funnel_slug, now))
            count += 1
        except sqlite3.IntegrityError:
            pass

    db.commit()
    log.info(f"{count} leads inscritos no funil '{funnel_slug}'")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Email Sender — Sequência automatizada")
    parser.add_argument("--funil", required=True, help="Slug do funil em config/funis.json")
    parser.add_argument("--persona", help="Filtrar por persona")
    parser.add_argument("--inscrever", action="store_true", help="Inscrever leads no funil")
    parser.add_argument("--executar", action="store_true", help="Executar envios pendentes")
    parser.add_argument("--dry-run", action="store_true", help="Apenas simula")
    args = parser.parse_args()

    email_config = load_json(CONFIG_DIR / "email.json")
    funis_config = load_json(CONFIG_DIR / "funis.json")
    funis = funis_config.get("funis", funis_config)

    db = get_db()

    if args.inscrever:
        inscrever_leads(db, args.funil, args.persona)

    if args.executar:
        if args.dry_run:
            log.info("DRY-RUN: simulando envios")
            return
        sender = EmailSender(email_config)
        sequencer = FunnelSequencer(db, sender, funis)
        try:
            sequencer.executar(args.funil)
        finally:
            sender.disconnect()

    if not args.inscrever and not args.executar:
        parser.print_help()


if __name__ == "__main__":
    main()
