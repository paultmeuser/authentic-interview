from abc import ABC, abstractmethod
from models.account import Account
from models.transaction import Transaction

class AbstractDatabase(ABC):

    @abstractmethod
    def add_account(self, account: Account) -> None:
        pass

    @abstractmethod
    def get_account(self, account_id: int) -> Account | None:
        pass

    @abstractmethod
    def get_account_by_name(self, account_name: str) -> Account | None:
        pass

    @abstractmethod
    def list_accounts(self) -> list[Account]:
        pass

    @abstractmethod
    def write_transaction(self, transaction: Transaction) -> None:
        pass

    @abstractmethod
    def list_transactions(self) -> list[Transaction]:
        pass

class InMemoryDatabase(AbstractDatabase):
    def __init__(self):
        self.accounts_by_id = {}
        self.accounts_by_name = {}
        self.transactions = []

    def add_account(self, account: Account) -> None:
        if account.id in self.accounts_by_id:
            raise ValueError(f"Account with id {account.id} already exists.")
        if account.name in self.accounts_by_name:
            raise ValueError(f"Account with name '{account.name}' already exists.")
        self.accounts_by_id[account.id] = account
        self.accounts_by_name[account.name] = account

    def get_account(self, account_id: int) -> Account | None:
        return self.accounts_by_id.get(account_id)
    
    def get_account_by_name(self, account_name: str) -> Account | None:
        return self.accounts_by_name.get(account_name)

    def list_accounts(self) -> list[Account]:
        return list(self.accounts_by_id.values())

    def write_transaction(self, transaction: Transaction) -> None:
        if transaction.id in {t.id for t in self.transactions}:
            raise ValueError(f"Transaction with id {transaction.id} already exists.")
        self.transactions.append(transaction)

    def list_transactions(self) -> list[Transaction]:
        return self.transactions