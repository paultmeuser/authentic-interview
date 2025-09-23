import unittest
from app.ledger import Ledger
from models.account import Account
from database.database import InMemoryDatabase

class TestLedger(unittest.TestCase):

    def setUp(self):
        self.ledger = Ledger(InMemoryDatabase())
   
    def test_add_and_get_account(self):
        account = Account(id=1, name="Cash", type="debit")
        self.ledger.add_account(account)
        retrieved_account = self.ledger.get_account(1)
        self.assertEqual(retrieved_account, account)
