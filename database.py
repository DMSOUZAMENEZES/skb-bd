import hashlib
import os
import sqlite3
from pathlib import Path
from typing import Any, Iterable

DEFAULT_DB_PATH = os.environ.get("SKB_DB_PATH", "data/skb.db")


def _ensure_parent_dir(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    _ensure_parent_dir(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_url TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                document_type TEXT,
                published_at TEXT,
                content TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_documents_title ON documents(title)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_documents_updated_at ON documents(updated_at)"
        )
        conn.commit()


def build_content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def upsert_document(document: dict[str, Any], db_path: str = DEFAULT_DB_PATH) -> None:
    content_hash = document.get("content_hash") or build_content_hash(document["content"])

    with get_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO documents (
                source_url,
                title,
                document_type,
                published_at,
                content,
                content_hash,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(source_url) DO UPDATE SET
                title=excluded.title,
                document_type=excluded.document_type,
                published_at=excluded.published_at,
                content=excluded.content,
                content_hash=excluded.content_hash,
                updated_at=CURRENT_TIMESTAMP
            """,
            (
                document["source_url"],
                document["title"],
                document.get("document_type"),
                document.get("published_at"),
                document["content"],
                content_hash,
            ),
        )
        conn.commit()


def bulk_upsert_documents(documents: Iterable[dict[str, Any]], db_path: str = DEFAULT_DB_PATH) -> int:
    count = 0
    for document in documents:
        upsert_document(document, db_path=db_path)
        count += 1
    return count


def search_documents(query: str, db_path: str = DEFAULT_DB_PATH, limit: int = 10) -> list[sqlite3.Row]:
    sanitized_limit = max(1, min(limit, 50))
    like_pattern = f"%{query}%"

    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT id, title, source_url, document_type, published_at, updated_at
            FROM documents
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY updated_at DESC, id DESC
            LIMIT ?
            """,
            (like_pattern, like_pattern, sanitized_limit),
        ).fetchall()

    return rows
