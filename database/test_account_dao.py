import unittest
from models.account import Account, AccountType
from database.database import InMemoryDatabase
from database.account_dao import AccountDao


class TestAccountDao(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDatabase()
        self.dao = AccountDao(self.db)

    def test_add_and_get_account(self):
        acc = Account(id=1, name="Alice", type=AccountType.CREDIT, description="Test account")
        self.dao.add_account(acc)
        self.assertEqual(self.dao.get_account(1), acc)
        self.assertEqual(self.dao.get_account_by_name("Alice"), acc)

    def test_add_duplicate_id_raises(self):
        acc1 = Account(id=1, name="Alice", type=AccountType.CREDIT)
        acc2 = Account(id=1, name="Bob", type=AccountType.DEBIT)
        self.dao.add_account(acc1)
        with self.assertRaises(ValueError):
            self.dao.add_account(acc2)

    def test_add_duplicate_name_raises(self):
        acc1 = Account(id=1, name="Alice", type=AccountType.CREDIT)
        acc2 = Account(id=2, name="Alice", type=AccountType.DEBIT)
        self.dao.add_account(acc1)
        with self.assertRaises(ValueError):
            self.dao.add_account(acc2)

    def test_list_accounts(self):
        acc1 = Account(id=1, name="Alice", type=AccountType.CREDIT)
        acc2 = Account(id=2, name="Bob", type=AccountType.DEBIT)
        self.dao.add_account(acc1)
        self.dao.add_account(acc2)
        accounts = self.dao.list_accounts()
        self.assertEqual(set(accounts), {acc1, acc2})

    def test_get_account_not_found(self):
        self.assertIsNone(self.dao.get_account(999))
        self.assertIsNone(self.dao.get_account_by_name("Unknown"))