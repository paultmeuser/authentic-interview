from unittest import TestCase, mock
from io import StringIO

from parameterized import parameterized
from cli.ledger_shell import LedgerShell
from models.account import Account, AccountType
from models.transaction import Transaction, TransactionEntry
from datetime import datetime

class TestLedgerShell(TestCase):

    def setUp(self):
        self.mock_ledger = mock.MagicMock()
        self.shell = LedgerShell(self.mock_ledger)

    def test_add_transaction_valid_format(self):
        self.shell.do_add_transaction("1 1:100 2:100")
        self.assertTrue(self.mock_ledger.add_transaction.called)

    def test_add_transaction_with_timestamp(self):
        expected_entries = (
            TransactionEntry(account_id=1, value=200), 
            TransactionEntry(account_id=2, value=200)
        )
        expected_txn = Transaction(
            id=2,
            timestamp=datetime.fromisoformat("2025-09-28T12:00:00"),
            entries=expected_entries
        )
        self.shell.do_add_transaction("2 1:200 2:200 --timestamp 2025-09-28T12:00:00")
        self.mock_ledger.add_transaction.assert_called_once_with(expected_txn)

    def test_add_transaction_invalid_entry_format(self):
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.shell.do_add_transaction("1 1-100 2:-100")
            self.assertIn("Invalid entry format", mock_stdout.getvalue())
        self.mock_ledger.add_transaction.assert_not_called()

    def test_add_transaction_invalid_timestamp(self):
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.shell.do_add_transaction("3 1:100 2:-100 --timestamp not-a-date")
            self.assertIn("Invalid timestamp", mock_stdout.getvalue())
        self.mock_ledger.add_transaction.assert_not_called()

    def test_get_transaction(self):
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.shell.do_get_transaction("1")
        self.mock_ledger.get_transaction.assert_called_once_with(1)

    def test_list_transactions(self):
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.shell.do_list_transactions("")
        self.mock_ledger.list_transactions.assert_called_once()

    
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
        with mock.patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            self.shell.do_add_account(command_arg_list)
            self.mock_ledger.add_account.assert_not_called()

    def test_get_account(self):
        account = Account(id=1, name="Cash", type=AccountType.DEBIT, description="")
        self.mock_ledger.get_account.return_value = account

        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.shell.do_get_account("1")
            self.mock_ledger.get_account.assert_called_once_with(1)
            self.assertIn(str(account), mock_stdout.getvalue())

    def test_get_account_balance(self):
        account = Account(id=1, name="Cash", type=AccountType.DEBIT, description="")
        balance = 1000
        self.mock_ledger.get_account_balance.return_value = (account, balance)
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.shell.do_get_account_balance("1 --timestamp 2025-09-28T12:00:00")
            self.mock_ledger.get_account_balance.assert_called_once_with(1, datetime.fromisoformat("2025-09-28T12:00:00"))