# SDE Take Home project

Simple implementation of a double-entry transaction ledger.

## Dependencies
This project depends on some 3rd party libraries including `parameterized` and `prettytable`.
To install these dependencies, run:
```shell
$ pip install -r requirements.txt
```

To run the program, use python to launch the module `__main__.py`.

```shell
python3 __main__.py
```

This will launch an interactive shell for interacting with the ledger system.

> NOTE: The current implementation uses an memory data storage, so any input data will not persist beyond a single shell session.

## Useful Commands

to manage accounts:
```
(ledger)> add_account 1 Cash debit money in my pocket
(ledger)> add_account 2 Equity credit we have investors
(ledger)> get_account 1
Account(id=1, name='Cash', type='debit', description='money in my pocket')
(ledger)> get_account 2
Account(id=2, name='Equity', type='credit', description='we have investors')
```

to add transactions:
```
(ledger)> add_transaction 1 1:50 2:50 --timestamp=2025-09-20T10:09:08 
(ledger)> add_transaction 2 1:-25 2:-25 --timestamp=2025-09-22
```

to view formatted transactions:
```
+--------------------------------------------------------------------------+
|           Transaction Report as of 2025-09-28T23:14:14.040243            |
+----------------+---------------------+------+-----------+--------+-------+
| Transaction ID |      Timestamp      | Cash | Inventory | Equity | Loans |
+----------------+---------------------+------+-----------+--------+-------+
|       1        | 2024-01-01T00:00:00 | 500  |     0     |  200   |  300  |
|       2        | 2024-02-02T00:00:00 | -400 |    400    |   0    |   0   |
|       3        | 2024-03-03T00:00:00 | 1000 |    -250   |  500   |  250  |
|       4        | 2024-04-04T00:00:00 | 1000 |     0     |  500   |  500  |
+----------------+---------------------+------+-----------+--------+-------+
```

to view a Trial Balance Report:
```
(ledger)> get_trial_balance_report
+-------------------------------------------------------+
| Trial Balance Report as of 2025-09-28T23:28:01.548399 |
+--------------+-----------------+---------+------------+
|  Account ID  |   Account Name  |   Type  |  Balance   |
+--------------+-----------------+---------+------------+
|      1       |       Cash      |  debit  |    2100    |
|      3       |    Inventory    |  debit  |    150     |
+--------------+-----------------+---------+------------+
|              |   Total Debits  |         |    2250    |
+--------------+-----------------+---------+------------+
|      2       |      Equity     |  credit |    1200    |
|      4       |      Loans      |  credit |    1050    |
+--------------+-----------------+---------+------------+
|              |  Total Credits  |         |    2250    |
+--------------+-----------------+---------+------------+
```

In the shell session, enter `help` to view a list of commands. Enter `help <cmd>` to view help text for a specific command. For example:

```
$ python3 .\__main__.py
Welcome to the Ledger shell. Type help or ? to list commands.

(ledger)> help

Documented commands (type help <topic>):
========================================
add_account  exit  get_account  help

(ledger)> help add_account
usage: add_account [-h] id name {debit,credit} [description ...]

Add a new account

positional arguments:
  id              A unique numeric ID for the account.
  name            The name of the account.
  {debit,credit}  The type of the account (debit or credit).
  description     An optional plain text description of the account.

options:
  -h, --help      show this help message and exit
```
