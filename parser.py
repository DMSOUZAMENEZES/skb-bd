from pathlib import Path

import fitz

import database


TEXT_STORAGE = Path("storage/text")


def parse_pdfs() -> tuple[int, int]:
    database.init_db()
    TEXT_STORAGE.mkdir(parents=True, exist_ok=True)

    conn = database.get_connection()
    documents = conn.execute(
        "SELECT id, pdf_path FROM documents WHERE text_path IS NULL AND pdf_path IS NOT NULL"
    ).fetchall()
    conn.close()

    parsed = 0
    failed = 0

    for document_id, pdf_path in documents:
        source = Path(pdf_path)
        target = TEXT_STORAGE / f"{document_id}.txt"

        try:
            with fitz.open(source) as pdf:
                if not pdf.is_pdf:
                    raise ValueError("Arquivo não é PDF")
                text = "\n\n".join(page.get_text(sort=True) for page in pdf)

            if not text.strip():
                raise ValueError("PDF sem texto extraível (possível digitalização)")

            temp = target.with_suffix(".tmp")
            temp.write_text(text, encoding="utf-8")
            temp.replace(target)

            conn = database.get_connection()
            try:
                conn.execute(
                    "UPDATE documents SET text_path = ? WHERE id = ? AND text_path IS NULL",
                    (str(target), document_id),
                )
                conn.commit()
            finally:
                conn.close()
            parsed += 1
            print(f"OK: {source.name} -> {target}")
        except (OSError, RuntimeError, ValueError, fitz.FileDataError) as exc:
            failed += 1
            print(f"FALHA: {source.name}: {exc}")

    return parsed, failed
