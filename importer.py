from __future__ import annotations

import hashlib
import shutil
from dataclasses import dataclass
from pathlib import Path

from database import DocumentRecord, document_exists_by_hash, init_db, upsert_document
from parser import extract_text_from_pdf, save_text_file


@dataclass(frozen=True)
class ImportResult:
    imported: int
    skipped: int


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def list_pdf_files(import_dir: Path) -> list[Path]:
    if not import_dir.exists():
        return []
    return sorted(
        [p for p in import_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"]
    )


def import_local_pdfs(
    db_path: Path,
    import_dir: Path,
    pdf_storage_dir: Path,
    text_storage_dir: Path,
    source: str = "local_import",
) -> ImportResult:
    init_db(db_path)
    import_dir.mkdir(parents=True, exist_ok=True)
    pdf_storage_dir.mkdir(parents=True, exist_ok=True)
    text_storage_dir.mkdir(parents=True, exist_ok=True)

    imported = 0
    skipped = 0
    for original_pdf in list_pdf_files(import_dir):
        file_hash = sha256_file(original_pdf)
        if document_exists_by_hash(db_path, file_hash):
            skipped += 1
            continue

        stored_pdf = pdf_storage_dir / f"{file_hash}.pdf"
        stored_txt = text_storage_dir / f"{file_hash}.txt"
        if not stored_pdf.exists():
            shutil.copy2(original_pdf, stored_pdf)

        extracted_text = extract_text_from_pdf(stored_pdf)
        save_text_file(extracted_text, stored_txt)

        doc = DocumentRecord(
            title=original_pdf.stem,
            url=f"file://{original_pdf.name}",
            source=source,
            sha256_hash=file_hash,
            local_pdf=str(stored_pdf),
            local_text=extracted_text,
        )
        upsert_document(db_path, doc)
        imported += 1

    return ImportResult(imported=imported, skipped=skipped)
