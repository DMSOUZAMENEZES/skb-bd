from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class DocumentRecord:
    title: str
    url: str
    source: str
    sha256_hash: str
    local_pdf: str
    local_text: str


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def connect(db_path: str | Path) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str | Path) -> None:
    with connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                source TEXT NOT NULL,
                hash TEXT NOT NULL UNIQUE,
                local_pdf TEXT NOT NULL,
                local_text TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_documents_title ON documents(title)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_documents_source ON documents(source)"
        )
        conn.commit()


def document_exists_by_hash(db_path: str | Path, sha256_hash: str) -> bool:
    with connect(db_path) as conn:
        row = conn.execute(
            "SELECT 1 FROM documents WHERE hash = ? LIMIT 1", (sha256_hash,)
        ).fetchone()
    return row is not None


def upsert_document(db_path: str | Path, doc: DocumentRecord) -> None:
    updated_at = utc_now_iso()
    with connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO documents (title, url, source, hash, local_pdf, local_text, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(hash) DO UPDATE SET
                title = excluded.title,
                url = excluded.url,
                source = excluded.source,
                local_pdf = excluded.local_pdf,
                local_text = excluded.local_text,
                updated_at = excluded.updated_at
            """,
            (
                doc.title,
                doc.url,
                doc.source,
                doc.sha256_hash,
                doc.local_pdf,
                doc.local_text,
                updated_at,
            ),
        )
        conn.commit()


def search_documents(
    db_path: str | Path, query: str, limit: int = 10
) -> Iterable[sqlite3.Row]:
    like_query = f"%{query}%"
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT id, title, url, source, local_text, updated_at
            FROM documents
            WHERE title LIKE ? OR local_text LIKE ?
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (like_query, like_query, limit),
        ).fetchall()
    return rows
