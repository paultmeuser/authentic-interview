import unittest
from datetime import datetime
from app.ledger import Ledger
from models.account import Account
from models.transaction import Transaction, TransactionEntry
from database.database import InMemoryDatabase

class TestLedger(unittest.TestCase):
    def setUp(self):
        self.ledger = Ledger(InMemoryDatabase())

    def test_add_and_get_account(self):
        account = Account(id=1, name="Cash", type="debit")
        self.ledger.add_account(account)
        retrieved_account = self.ledger.get_account(1)
        self.assertEqual(retrieved_account, account)
    def test_add_balanced_transaction(self):
        acc1 = Account(id=1, name="Cash", type="debit")
        acc2 = Account(id=2, name="Revenue", type="credit")
        self.ledger.add_account(acc1)
        self.ledger.add_account(acc2)
        entries = (
            TransactionEntry(account_id=1, value=1000),
            TransactionEntry(account_id=2, value=1000),
        )
        txn = Transaction(id=1, timestamp=datetime.now(), entries=entries)
        self.ledger.add_transaction(txn)
        retrieved_txn = self.ledger.get_transaction(1)
        self.assertEqual(retrieved_txn, txn)

    def test_get_transaction_by_id(self):
        acc1 = Account(id=1, name="Cash", type="debit")
        acc2 = Account(id=2, name="Revenue", type="credit")
        self.ledger.add_account(acc1)
        self.ledger.add_account(acc2)
        entries = (
            TransactionEntry(account_id=1, value=500),
            TransactionEntry(account_id=2, value=500),
        )
        txn = Transaction(id=2, timestamp=datetime.now(), entries=entries)
        self.ledger.add_transaction(txn)
        txn_fetched = self.ledger.get_transaction(2)
        self.assertEqual(txn_fetched, txn)

    def test_add_unbalanced_transaction(self):
        acc1 = Account(id=1, name="Cash", type="debit")
        acc2 = Account(id=2, name="Revenue", type="credit")
        self.ledger.add_account(acc1)
        self.ledger.add_account(acc2)
        entries = (
            TransactionEntry(account_id=1, value=1000),
            TransactionEntry(account_id=2, value=900),
        )
        txn = Transaction(id=3, timestamp=datetime.now(), entries=entries)
        with self.assertRaises(ValueError):
            self.ledger.add_transaction(txn)

    def test_list_transactions(self):
        acc1 = Account(id=1, name="Cash", type="debit")
        acc2 = Account(id=2, name="Revenue", type="credit")
        self.ledger.add_account(acc1)
        self.ledger.add_account(acc2)
        txn1 = Transaction(
            id=1,
            timestamp=datetime.now(),
            entries=(
                TransactionEntry(account_id=1, value=200),
                TransactionEntry(account_id=2, value=200),
            ),
        )
        txn2 = Transaction(
            id=2,
            timestamp=datetime.now(),
            entries=(
                TransactionEntry(account_id=1, value=300),
                TransactionEntry(account_id=2, value=300),
            ),
        )
        self.ledger.add_transaction(txn1)
        self.ledger.add_transaction(txn2)
        txns = self.ledger.list_transactions()
        self.assertIn(txn1, txns)
        self.assertIn(txn2, txns)
        self.assertEqual(len(txns), 2)

    def test_get_historic_balance(self):
        acc1 = Account(id=1, name="Cash", type="debit")
        acc2 = Account(id=2, name="Revenue", type="credit")
        self.ledger.add_account(acc1)
        self.ledger.add_account(acc2)
        entries1 = (
            TransactionEntry(account_id=1, value=1000),
            TransactionEntry(account_id=2, value=1000),
        )
        txn1 = Transaction(id=1, timestamp=datetime(2024, 1, 1, 12, 0, 0), entries=entries1)
        self.ledger.add_transaction(txn1)
        entries2 = (
            TransactionEntry(account_id=1, value=500),
            TransactionEntry(account_id=2, value=500),
        )
        txn2 = Transaction(id=2, timestamp=datetime(2024, 6, 1, 12, 0, 0), entries=entries2)
        self.ledger.add_transaction(txn2)
        account, balance = self.ledger.get_historic_balance(1, datetime(2024, 12, 31))
        self.assertEqual(account, acc1)
        self.assertEqual(balance, 1500)
        account, balance = self.ledger.get_historic_balance(2, datetime(2024, 12, 31))
        self.assertEqual(account, acc2)
        self.assertEqual(balance, 1500)
        account, balance = self.ledger.get_historic_balance(1, datetime(2024, 3, 1))
        self.assertEqual(account, acc1)
        self.assertEqual(balance, 1000)
        account, balance = self.ledger.get_historic_balance(2, datetime(2024, 3, 1))
        self.assertEqual(account, acc2)
        self.assertEqual(balance, 1000)

    def test_get_account_balance(self):
        acc1 = Account(id=1, name="Cash", type="debit")
        acc2 = Account(id=2, name="Revenue", type="credit")
        self.ledger.add_account(acc1)
        self.ledger.add_account(acc2)
        account, balance = self.ledger.get_account_balance(1)
        self.assertEqual(account, acc1)
        self.assertEqual(balance, 0)
        entries1 = (
            TransactionEntry(account_id=1, value=1000),
            TransactionEntry(account_id=2, value=1000),
        )
        txn1 = Transaction(id=1, timestamp=datetime(2024, 1, 1, 12, 0, 0), entries=entries1)
        self.ledger.add_transaction(txn1)
        _, balance = self.ledger.get_account_balance(1)
        self.assertEqual(balance, 1000)
        entries2 = (
            TransactionEntry(account_id=1, value=500),
            TransactionEntry(account_id=2, value=500),
        )
        txn2 = Transaction(id=2, timestamp=datetime(2024, 6, 1, 12, 0, 0), entries=entries2)
        self.ledger.add_transaction(txn2)
        _, balance = self.ledger.get_account_balance(1)
        self.assertEqual(balance, 1500)
        entries3 = (
            TransactionEntry(account_id=1, value=-200),
            TransactionEntry(account_id=2, value=-200),
        )
        txn3 = Transaction(id=3, timestamp=datetime(2024, 9, 1, 12, 0, 0), entries=entries3)
        self.ledger.add_transaction(txn3)
        _, balance = self.ledger.get_account_balance(1)
        self.assertEqual(balance, 1300)


    def test_get_trial_balance_report(self):
        acc1 = Account(id=1, name="Cash", type="debit")
        acc2 = Account(id=2, name="Revenue", type="credit")
        acc3 = Account(id=3, name="Bank", type="debit")
        acc4 = Account(id=4, name="Sales", type="credit")
        self.ledger.add_account(acc1)
        self.ledger.add_account(acc2)
        self.ledger.add_account(acc3)
        self.ledger.add_account(acc4)
        entries1 = (
            TransactionEntry(account_id=1, value=1000),
            TransactionEntry(account_id=2, value=1000),
            TransactionEntry(account_id=3, value=2000),
            TransactionEntry(account_id=4, value=2000),
        )
        txn1 = Transaction(id=1, timestamp=datetime(2024, 1, 1, 12, 0, 0), entries=entries1)
        self.ledger.add_transaction(txn1)
        entries2 = (
            TransactionEntry(account_id=1, value=500),
            TransactionEntry(account_id=2, value=500),
            TransactionEntry(account_id=3, value=1000),
            TransactionEntry(account_id=4, value=1000),
        )
        txn2 = Transaction(id=2, timestamp=datetime(2024, 6, 1, 12, 0, 0), entries=entries2)
        self.ledger.add_transaction(txn2)
        report = self.ledger.get_trial_balance_report(datetime(2024, 12, 31))
        debits = list(report.debits)
        credits = list(report.credits)
        self.assertEqual(len(debits), 2)
        self.assertEqual(len(credits), 2)
        # Check names and balances
        debit_dict = {entry.account.name: entry.balance for entry in debits}
        credit_dict = {entry.account.name: entry.balance for entry in credits}
        self.assertEqual(debit_dict["Cash"], 1500)
        self.assertEqual(debit_dict["Bank"], 3000)
        self.assertEqual(credit_dict["Revenue"], 1500)
        self.assertEqual(credit_dict["Sales"], 3000)
        self.assertEqual(report.debits_total, 1500 + 3000)
        self.assertEqual(report.credits_total, 1500 + 3000)


