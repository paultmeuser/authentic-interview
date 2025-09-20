# SDE Take Home project

Work in progress

Simple implementation of a double-entry transaction ledger.

To run the program, use python to launch the module `__main__.py`.

```shell
$ python3 __main__.py
```

This will launch an interactive shell for interacting with the ledger system.

> NOTE: The current implementation uses an memory data storage, so any input data will not persist beyond a single shell session.

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
