from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = [(page.extract_text() or "") for page in reader.pages]
    text = "\n".join(pages).strip()
    return text


def save_text_file(text: str, txt_path: str | Path) -> None:
    path = Path(txt_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
