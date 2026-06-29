from pathlib import Path
import hashlib
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


def _file_sha256(file_path: Path):
    digest = hashlib.sha256()

    with file_path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(8192), b""):
            digest.update(chunk)

    return digest.hexdigest()


def import_pdfs(import_dir):
    directory = Path(import_dir)

    if not directory.exists():
        raise FileNotFoundError(f"Diretorio nao encontrado: {directory}")

    if not directory.is_dir():
        raise NotADirectoryError(f"Caminho nao e diretorio: {directory}")

    create_database()

    pdf_files = sorted(
        path for path in directory.rglob("*")
        if path.is_file() and path.suffix.lower() == ".pdf"
    )

    if not pdf_files:
        print(f"Nenhum PDF encontrado em: {directory}")
        return

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    imported = 0
    skipped = 0

    for pdf_file in pdf_files:
        resolved_pdf = pdf_file.resolve()
        sha256 = _file_sha256(resolved_pdf)
        url = f"file://{resolved_pdf.as_posix()}"

        cur.execute(
            """
            INSERT OR IGNORE INTO documents
            (title, source, url, pdf_path, text_path, sha256)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                resolved_pdf.stem,
                "local",
                url,
                str(resolved_pdf),
                None,
                sha256,
            ),
        )

        if cur.rowcount == 1:
            imported += 1
        else:
            skipped += 1

    conn.commit()
    conn.close()

    print(f"Importacao concluida: {imported} novo(s), {skipped} duplicado(s).")


if __name__ == "__main__":
    create_database()
