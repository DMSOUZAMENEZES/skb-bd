import sys

import database
from importer import import_pdfs
from parser import parse_pdfs


def cmd_init():
    database.init_db()
    print("Banco e pastas inicializados")


def cmd_import():
    source_dir = sys.argv[2] if len(sys.argv) > 2 else "imports"
    try:
        imported, skipped = import_pdfs(source_dir)
    except ValueError as exc:
        print(f"Erro: {exc}")
        sys.exit(1)
    print(f"PDFs importados: {imported}; duplicados: {skipped}")


def cmd_parse():
    parsed, failed = parse_pdfs()
    print(f"PDFs processados: {parsed}; falhas: {failed}")
    if failed:
        sys.exit(1)


COMMANDS = {
    "init": cmd_init,
    "import": cmd_import,
    "parse": cmd_parse,
}


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Uso: python app.py init | import [pasta] | parse")
        sys.exit(1)
    COMMANDS[sys.argv[1]]()
