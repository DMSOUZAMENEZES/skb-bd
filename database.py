import sqlite3
import os

DB_PATH = os.path.join("data", "skb.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    os.makedirs("data", exist_ok=True)
    os.makedirs(os.path.join("storage", "pdf"), exist_ok=True)
    os.makedirs(os.path.join("storage", "text"), exist_ok=True)
    os.makedirs("imports", exist_ok=True)

    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL UNIQUE,
            imported_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    conn.close()
