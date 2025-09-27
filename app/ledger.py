from database.database import AbstractDatabase
from database.account_dao import AccountDao
from models.account import Account

class Ledger:

    def __init__(self, db: AbstractDatabase):
        self.account_dao = AccountDao(db)

    def add_account(self, account: Account) -> None:
        self.account_dao.add_account(account)

    def get_account(self, account_id: int) -> Account | None:
        return self.account_dao.get_account(account_id)
