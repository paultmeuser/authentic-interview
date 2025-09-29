from dataclasses import dataclass
from datetime import datetime

from models.account import Account

# Immutable dataclasses for representing a report

@dataclass(frozen=True)
class ReportEntry:
    account_name: str
    total_value: int

@dataclass(frozen=True)
class TrialBalanceReport:
    timestamp: datetime
    debits: tuple[ReportEntry]
    debits_total: int
    credits: tuple[ReportEntry]
    credits_total: int