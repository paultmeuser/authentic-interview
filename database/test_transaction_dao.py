import unittest
from datetime import datetime
from models.account import Account
from models.transaction import Transaction, TransactionEntry
from database.transaction_dao import TransactionDao
from database.database import InMemoryDatabase

class TestTransactionDao(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDatabase()
        self.dao = TransactionDao(self.db)
        self.db.add_account(Account(id=1, name="Cash", type="debit"))
        self.db.add_account(Account(id=2, name="Equity", type="credit"))
        self.db.add_account(Account(id=3, name="Inventory", type="debit"))
        self.db.add_account(Account(id=4, name="Revenue", type="credit"))

    def test_add_transaction_success(self):
        entries = (
            TransactionEntry(account_id=1, value=100),
            TransactionEntry(account_id=2, value=100),
        )
        transaction = Transaction(id=1, timestamp=datetime.now(), entries=entries)
        self.dao.add_transaction(transaction)
        self.assertEqual(self.db.get_transaction(1), transaction)

    def test_add_transaction_duplicate(self):
        entries = (
            TransactionEntry(account_id=1, value=100),
            TransactionEntry(account_id=2, value=100),
        )
        transaction = Transaction(id=1, timestamp=datetime.now(), entries=entries)
        self.dao.add_transaction(transaction)
        with self.assertRaises(ValueError):
            self.dao.add_transaction(transaction)
    
    def test_add_transaction_unbalanced(self):
        entries = (
            TransactionEntry(account_id=1, value=100),
            TransactionEntry(account_id=2, value=50),
        )
        transaction = Transaction(id=1, timestamp=datetime.now(), entries=entries)
        with self.assertRaises(ValueError):
            self.dao.add_transaction(transaction)
    
    def test_add_transaction_invalid_account(self):
        entries = (
            TransactionEntry(account_id=1, value=100),
            TransactionEntry(account_id=999, value=100),
        )
        transaction = Transaction(id=1, timestamp=datetime.now(), entries=entries)
        with self.assertRaises(ValueError):
            self.dao.add_transaction(transaction)
    
    def test_add_balanced_transaction_many_accounts(self):
        entries = (
            TransactionEntry(account_id=1, value=150),
            TransactionEntry(account_id=3, value=50),
            TransactionEntry(account_id=2, value=100),
            TransactionEntry(account_id=4, value=100),
        )
        transaction = Transaction(id=1, timestamp=datetime.now(), entries=entries)
        self.dao.add_transaction(transaction)
        self.assertEqual(self.db.get_transaction(1), transaction)
    
    def test_add_unbalanaced_transaction_many_accounts(self):
        entries = (
            TransactionEntry(account_id=1, value=150),
            TransactionEntry(account_id=3, value=50),
            TransactionEntry(account_id=2, value=100),
            TransactionEntry(account_id=4, value=50),
        )
        transaction = Transaction(id=1, timestamp=datetime.now(), entries=entries)
        with self.assertRaises(ValueError):
            self.dao.add_transaction(transaction)

    def test_add_transaction_only_debit_accounts(self):
        entries = (
            TransactionEntry(account_id=1, value=100),
            TransactionEntry(account_id=3, value=-100),
        )
        transaction = Transaction(id=1, timestamp=datetime.now(), entries=entries)
        self.dao.add_transaction(transaction)
        self.assertEqual(self.db.get_transaction(1), transaction)
    
    def test_add_transaction_only_credit_accounts(self):
        entries = (
            TransactionEntry(account_id=2, value=100),
            TransactionEntry(account_id=4, value=-100),
        )
        transaction = Transaction(id=1, timestamp=datetime.now(), entries=entries)
        self.dao.add_transaction(transaction)
        self.assertEqual(self.db.get_transaction(1), transaction)

    def test_get_transaction_found(self):
        entries = (
            TransactionEntry(account_id=1, value=100),
            TransactionEntry(account_id=2, value=100),
        )
        transaction = Transaction(id=1, timestamp=datetime.now(), entries=entries)
        self.dao.add_transaction(transaction)
        result = self.dao.get_transaction(1)
        self.assertEqual(result, transaction)

    def test_get_transaction_not_found(self):
        result = self.dao.get_transaction(2)
        self.assertIsNone(result)

    def test_list_transactions(self):
        entries1 = (
            TransactionEntry(account_id=1, value=100),
            TransactionEntry(account_id=2, value=100),
        )
        entries2 = (
            TransactionEntry(account_id=1, value=200),
            TransactionEntry(account_id=2, value=200),
        )
        t1 = Transaction(id=1, timestamp=datetime.now(), entries=entries1)
        t2 = Transaction(id=2, timestamp=datetime.now(), entries=entries2)
        self.dao.add_transaction(t1)
        self.dao.add_transaction(t2)
        result = list(self.dao.list_transactions())
        self.assertEqual(set(result), {t1, t2})

if __name__ == "__main__":
    unittest.main()
