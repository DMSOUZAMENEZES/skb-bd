import sys

import database
from importer import import_pdfs


def cmd_init():
    database.init_db()
    print("✔ data/skb.db criado")
    print("✔ tabela documents criada")
    print("✔ storage/pdf criada")
    print("✔ storage/text criada")
    print("✔ imports criada")


def cmd_import():
    source_dir = sys.argv[2] if len(sys.argv) > 2 else "imports"

    try:
        imported, skipped = import_pdfs(source_dir)
    except ValueError as exc:
        print(f"Erro: {exc}")
        sys.exit(1)

    print(f"✔ PDFs importados: {imported}")
    print(f"✔ PDFs ignorados (duplicados): {skipped}")


COMMANDS = {
    "init": cmd_init,
    "import": cmd_import,
}


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Uso:")
        print("  python app.py init")
        print("  python app.py import [pasta]")
        sys.exit(1)

    COMMANDS[sys.argv[1]]()
