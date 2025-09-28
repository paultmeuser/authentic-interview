from dataclasses import dataclass
from enum import Enum

class AccountType(Enum):

    CREDIT = "credit"
    DEBIT = "debit"

    def __str__(self):
        return str(self.value)

@dataclass(frozen=True)
class Account:
    id: int
    name: str
    type: AccountType
    description: str = ""

    def __post_init__(self):
        # Cast type to AccountType if it's a string
        object.__setattr__(self, 'type', AccountType(self.type) if not isinstance(self.type, AccountType) else self.type)

    def __str__(self):
        return f"Account(id={self.id}, name='{self.name}', type='{self.type}', description='{self.description}')"