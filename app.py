from __future__ import annotations

import argparse
from pathlib import Path

from database import init_db, search_documents
from importer import import_local_pdfs


PROJECT_ROOT = Path(__file__).resolve().parent
STORAGE_ROOT = PROJECT_ROOT / "storage"
DB_PATH = STORAGE_ROOT / "skb.db"
IMPORT_DIR = STORAGE_ROOT / "import"
PDF_DIR = STORAGE_ROOT / "pdf"
TEXT_DIR = STORAGE_ROOT / "text"


def build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skb", description="SKB-BD: base local de documentos do SUS"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init-db", help="Cria o banco SQLite")
    subparsers.add_parser(
        "import", help="Importa PDFs de storage/import para storage/pdf e SQLite"
    )

    search_cmd = subparsers.add_parser(
        "search", help="Pesquisa por termo com SQLite LIKE"
    )
    search_cmd.add_argument("query", help="Termo de pesquisa")
    search_cmd.add_argument("--limit", type=int, default=10, help="Limite de resultados")

    return parser


def snippet(text: str, query: str, radius: int = 120) -> str:
    lower_text = text.lower()
    lower_query = query.lower()
    idx = lower_text.find(lower_query)
    if idx == -1:
        preview = text[: radius * 2].strip()
        return preview + ("..." if len(text) > len(preview) else "")

    start = max(0, idx - radius)
    end = min(len(text), idx + len(query) + radius)
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(text) else ""
    return prefix + text[start:end].strip() + suffix


def cmd_init_db() -> int:
    init_db(DB_PATH)
    print(f"Banco inicializado em: {DB_PATH}")
    return 0


def cmd_import() -> int:
    result = import_local_pdfs(
        db_path=DB_PATH,
        import_dir=IMPORT_DIR,
        pdf_storage_dir=PDF_DIR,
        text_storage_dir=TEXT_DIR,
    )
    print(f"Importados: {result.imported}")
    print(f"Ignorados (hash já existente): {result.skipped}")
    return 0


def cmd_search(query: str, limit: int) -> int:
    rows = list(search_documents(DB_PATH, query=query, limit=limit))
    if not rows:
        print("Nenhum resultado encontrado.")
        return 0

    for row in rows:
        print(f"[{row['id']}] {row['title']}")
        print(f"Fonte: {row['source']}")
        print(f"URL: {row['url']}")
        print(f"Trecho: {snippet(row['local_text'], query)}")
        print("-" * 72)
    return 0


def main() -> int:
    args = build_cli().parse_args()
    if args.command == "init-db":
        return cmd_init_db()
    if args.command == "import":
        return cmd_import()
    if args.command == "search":
        return cmd_search(args.query, args.limit)
    raise ValueError(f"Comando não suportado: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
