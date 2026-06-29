import argparse

from database import create_database


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

    args = parser.parse_args()

    if args.command == "init":
        create_database()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
