from datetime import datetime

from database.database import AbstractDatabase
from database.account_dao import AccountDao
from database.transaction_dao import TransactionDao
from models.account import Account
from models.transaction import Transaction

class Ledger:

    def __init__(self, db: AbstractDatabase):
        self.account_dao = AccountDao(db)
        self.transaction_dao = TransactionDao(db)

    def add_account(self, account: Account) -> None:
        self.account_dao.add_account(account)

    def get_account(self, account_id: int) -> Account | None:
        return self.account_dao.get_account(account_id)
    
    def add_transaction(self, transaction: Transaction) -> None:
        self.transaction_dao.add_transaction(transaction)

    def get_transaction(self, transaction_id: int) -> Transaction | None:
        return self.transaction_dao.get_transaction(transaction_id)
    
    def list_transactions(self) -> list[Transaction]:
        return self.transaction_dao.list_transactions()

    def get_account_balance(self, account_id: int, timestamp: datetime) -> tuple[Account, int]:
        account = self.get_account(account_id)
        if account is None:
            raise ValueError(f"Account with ID {account_id} does not exist.")
    
        balance = 0
        for txn in self.list_transactions():
            if txn.timestamp > timestamp:
                continue
            for entry in txn.entries:
                if entry.account_id == account_id:
                    balance += entry.value
        return account, balance