import cmd
import argparse

from app.ledger import Ledger
from models.account import Account, AccountType


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


    def do_exit(self, line: str):
        """Exit the Ledger shell."""
        print("Exiting...")
        return True

    def help_add_account(self):
        print(self.add_account_parser.format_help())

    def help_get_account(self):
        print(self.get_account_parser.format_help())

    def help_exit(self):
        print("Exit the Ledger shell.")