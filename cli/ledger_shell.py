import cmd
import argparse
from datetime import datetime

from app.ledger import Ledger
from models.account import Account, AccountType
from models.transaction import Transaction, TransactionEntry


class LedgerShell(cmd.Cmd):
    intro = "Welcome to the Ledger shell. Type help or ? to list commands.\n"
    prompt = "(ledger)> "

    def __init__(self, ledger: Ledger):
        super().__init__()
        self.ledger = ledger

        self.add_account_parser = argparse.ArgumentParser(prog="add_account", description="Add a new account")
        self.add_account_parser.add_argument("id", type=int, help="A unique numeric ID for the account.")
        self.add_account_parser.add_argument("name", type=str, help="The name of the account.")
        self.add_account_parser.add_argument("type", type=AccountType, choices=[AccountType.DEBIT, AccountType.CREDIT], help="The type of the account (debit or credit).")
        self.add_account_parser.add_argument("description", type=str, nargs="*", default="", help="An optional plain text description of the account.")

        self.get_account_parser = argparse.ArgumentParser(prog="get_account", description="Get account details by ID")
        self.get_account_parser.add_argument("id", type=int, help="The unique numeric ID of the account to retrieve.")

        self.get_historic_balance_parser = argparse.ArgumentParser(prog="get_historic_balance", description="Get account balance as of a certain timestamp")
        self.get_historic_balance_parser.add_argument("id", type=int, help="The unique numeric ID of the account.")
        self.get_historic_balance_parser.add_argument("--timestamp", type=str, default=None, help="Optional timestamp (ISO format) to get balance as of that time. Defaults to now.")

        self.get_account_balance_parser = argparse.ArgumentParser(prog="get_account_balance", description="Get current account balance")
        self.get_account_balance_parser.add_argument("id", type=int, help="The unique numeric ID of the account.")

        self.get_trial_balance_report_parser = argparse.ArgumentParser(prog="get_trial_balance_report", description="Get trial balance report as of a certain timestamp")
        self.get_trial_balance_report_parser.add_argument("--timestamp", type=str, default=None, help="Optional timestamp (ISO format) to get report as of that time. Defaults to now.")

        self.add_transaction_parser = argparse.ArgumentParser(prog="add_transaction", description="Add a new transaction")
        self.add_transaction_parser.add_argument("id", type=int, help="A unique numeric ID for the transaction.")
        self.add_transaction_parser.add_argument("entries", type=str, nargs='+', help="Entries in the format <account_id>:<value> ...")
        self.add_transaction_parser.add_argument("--timestamp", type=str, default=None, help="Optional transaction timestamp (ISO format)")

        self.get_transaction_parser = argparse.ArgumentParser(prog="get_transaction", description="Get transaction details by ID")
        self.get_transaction_parser.add_argument("id", type=int, help="The unique numeric ID of the transaction to retrieve.")

    def do_add_transaction(self, line: str):
        """Add a new transaction: add_transaction <id> <account_id:value> [<account_id:value> ...]"""
        try:
            parsed_args = self.add_transaction_parser.parse_args(line.split())
        except SystemExit:
            return
        entries = []
        for entry_str in parsed_args.entries:
            try:
                account_id_str, value_str = entry_str.split(":")
                account_id = int(account_id_str)
                value = int(value_str)
                entries.append(TransactionEntry(account_id=account_id, value=value))
            except ValueError:
                print(f"Invalid entry format: '{entry_str}'. Expected <account_id>:<value>.")
                return
        txn_timestamp = datetime.now()
        if parsed_args.timestamp:
            try:
                txn_timestamp = datetime.fromisoformat(parsed_args.timestamp)
            except ValueError as e:
                print(f"Invalid timestamp: {e}")
                return
        txn = Transaction(id=parsed_args.id, timestamp=txn_timestamp, entries=tuple(entries))
        try:
            self.ledger.add_transaction(txn)
        except ValueError as e:
            print(f"Invalid Input: {e}")

    def do_get_transaction(self, line: str):
        """Get transaction details by ID: get_transaction <id>"""
        try:
            parsed_args = self.get_transaction_parser.parse_args(line.split())
        except SystemExit:
            return
        txn = self.ledger.get_transaction(parsed_args.id)
        if txn is None:
            print(f"Transaction with id {parsed_args.id} does not exist.")
        else:
            print(txn)

    def do_list_transactions(self, line: str):
        """List all transactions: list_transactions"""
        txns = self.ledger.list_transactions()
        for txn in txns:
            print(txn)

    def help_add_transaction(self):
        print(self.add_transaction_parser.format_help())

    def help_get_transaction(self):
        print(self.get_transaction_parser.format_help())

    def help_list_transactions(self):
        print("List all transactions.")

    def do_add_account(self, line: str):
        """Add a new account to the ledger: add_account <id> <name> <type> [<description>]"""
        try:
            parsed_args = self.add_account_parser.parse_args(line.split())
        except SystemExit:
            return

        new_account = Account(
            id=parsed_args.id,
            name=parsed_args.name,
            type=parsed_args.type,
            description=" ".join(parsed_args.description,))
        try:
            self.ledger.add_account(new_account)
        except ValueError as e:
            print(f"Invalid Input: {e}")
    
    def do_get_account(self, line: str):
        """Get account details by ID: get_account <id>"""
        try:
            parsed_args = self.get_account_parser.parse_args(line.split())
        except SystemExit:
            return

        account = self.ledger.get_account(parsed_args.id)
        if account is None:
            print(f"Account with id {parsed_args.id} does not exist.")
        else:
            print(account)

    def do_get_historic_balance(self, line: str):
        """Get account balance as of a certain timestamp (defaults to now): get_account_balance <id> [--timestamp <ISO timestamp>]"""
        try:
            parsed_args = self.get_historic_balance_parser.parse_args(line.split())
        except SystemExit:
            return
        
        txn_timestamp = datetime.now()
        if parsed_args.timestamp:
            try:
                txn_timestamp = datetime.fromisoformat(parsed_args.timestamp)
            except ValueError as e:
                print(f"Invalid timestamp: {e}")
                return
        account, balance = self.ledger.get_historic_balance(parsed_args.id, txn_timestamp)
        print(f"ID: {account.id} Account: {account.name} type: {account.type} balance as of {txn_timestamp.isoformat()}: {balance}")

    def do_get_account_balance(self, line: str):
        """Get current account balance: get_account_balance <id>"""
        try:
            parsed_args = self.get_account_balance_parser.parse_args(line.split())
        except SystemExit:
            return
        
        account, balance = self.ledger.get_account_balance(parsed_args.id)
        print(f"ID: {account.id} Account: {account.name} type: {account.type} current balance: {balance}")

    def do_get_trial_balance_report(self, line: str):
        """Get trial balance report as of a certain timestamp (defaults to now): get_trial_balance_report [--timestamp <ISO timestamp>]"""
        try:
            parsed_args = self.get_trial_balance_report_parser.parse_args(line.split())
        except SystemExit:
            return
        
        report_timestamp = datetime.now()
        if parsed_args.timestamp:
            try:
                report_timestamp = datetime.fromisoformat(parsed_args.timestamp)
            except ValueError as e:
                print(f"Invalid timestamp: {e}")
                return
        report = self.ledger.get_trial_balance_report(report_timestamp)
        print(report.table_str())

    def do_exit(self, _: str):
        """Exit the Ledger shell."""
        print("Exiting...")
        return True

    def help_add_account(self):
        print(self.add_account_parser.format_help())

    def help_get_account(self):
        print(self.get_account_parser.format_help())

    def help_exit(self):
        print("Exit the Ledger shell.")