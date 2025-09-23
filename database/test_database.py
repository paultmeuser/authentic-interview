import unittest
from datetime import datetime
from models.account import Account
from models.transaction import Transaction, TransactionEntry
from database.database import InMemoryDatabase

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDatabase()
        self.account1 = Account(id=1, name="Cash", type="debit")
        self.account2 = Account(id=2, name="Equity", type="credit")
        self.db.add_account(self.account1)
        self.db.add_account(self.account2)

    def test_add_and_get_account(self):
        account = self.db.get_account(1)
        self.assertEqual(account, self.account1)
        account_none = self.db.get_account(999)
        self.assertIsNone(account_none)

    def test_list_accounts(self):
        accounts = self.db.list_accounts()
        self.assertIn(self.account1, accounts)
        self.assertIn(self.account2, accounts)
        self.assertEqual(len(accounts), 2)

    def test_write_and_list_transactions(self):
        entry1 = TransactionEntry(account_id=1, value=100)
        entry2 = TransactionEntry(account_id=2, value=-100)
        transaction = Transaction(id=1, timestamp=datetime.now(), entries=(entry1, entry2))
        self.db.write_transaction(transaction)
        transactions = self.db.list_transactions()
        self.assertIn(transaction, transactions)
        self.assertEqual(len(transactions), 1)
    
    def test_add_account_duplicate_id_raises(self):
        duplicate_account = Account(id=1, name="Duplicate", type="debit")
        with self.assertRaises(ValueError) as context:
            self.db.add_account(duplicate_account)
        self.assertIn("Account with id 1 already exists", str(context.exception))

    def test_write_transaction_duplicate_id_raises(self):
        entry1 = TransactionEntry(account_id=1, value=100)
        entry2 = TransactionEntry(account_id=2, value=-100)
        transaction1 = Transaction(id=1, timestamp=datetime.now(), entries=(entry1, entry2))
        transaction2 = Transaction(id=1, timestamp=datetime.now(), entries=(entry1, entry2))
        self.db.write_transaction(transaction1)
        with self.assertRaises(ValueError) as context:
            self.db.write_transaction(transaction2)
        self.assertIn("Transaction with id 1 already exists", str(context.exception))

if __name__ == "__main__":
    unittest.main()
