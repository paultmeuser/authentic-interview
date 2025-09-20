from app.ledger import Ledger
from database.database import InMemoryDatabase
from cli.ledger_shell import LedgerShell


if __name__ == "__main__":
    db = InMemoryDatabase()
    ledger = Ledger(db)
    LedgerShell(ledger).cmdloop()