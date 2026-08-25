from hashlib import sha256
from pathlib import Path
import shutil

import database


PDF_STORAGE = Path("storage/pdf")


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def import_pdfs(source_dir: str) -> tuple[int, int]:
    database.init_db()

    source = Path(source_dir)
    if not source.exists() or not source.is_dir():
        raise ValueError(f"Pasta não encontrada: {source}")

    imported = 0
    skipped = 0

    for pdf in sorted(source.glob("*.pdf")):
        digest = file_sha256(pdf)

        if database.document_exists_by_hash(digest):
            skipped += 1
            continue

        destination = PDF_STORAGE / pdf.name
        if destination.exists():
            destination = PDF_STORAGE / f"{pdf.stem}_{digest[:8]}.pdf"

        shutil.copy2(pdf, destination)

        database.insert_document(
            title=pdf.stem,
            source="local",
            pdf_path=str(destination),
            sha256=digest,
        )
        imported += 1

    return imported, skipped
