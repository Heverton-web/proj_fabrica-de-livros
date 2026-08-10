from app.database.connection import get_db


def run_migrations():
    """Aplica migrações incrementais no banco."""
    db = get_db()
    _criar_tabela_migrations(db)
    executadas = _migrations_executadas(db)

    for nome, sql in MIGRATIONS:
        if nome not in executadas:
            db.executescript(sql)
            db.execute("INSERT INTO migrations (nome) VALUES (?)", [nome])
            db.commit()


def _criar_tabela_migrations(db):
    db.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()


def _migrations_executadas(db) -> set:
    rows = db.execute("SELECT nome FROM migrations").fetchall()
    return {r["nome"] for r in rows}


MIGRATIONS = [
    (
        "001_add_lead_score_index",
        "CREATE INDEX IF NOT EXISTS idx_leads_score ON leads(score DESC);",
    ),
    (
        "002_add_lead_etapa_index",
        "CREATE INDEX IF NOT EXISTS idx_leads_etapa ON leads(etapa_funil);",
    ),
    (
        "003_add_interacoes_lead_index",
        "CREATE INDEX IF NOT EXISTS idx_interacoes_lead ON interacoes(lead_id);",
    ),
    (
        "004_add_emails_enviados_lead_index",
        "CREATE INDEX IF NOT EXISTS idx_emails_lead ON emails_enviados(lead_id);",
    ),
]
