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
