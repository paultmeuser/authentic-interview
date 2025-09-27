from models.account import Account
from database.database import AbstractDatabase

class AccountDao:

    def __init__(self, db: AbstractDatabase):
        self.db = db

    def add_account(self, account: Account) -> None:
        if self.db.get_account(account.id) is not None:
            raise ValueError(f"Account with id {account.id} already exists.")
        if self.db.get_account_by_name(account.name) is not None:
            raise ValueError(f"Account with name '{account.name}' already exists.")
        self.db.add_account(account)

    def get_account(self, account_id: int) -> Account | None:
        return self.db.get_account(account_id)
    
    def get_account_by_name(self, account_name: str) -> Account | None:
        return self.db.get_account_by_name(account_name)

    def list_accounts(self) -> list[Account]:
        return self.db.list_accounts()