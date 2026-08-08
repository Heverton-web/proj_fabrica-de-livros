import os
import sqlite3
from pathlib import Path

_DB_PATH = os.environ.get("DATABASE_URL", "sqlite:///./data/vendas.db").replace("sqlite:///", "")
_conn: sqlite3.Connection | None = None


def _ensure_dir():
    Path(_DB_PATH).parent.mkdir(parents=True, exist_ok=True)


def get_db() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _ensure_dir()
        _conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.execute("PRAGMA journal_mode=WAL")
        _conn.execute("PRAGMA foreign_keys=ON")
    return _conn


def init_db():
    """Cria as tabelas se não existirem."""
    db = get_db()
    schema_path = Path(__file__).parent.parent.parent.parent / "database" / "schema.sql"
    if schema_path.exists():
        db.executescript(schema_path.read_text(encoding="utf-8"))
    db.commit()


def close_db():
    global _conn
    if _conn:
        _conn.close()
        _conn = None
