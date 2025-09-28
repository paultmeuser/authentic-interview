from models.transaction import Transaction
from database.database import AbstractDatabase

class TransactionDao:
    def __init__(self, db: AbstractDatabase):
        self.db = db

    def validate_transaction(self, transaction: Transaction) -> None:
        accounts_by_id = {}
        for entry in transaction.entries:
            if entry.account_id in accounts_by_id:
                continue
            account = self.db.get_account(entry.account_id)
            if account is None:
                raise ValueError(f"Account with ID {entry.account_id} does not exist.")
            accounts_by_id[entry.account_id] = account

        debit_total = 0
        credit_total = 0
        for entry in transaction.entries:
            account = accounts_by_id[entry.account_id]
            match(account.type):
                case "debit":
                    debit_total += entry.value
                case "credit":
                    credit_total += entry.value
                case _:
                    raise ValueError(f"Unknown account type '{account.type}' for account ID {account.id}.")
        
        if debit_total != credit_total:
            raise ValueError(f"Transaction is not balanced: debit total {debit_total} != credit total {credit_total}.")


    def add_transaction(self, transaction: Transaction) -> None:
        if self.db.get_transaction(transaction.id) is not None:
            raise ValueError(f"A Transaction with ID {transaction.id} already exists.")
        self.validate_transaction(transaction)
        self.db.add_transaction(transaction)

    def get_transaction(self, transaction_id: int) -> Transaction | None:
        return self.db.get_transaction(transaction_id)
    
    def list_transactions(self) -> list[Transaction]:
        return self.db.list_transactions()
