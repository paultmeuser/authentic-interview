from dataclasses import dataclass
from datetime import datetime
from prettytable import PrettyTable

from models.account import Account

# Immutable dataclasses for representing a report

@dataclass(frozen=True)
class ReportEntry:
    account: Account
    balance: int

    def __str__(self):
        return f"ReportEntry(account='{self.account}', balance={self.balance})"
    
    def table_row(self) -> list:
        return [self.account.id, self.account.name, str(self.account.type), self.balance]

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
    
    def table_str(self) -> str:
        table = PrettyTable()
        table.field_names = ["Account ID", "Account Name", "Type", "Balance"]
        table.add_rows(
            [entry.table_row() for entry in self.debits],
            divider=True
        )
        table.add_row(["", "Total Debits", "", self.debits_total], divider=True)
        table.add_rows(
            [entry.table_row() for entry in self.credits],
            divider=True
        )
        table.add_row(["", "Total Credits", "", self.credits_total], divider=True)
        return table.get_string(title=f"Trial Balance Report as of {self.timestamp.isoformat()}")