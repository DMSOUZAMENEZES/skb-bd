import argparse
from typing import Sequence

from crawler import sync_documents
from database import bulk_upsert_documents, init_db
from parser import parse_document_content
from search import run_search


def _cmd_sync() -> int:
    init_db()
    raw_documents = sync_documents()

    normalized_documents = []
    for doc in raw_documents:
        normalized_documents.append(
            {
                **doc,
                "content": parse_document_content(doc["content"]),
            }
        )

    saved_count = bulk_upsert_documents(normalized_documents)
    print(f"Sincronizacao concluida: {saved_count} documento(s) processado(s).")
    return 0


def _cmd_search(query: str, limit: int) -> int:
    init_db()
    rows = run_search(query=query, limit=limit)

    if not rows:
        print("Nenhum documento encontrado.")
        return 0

    print(f"{len(rows)} resultado(s):")
    for row in rows:
        print(
            f"- [{row['document_type'] or 'N/A'}] {row['title']} | {row['source_url']} | publicado: {row['published_at'] or 'N/A'}"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SKB - SUS Knowledge Base")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("sync", help="Sincroniza documentos oficiais para o banco local")

    search_parser = subparsers.add_parser("search", help="Pesquisa documentos no banco local")
    search_parser.add_argument("query", help="Termo de busca")
    search_parser.add_argument("--limit", type=int, default=10, help="Maximo de resultados")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "sync":
        return _cmd_sync()
    if args.command == "search":
        return _cmd_search(query=args.query, limit=args.limit)

    raise ValueError(f"Comando desconhecido: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
