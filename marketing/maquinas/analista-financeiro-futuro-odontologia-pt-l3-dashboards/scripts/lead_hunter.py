#!/usr/bin/env python3
"""
Lead Hunter — Busca automatizada de leads via Instagram Graph API.
Coleta perfis por hashtag/localização, filtra por critérios de persona,
e persiste em SQLite para downstream (email_sender, funnel_monitor).
"""

import json
import sqlite3
import time
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "personas.json"
CANAL_PATH = BASE_DIR / "config" / "canais.json"
DB_PATH = BASE_DIR / "database" / "leads.db"

LOG_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FMT)
log = logging.getLogger("lead_hunter")

INSTAGRAM_API_BASE = "https://graph.instagram.com/v18.0"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_db(path: Path = DB_PATH) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            instagram_id    TEXT UNIQUE,
            username        TEXT NOT NULL,
            full_name       TEXT,
            bio             TEXT,
            followers       INTEGER DEFAULT 0,
            following       INTEGER DEFAULT 0,
            media_count     INTEGER DEFAULT 0,
            email           TEXT,
            phone           TEXT,
            website         TEXT,
            city            TEXT,
            state           TEXT,
            persona_match   TEXT,
            score           REAL DEFAULT 0.0,
            stage           TEXT DEFAULT 'novo',
            source_hashtag  TEXT,
            source_location TEXT,
            captured_at     TEXT DEFAULT (datetime('now')),
            updated_at      TEXT DEFAULT (datetime('now')),
            contacted       INTEGER DEFAULT 0,
            tags            TEXT DEFAULT '[]'
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS lead_interactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id     INTEGER NOT NULL,
            channel     TEXT NOT NULL,
            action      TEXT NOT NULL,
            content     TEXT,
            created_at  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_leads_stage ON leads(stage)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_leads_persona ON leads(persona_match)
    """)
    conn.commit()
    return conn


def calcular_score(lead: dict, persona: dict) -> float:
    """Score 0-100 baseado em critérios da persona."""
    score = 0.0
    criterios = persona.get("criterios", {})

    # Seguidores (peso 25)
    min_followers = criterios.get("min_seguidores", 100)
    max_followers = criterios.get("max_seguidores", 100000)
    followers = lead.get("followers", 0)
    if min_followers <= followers <= max_followers:
        score += 25.0
    elif followers > 0:
        ratio = min(followers / min_followers, max_followers / followers)
        score += 12.5 * min(ratio, 1.0)

    # Bio keywords (peso 30)
    bio = (lead.get("bio") or "").lower()
    keywords = criterios.get("bio_keywords", [])
    if keywords:
        hits = sum(1 for kw in keywords if kw.lower() in bio)
        score += 30.0 * (hits / len(keywords))

    # Engajamento estimado (peso 20)
    media_count = lead.get("media_count", 0)
    if media_count >= criterios.get("min_posts", 10):
        score += 20.0
    elif media_count > 0:
        score += 10.0

    # Contato disponível (peso 15)
    if lead.get("email"):
        score += 8.0
    if lead.get("phone"):
        score += 4.0
    if lead.get("website"):
        score += 3.0

    # Localização (peso 10)
    localizacoes = criterios.get("localizacoes", [])
    city = (lead.get("city") or "").lower()
    state = (lead.get("state") or "").lower()
    if localizacoes:
        for loc in localizacoes:
            if loc.lower() in city or loc.lower() in state:
                score += 10.0
                break

    return round(min(score, 100.0), 2)


def match_persona(lead: dict, personas: list[dict]) -> Optional[str]:
    """Retorna slug da persona com maior score, ou None."""
    best_slug, best_score = None, 0.0
    for p in personas:
        s = calcular_score(lead, p)
        if s > best_score:
            best_score = s
            best_slug = p["slug"]
    return best_slug if best_score >= 30.0 else None


# ---------------------------------------------------------------------------
# Instagram API Client
# ---------------------------------------------------------------------------
class InstagramClient:
    def __init__(self, access_token: str):
        self.token = access_token
        self.session = requests.Session()
        self.session.params = {"access_token": access_token}  # type: ignore

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        url = f"{INSTAGRAM_API_BASE}/{endpoint}"
        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def search_hashtag(self, tag: str) -> list[dict]:
        """Busca mídia recente por hashtag."""
        # 1) Obter hashtag ID
        data = self._get("ig_hashtag_search", {"q": tag, "user_id": "me"})
        if not data.get("data"):
            log.warning(f"Hashtag '#{tag}' não encontrada")
            return []
        hashtag_id = data["data"][0]["id"]

        # 2) Buscar mídias recentes
        media = self._get(f"{hashtag_id}/recent_media", {
            "user_id": "me",
            "fields": "id,caption,media_type,timestamp,permalink"
        })
        return media.get("data", [])

    def get_user_info(self, user_id: str) -> dict:
        """Obtém detalhes de um perfil público."""
        fields = "id,username,name,biography,followers_count,follows_count,media_count,profile_picture_url,website"
        return self._get(user_id, {"fields": fields})

    def get_media_comments(self, media_id: str) -> list[dict]:
        """Extrai comentários de uma mídia (potenciais leads)."""
        data = self._get(f"{media_id}/comments", {
            "fields": "id,text,username,timestamp"
        })
        return data.get("data", [])


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------
def coletar_leads(
    hashtags: list[str],
    personas: list[dict],
    max_per_tag: int = 50,
    delay: float = 1.5,
) -> list[dict]:
    """Pipeline completo: buscar → filtrar → persistir."""
    token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    if not token:
        log.error("INSTAGRAM_ACCESS_TOKEN não definido no ambiente")
        sys.exit(1)

    client = InstagramClient(token)
    db = get_db()
    leads_capturados = []

    for tag in hashtags:
        log.info(f"Buscando hashtag: #{tag}")
        try:
            medias = client.search_hashtag(tag)
        except requests.HTTPError as e:
            log.error(f"Erro na API para #{tag}: {e}")
            continue

        count = 0
        for media in medias:
            if count >= max_per_tag:
                break

            # Extrair leads dos comentários
            try:
                comments = client.get_media_comments(media["id"])
            except requests.HTTPError:
                comments = []

            for comment in comments:
                username = comment.get("username")
                if not username:
                    continue

                # Evitar duplicatas
                existing = db.execute(
                    "SELECT id FROM leads WHERE instagram_id = ?",
                    (comment.get("id"),)
                ).fetchone()
                if existing:
                    continue

                # Montar lead bruto
                lead_raw = {
                    "instagram_id": comment.get("id"),
                    "username": username,
                    "full_name": "",
                    "bio": comment.get("text", ""),
                    "followers": 0,
                    "following": 0,
                    "media_count": 0,
                    "email": None,
                    "phone": None,
                    "website": None,
                    "city": "",
                    "state": "",
                    "source_hashtag": tag,
                    "source_location": None,
                }

                # Enriquecer com dados do perfil
                try:
                    time.sleep(delay)
                    user_info = client.get_user_info(username)
                    lead_raw.update({
                        "full_name": user_info.get("name", ""),
                        "bio": user_info.get("biography", lead_raw["bio"]),
                        "followers": user_info.get("followers_count", 0),
                        "following": user_info.get("follows_count", 0),
                        "media_count": user_info.get("media_count", 0),
                        "website": user_info.get("website"),
                    })
                except requests.HTTPError:
                    pass

                # Calcular score e persona
                persona_match = match_persona(lead_raw, personas)
                if not persona_match:
                    continue

                score = calcular_score(lead_raw, next(
                    p for p in personas if p["slug"] == persona_match
                ))

                # Persistir
                try:
                    db.execute("""
                        INSERT OR IGNORE INTO leads
                        (instagram_id, username, full_name, bio, followers,
                         following, media_count, email, phone, website,
                         city, state, persona_match, score, source_hashtag,
                         source_location, tags)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        lead_raw["instagram_id"], lead_raw["username"],
                        lead_raw["full_name"], lead_raw["bio"],
                        lead_raw["followers"], lead_raw["following"],
                        lead_raw["media_count"], lead_raw["email"],
                        lead_raw["phone"], lead_raw["website"],
                        lead_raw["city"], lead_raw["state"],
                        persona_match, score, tag, None, "[]"
                    ))
                    db.commit()
                    leads_capturados.append({**lead_raw, "persona_match": persona_match, "score": score})
                    count += 1
                    log.info(f"  Lead: @{lead_raw['username']} | persona={persona_match} | score={score}")
                except sqlite3.IntegrityError:
                    pass

            time.sleep(delay)

        log.info(f"#{tag}: {count} leads capturados")

    total = len(leads_capturados)
    log.info(f"Total: {total} leads novos capturados")
    return leads_capturados


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Lead Hunter — Instagram")
    parser.add_argument("--hashtags", nargs="+", help="Hashtags para buscar")
    parser.add_argument("--max-per-tag", type=int, default=50)
    parser.add_argument("--delay", type=float, default=1.5, help="Delay entre requisições (seg)")
    parser.add_argument("--dry-run", action="store_true", help="Apenas simula, não persiste")
    parser.add_argument("--stats", action="store_true", help="Mostra estatísticas do banco")
    args = parser.parse_args()

    if args.stats:
        db = get_db()
        total = db.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
        por_stage = db.execute(
            "SELECT stage, COUNT(*) FROM leads GROUP BY stage"
        ).fetchall()
        por_persona = db.execute(
            "SELECT persona_match, COUNT(*) FROM leads WHERE persona_match IS NOT NULL GROUP BY persona_match"
        ).fetchall()
        print(f"\n{'='*50}")
        print(f"  LEAD HUNTER — Estatísticas")
        print(f"{'='*50}")
        print(f"  Total de leads: {total}")
        print(f"\n  Por estágio:")
        for row in por_stage:
            print(f"    {row[0]:20s} → {row[1]}")
        print(f"\n  Por persona:")
        for row in por_persona:
            print(f"    {row[0]:20s} → {row[1]}")
        print(f"{'='*50}\n")
        return

    if not args.hashtags:
        # Carregar hashtags do config de canais
        canais = load_json(CANAL_PATH)
        hashtags = canais.get("instagram", {}).get("hashtags", [])
        if not hashtags:
            log.error("Nenhuma hashtag fornecida e config/canais.json vazio")
            sys.exit(1)
    else:
        hashtags = args.hashtags

    personas = load_json(CONFIG_PATH)
    if isinstance(personas, dict):
        personas = personas.get("personas", [])

    if args.dry_run:
        log.info("DRY-RUN: nenhuma escrita no banco")
        for tag in hashtags:
            log.info(f"  Simularia busca em #{tag}")
        return

    coletar_leads(
        hashtags=hashtags,
        personas=personas,
        max_per_tag=args.max_per_tag,
        delay=args.delay,
    )


if __name__ == "__main__":
    main()
