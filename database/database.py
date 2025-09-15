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
        self.accounts = {}
        self.transactions = []

    def add_account(self, account: Account) -> None:
        if account.id in self.accounts:
            raise ValueError(f"Account with id {account.id} already exists.")
        self.accounts[account.id] = account

    def get_account(self, account_id: int) -> Account | None:
        return self.accounts.get(account_id)

    def list_accounts(self) -> list[Account]:
        return list(self.accounts.values())

    def write_transaction(self, transaction: Transaction) -> None:
        if transaction.id in {t.id for t in self.transactions}:
            raise ValueError(f"Transaction with id {transaction.id} already exists.")
        self.transactions.append(transaction)

    def list_transactions(self) -> list[Transaction]:
        return self.transactions