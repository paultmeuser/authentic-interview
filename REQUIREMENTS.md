# SDE Take Home
Goal: Design and implement a small T-account ledger that supports double-entry
bookkeeping. This exercise is meant to showcase your ability to make clear domain
models, enforce invariants, and communicate trade-offs.

Time guidance: 3–5 hours total. Please don’t over-invest; depth of thinking,
correctness, and clarity matter more than breadth.

## What you’ll build
A minimal ledger service (CLI or small web/API app) that:

1. Manages a chart of accounts.
2. Records journal entries with line items (debits/credits) that must balance.
3. Posts entries to T-accounts and computes running balances.
4. Produces a Trial Balance report at a point in time.
5. (Small UI or CLI output is fine) Visualizes T-accounts with left/right columns, totals, and ending balance side.

You may implement this in the language/framework of your choice. We value strong fundamentals over any particular stack.

## What We're Looking For
Correctness: Enforce accounting rules at the domain boundary.
Design & clarity: Organize code with clear separation of concerns (domain,
persistence, presentation). A brief design note (see Deliverables) should explain
your choices.

Data storage: In-memory is fine; a simple file/SQLite persistence is also fine.
Please keep it lightweight.

Errors: Return helpful, actionable errors (e.g., “Entry 17 does not balance: debits 100 ≠ credits 90”).
Performance: Reasonable complexity (e.g., O(n) for posting and reporting). No
need to over-optimize.

## What to Submit
1. Source code (public repo link or archive).
2. README with:
How to run locally.
How to run tests (if you choose to write any).
Example commands or API calls.
3. Design note (½–1 page, DESIGN.md ):
Domain model and key types.
How you enforce invariants (where and why).
Data storage choice and trade-offs.
Edge cases you considered (e.g., empty postings, duplicate ids, invalid
account types)

Bonus (not required, nice if you have time): lightweight persistence, small UI,
CSV/JSON export, property-based tests, simple statements (BS/IS), multi-currency
design notes.