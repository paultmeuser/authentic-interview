from database.database import AbstractDatabase
from models.transaction import Transaction
from models.account import Account, AccountType

class TransactionWriter(AbstractDatabase):

    # Validates a 
    def validate_transaction(self, transaction: Transaction) -> None:

        if len(transaction.entries) < 2:
            raise ValueError("Transaction must have at least two entries.")

        debits = 0
        credits = 0

        for entry in transaction.entries:
            account = self.db.get_account(entry.account_id)
            if account is None:
                raise ValueError(f"Account with id {entry.account_id} does not exist.")
            match account.type:
                case AccountType.DEBIT:
                    debits += entry.value
                case AccountType.CREDIT:
                    credits += entry.value
                case _:
                    raise ValueError(f"Invalid account type {account.type} for account id {account.id}.")
        if debits != credits:
            raise ValueError(f"Transaction is not balanced. Total debits must equal total credits: total debits={debits}, total credits={credits}.")
        
        self.db.write_transaction(transaction)
