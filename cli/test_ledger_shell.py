import unittest
from io import StringIO

from parameterized import parameterized
from cli.ledger_shell import LedgerShell
from models.account import Account, AccountType

class TestLedgerShell(unittest.TestCase):

    def setUp(self):
        self.mock_ledger = unittest.mock.MagicMock()
        self.shell = LedgerShell(self.mock_ledger)

    
    @parameterized.expand([
        ("1 Cash debit", Account(id=1, name="Cash", type=AccountType.DEBIT, description="")),
        ("1 Inventory debit description", Account(id=1, name="Inventory", type=AccountType.DEBIT, description="description")),
        ("1 Equity credit we have investors!", Account(id=1, name="Equity", type=AccountType.CREDIT, description="we have investors!")),
    ])
    def test_add_account_valid_format(self, command_arg_list, expected_account):
        self.shell.do_add_account(command_arg_list)
        self.mock_ledger.add_account.assert_called_once_with(expected_account)

    @parameterized.expand([
        ("1 Cash unknown",),  # Invalid account type
        ("1",),              # Missing arguments
        ("",),               # Empty input
    ])
    def test_add_account_invalid_format(self, command_arg_list):
        self.shell.do_add_account(command_arg_list)
        self.mock_ledger.add_account.assert_not_called()

    def test_get_account(self):
        account = Account(id=1, name="Cash", type=AccountType.DEBIT, description="")
        self.mock_ledger.get_account.return_value = account

        with unittest.mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.shell.do_get_account("1")
            self.mock_ledger.get_account.assert_called_once_with(1)
            self.assertIn(str(account), mock_stdout.getvalue())