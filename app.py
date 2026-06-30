import sys
import database


def cmd_init():
    database.init_db()
    print("✔ data/skb.db criado")
    print("✔ tabela documents criada")
    print("✔ storage/pdf criada")
    print("✔ storage/text criada")
    print("✔ imports criada")


COMMANDS = {
    "init": cmd_init,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(f"Uso: python app.py [{' | '.join(COMMANDS)}]")
        sys.exit(1)
    COMMANDS[sys.argv[1]]()
