import argparse
from datetime import datetime
from models.account import Account, AccountType
from models.transaction import Transaction, TransactionEntry
from database.database import InMemoryDatabase

def main():
    parser = argparse.ArgumentParser(description="Ledger CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Add account command
    add_account_parser = subparsers.add_parser("add-account", help="Add a new account")
    add_account_parser.add_argument("id", type=int, help="Account ID")
    add_account_parser.add_argument("name", type=str, help="Account name")
    add_account_parser.add_argument("type", choices=[t.value for t in AccountType], help="Account type (debit/credit)")
    add_account_parser.add_argument("--description", type=str, default="", help="Account description")

    # Add transaction command
    add_tx_parser = subparsers.add_parser("add-transaction", help="Add a new transaction")
    add_tx_parser.add_argument("id", type=int, help="Transaction ID")
    add_tx_parser.add_argument("entries", nargs='+', help="Entries in format account_id:value (e.g. 1:100 2:-100)")

    # List transactions command
    list_tx_parser = subparsers.add_parser("list-transactions", help="List all transactions")

    args = parser.parse_args()
    db = InMemoryDatabase()

    if args.command == "add-account":
        account_type = AccountType(args.type)
        account = Account(id=args.id, name=args.name, type=account_type)
        db.add_account(account)
        print(f"Account added: {account}")

    elif args.command == "add-transaction":
        entries = []
        for entry_str in args.entries:
            try:
                account_id_str, value_str = entry_str.split(":")
                entry = TransactionEntry(account_id=int(account_id_str), value=int(value_str))
                entries.append(entry)
            except Exception:
                print(f"Invalid entry format: {entry_str}")
                return
        transaction = Transaction(id=args.id, timestamp=datetime.now(), entries=tuple(entries))
        db.write_transaction(transaction)
        print(f"Transaction added: {transaction}")

    elif args.command == "list-transactions":
        transactions = db.list_transactions()
        for tx in transactions:
            print(tx)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
