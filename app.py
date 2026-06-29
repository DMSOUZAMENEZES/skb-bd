import argparse

from database import create_database, import_pdfs


def main():
    parser = argparse.ArgumentParser(
        prog="skb",
        description="SUS Knowledge Base"
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser(
        "init",
        help="Cria o banco SQLite"
    )

    import_parser = sub.add_parser(
        "import",
        help="Importa PDFs de uma pasta local para o banco"
    )
    import_parser.add_argument("directory", help="Diretorio com PDFs")

    args = parser.parse_args()

    if args.command == "init":
        create_database()
    elif args.command == "import":
        try:
            import_pdfs(args.directory)
        except (FileNotFoundError, NotADirectoryError) as exc:
            parser.error(str(exc))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
