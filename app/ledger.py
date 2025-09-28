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
