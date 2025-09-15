# Design Notes

 This document describes the design I intended to work towards, but was not able to fully implement.

## Architecture

This ledger application would be divided into three domains:
1. storage
2. application logic
3. i/o translation

### Storage

Storage logic is bare-bones, simply store a dictionary of all accounts and a list of all transactions. Storage is in-memory because it was easiest to implement. I put the database behind an abstract class to make it easy to replace with another implementation.

With more time I would create a SQlite implementation, since persistent storage seems important for a ledger application

### Application Logic

The core application logic would live in its own module, and depend on the AbstractDatabse for storage. It would provide an API operating on the internal data model:

* add_account(account)
    * Passthrough method to add an account to the database
* add_transaction(transaction)
    * Perform input validation on incoming transactions:
        * Account ids point to real accounts in storage
        * Transaction includes 2 or more accounts
        * total credits = total debits
    * Failing validation raises a descriptive valueError
* create_report()
    * aggregates all transactions in storage into a report of total debits/credits to all accounts.

### I/O Translation

The interface for this app would either be a CLI implemented with argparse, or a REST API implemented with flask. Whichever one I used, the implementation would translate inputs/outputs into the internal data model before sending them through the internal API.







