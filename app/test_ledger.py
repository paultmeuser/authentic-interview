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
