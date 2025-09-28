from models.transaction import Transaction
from database.database import AbstractDatabase

class TransactionDao:
    def __init__(self, db: AbstractDatabase):
        self.db = db

    def add_transaction(self, transaction: Transaction) -> None:
        if any(t.id == transaction.id for t in self.db.list_transactions()):
            raise ValueError(f"Transaction with id {transaction.id} already exists.")
        self.db.write_transaction(transaction)

    def get_transaction(self, transaction_id: int) -> Transaction | None:
        for t in self.db.list_transactions():
            if t.id == transaction_id:
                return t
        return None

    def list_transactions(self) -> list[Transaction]:
        return self.db.list_transactions()
