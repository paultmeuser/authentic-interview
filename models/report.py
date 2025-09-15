from dataclasses import dataclass
from account import Account

# Immutable dataclasses for representing a financial transaction

@dataclass(frozen=True)
class ReportEntry:
    account: Account
    total_value: int  # Value in smallest currency unit (e.g., cents)
    

@dataclass(frozen=True)
class Report:
    id: int
    entries: tuple[ReportEntry, ...]