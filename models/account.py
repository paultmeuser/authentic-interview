from dataclasses import dataclass
from enum import Enum

class AccountType(Enum):

    CREDIT = "credit"
    DEBIT = "debit"

    def __str__(self):
        return str(self.value)

@dataclass
class Account:
    id: int
    name: str
    type: AccountType
    description: str = ""

    def __str__(self):
        return f"Account(id={self.id}, name='{self.name}', type='{self.type}', description='{self.description}')"