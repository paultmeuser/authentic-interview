from dataclasses import dataclass
from datetime import datetime

# Immutable dataclasses for representing a financial transaction

@dataclass(frozen=True)
class TransactionEntry:
    account_id: int
    value: int  # Value in smallest currency unit (e.g., cents)
    

@dataclass(frozen=True)
class Transaction:
    id: int
    timestamp: datetime
    entries: tuple[TransactionEntry, ...]


    def __str__(self):
        entries_str = ", ".join(f"(Account ID: {e.account_id}, Value: {e.value})" for e in self.entries)
        return f"Transaction(id={self.id}, timestamp='{self.timestamp.isoformat()}', entries=[{entries_str}])"