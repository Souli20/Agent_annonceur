"""
Petite base SQLite qui retient les offres déjà envoyées, pour ne jamais
notifier deux fois la même opportunité.
"""

import sqlite3
import hashlib
from contextlib import contextmanager

from config import DB_PATH


def _make_id(offre: dict) -> str:
    """Identifiant stable basé sur le lien (ou titre+entreprise si pas de lien)."""
    base = offre.get("lien") or f"{offre.get('titre')}|{offre.get('entreprise')}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


@contextmanager
def _connect():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()


def init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS offres_envoyees (
                id TEXT PRIMARY KEY,
                titre TEXT,
                entreprise TEXT,
                source TEXT,
                date_envoi TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def filtrer_nouvelles(offres: list[dict]) -> list[dict]:
    """Retourne uniquement les offres pas encore vues, et les marque comme vues."""
    init_db()
    nouvelles = []
    with _connect() as conn:
        for offre in offres:
            oid = _make_id(offre)
            existe = conn.execute(
                "SELECT 1 FROM offres_envoyees WHERE id = ?", (oid,)
            ).fetchone()
            if not existe:
                nouvelles.append(offre)
                conn.execute(
                    "INSERT INTO offres_envoyees (id, titre, entreprise, source) VALUES (?, ?, ?, ?)",
                    (oid, offre.get("titre"), offre.get("entreprise"), offre.get("source")),
                )
    return nouvelles
