from datetime import datetime
from collections import defaultdict

from database.database import AbstractDatabase
from database.account_dao import AccountDao
from database.transaction_dao import TransactionDao
from models.account import Account
from models.transaction import Transaction

class Ledger:

    def __init__(self, db: AbstractDatabase):
        self.account_dao = AccountDao(db)
        self.transaction_dao = TransactionDao(db)
        self.running_balance_cache = defaultdict(int)
        now = datetime.now()
        for account in self.account_dao.list_accounts():
            self.running_balance_cache[account.id] = self.get_historic_balance(account.id, now)[1]

    def add_account(self, account: Account) -> None:
        self.account_dao.add_account(account)

    def get_account(self, account_id: int) -> Account | None:
        return self.account_dao.get_account(account_id)
    
    def add_transaction(self, transaction: Transaction) -> None:
        self.transaction_dao.add_transaction(transaction)
        for entry in transaction.entries:
            self.running_balance_cache[entry.account_id] += entry.value

    def get_transaction(self, transaction_id: int) -> Transaction | None:
        return self.transaction_dao.get_transaction(transaction_id)
    
    def list_transactions(self) -> list[Transaction]:
        return self.transaction_dao.list_transactions()

    def get_historic_balance(self, account_id: int, timestamp: datetime) -> tuple[Account, int]:
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
    
    def get_current_account_balance(self, account_id: int) -> tuple[Account, int]:
        account = self.get_account(account_id)
        if account is None:
            raise ValueError(f"Account with ID {account_id} does not exist.")
        return account, self.running_balance_cache[account_id]