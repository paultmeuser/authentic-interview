from dataclasses import dataclass
from enum import Enum

class AccountType(Enum):
    CREDIT = "credit"
    DEBIT = "debit"

@dataclass
class Account:
    id: int
    name: str
    description = ""
    type: AccountType