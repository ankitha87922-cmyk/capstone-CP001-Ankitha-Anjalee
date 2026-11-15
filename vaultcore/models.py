"""Simple data objects used by VaultCore."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Account:
    account_number: str
    holder_name: str
    phone: str
    account_type: str
    balance: Decimal
    is_active: bool = True


@dataclass
class Transaction:
    timestamp: str
    account_number: str
    transaction_type: str
    amount: Decimal
    balance_after: Decimal
    note: str = ""
