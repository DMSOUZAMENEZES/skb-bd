from pathlib import Path
import sqlite3

DB_PATH = Path("data") / "skb.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    Path("data").mkdir(parents=True, exist_ok=True)
    Path("storage/pdf").mkdir(parents=True, exist_ok=True)
    Path("storage/text").mkdir(parents=True, exist_ok=True)
    Path("imports").mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            source TEXT NOT NULL,
            url TEXT UNIQUE,
            pdf_path TEXT,
            text_path TEXT,
            sha256 TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def document_exists_by_hash(sha256_value: str) -> bool:
    conn = get_connection()
    row = conn.execute(
        "SELECT 1 FROM documents WHERE sha256 = ? LIMIT 1",
        (sha256_value,),
    ).fetchone()
    conn.close()
    return row is not None


def insert_document(
    title: str,
    source: str,
    pdf_path: str,
    sha256: str,
    url: str | None = None,
) -> int:
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO documents (title, source, url, pdf_path, sha256)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, source, url, pdf_path, sha256),
    )
    conn.commit()
    document_id = cursor.lastrowid
    conn.close()
    return document_id


if __name__ == "__main__":
    init_db()
    print(f"Banco criado: {DB_PATH}")
