from dataclasses import dataclass
from datetime import datetime

# Immutable dataclasses for representing a report

@dataclass(frozen=True)
class ReportEntry:
    account_name: str
    balance: int

    def __str__(self):
        return f"ReportEntry(account_name='{self.account_name}', balance={self.balance})"

@dataclass(frozen=True)
class TrialBalanceReport:
    timestamp: datetime
    debits: tuple[ReportEntry]
    debits_total: int
    credits: tuple[ReportEntry]
    credits_total: int

    def __str__(self):
        debits_str = ", ".join(str(entry) for entry in self.debits)
        credits_str = ", ".join(str(entry) for entry in self.credits)
        return (f"TrialBalanceReport(timestamp={self.timestamp.isoformat()}, "
                f"debits={debits_str}, debits_total={self.debits_total}, "
                f"credits={credits_str}, credits_total={self.credits_total})")