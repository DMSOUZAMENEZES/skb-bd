from pathlib import Path
import sqlite3

DB_DIR = Path("data")
DB_FILE = DB_DIR / "skb.db"


def create_database():
    DB_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        source TEXT NOT NULL,
        url TEXT UNIQUE NOT NULL,
        pdf_path TEXT NOT NULL,
        text_path TEXT,
        sha256 TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

    print(f"Banco criado: {DB_FILE}")


if __name__ == "__main__":
    create_database()
