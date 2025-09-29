from datetime import datetime
from collections import defaultdict

from database.database import AbstractDatabase
from database.account_dao import AccountDao
from database.transaction_dao import TransactionDao
from models.account import Account, AccountType
from models.report import TransactionReport, TrialBalanceReport, ReportEntry
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
    
    def get_transaction_report(self, timestamp: datetime) -> TransactionReport:
        accounts = self.account_dao.list_accounts()
        transactions = [txn for txn in self.list_transactions() if txn.timestamp <= timestamp]
        return TransactionReport(timestamp=timestamp, accounts=accounts, transactions=transactions)

    def get_historic_balance(self, account_id: int, timestamp: datetime) -> tuple[Account, int]:
        account = self.get_account(account_id)
        if account is None:
            raise ValueError(f"Account with ID {account_id} does not exist.")
        return self._get_historic_balances([account], timestamp)[0]

    def _get_historic_balances(self, account_list: list[Account], timestamp: datetime) -> list[tuple[Account, int]]:
        account_balances = {account.id: 0 for account in account_list}
        for txn in self.list_transactions():
            if txn.timestamp > timestamp:
                continue
            for entry in txn.entries:
                if entry.account_id in account_balances:
                    account_balances[entry.account_id] += entry.value
        return [(account, account_balances[account.id]) for account in account_list]
    
    
    def get_account_balance(self, account_id: int) -> tuple[Account, int]:
        account = self.get_account(account_id)
        if account is None:
            raise ValueError(f"Account with ID {account_id} does not exist.")
        return account, self.running_balance_cache[account_id]
    
    def get_trial_balance_report(self, timestamp: datetime) -> TrialBalanceReport:
        accounts = self.account_dao.list_accounts()
        account_balances = self._get_historic_balances(accounts, timestamp)
        debit_entries = [ReportEntry(account=account, balance=balance) for account, balance in account_balances if account.type == AccountType.DEBIT]
        debits_total = sum(entry.balance for entry in debit_entries)
        credit_entries = [ReportEntry(account=account, balance=balance) for account, balance in account_balances if account.type == AccountType.CREDIT]
        credits_total = sum(entry.balance for entry in credit_entries)
        return TrialBalanceReport(timestamp=timestamp, debits=debit_entries, debits_total=debits_total, credits=credit_entries, credits_total=credits_total)
        