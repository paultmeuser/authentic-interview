from database.database import AbstractDatabase
from models.account import Account

def validate_account(account: Account) -> None:
    pass

class Ledger:

    def __init__(self, db: AbstractDatabase):
        self.db = db

    
    def add_account(self, account: Account) -> None:
        validate_account(account)
        self.db.add_account(account)
    
    def get_account(self, account_id: int) -> Account | None:
        return self.db.get_account(account_id)