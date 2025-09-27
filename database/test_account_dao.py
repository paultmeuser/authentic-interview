import pytest
from models.account import Account, AccountType
from database.database import InMemoryDatabase
from database.account_dao import AccountDao

@pytest.fixture
def dao():
    db = InMemoryDatabase()
    return AccountDao(db)

def make_account(id, name, type=AccountType.CREDIT, description=""):
    return Account(id=id, name=name, type=type, description=description)

def test_add_and_get_account(dao):
    acc = make_account(1, "Alice", AccountType.CREDIT, "Test account")
    dao.add_account(acc)
    assert dao.get_account(1) == acc
    assert dao.get_account_by_name("Alice") == acc

def test_add_duplicate_id_raises(dao):
    acc1 = make_account(1, "Alice", AccountType.CREDIT)
    acc2 = make_account(1, "Bob", AccountType.DEBIT)
    dao.add_account(acc1)
    with pytest.raises(ValueError):
        dao.add_account(acc2)

def test_add_duplicate_name_raises(dao):
    acc1 = make_account(1, "Alice", AccountType.CREDIT)
    acc2 = make_account(2, "Alice", AccountType.DEBIT)
    dao.add_account(acc1)
    with pytest.raises(ValueError):
        dao.add_account(acc2)

def test_list_accounts(dao):
    acc1 = make_account(1, "Alice", AccountType.CREDIT)
    acc2 = make_account(2, "Bob", AccountType.DEBIT)
    dao.add_account(acc1)
    dao.add_account(acc2)
    accounts = dao.list_accounts()
    assert set(accounts) == {acc1, acc2}

def test_get_account_not_found(dao):
    assert dao.get_account(999) is None
    assert dao.get_account_by_name("Unknown") is None
