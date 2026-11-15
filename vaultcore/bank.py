"""Banking rules for the VaultCore console project."""

from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import List, Optional

from .models import Account, Transaction
from .storage import CsvStorage


MONEY_PLACES = Decimal("0.01")


class BankError(ValueError):
    """A message that can be safely shown to the console user."""


def as_money(value: object) -> Decimal:
    """Convert a value to a positive-money-friendly Decimal."""
    try:
        amount = Decimal(str(value)).quantize(MONEY_PLACES, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        raise BankError("Enter a valid amount.") from None
    return amount


class Bank:
    """Manage accounts, balances, statements, and CSV persistence."""

    def __init__(self, storage: CsvStorage) -> None:
        self.storage = storage
        self.accounts, self.transactions = storage.load()

    def open_account(
        self,
        holder_name: str,
        phone: str,
        account_type: str,
        opening_balance: object = "0",
    ) -> Account:
        name = holder_name.strip()
        clean_phone = phone.strip()
        kind = account_type.strip().title()
        amount = as_money(opening_balance)

        if len(name) < 2 or not all(part.replace("-", "").isalpha() for part in name.split()):
            raise BankError("Name must contain at least two alphabetic characters.")
        if not (clean_phone.isdigit() and len(clean_phone) == 10):
            raise BankError("Phone number must contain exactly 10 digits.")
        if kind not in {"Savings", "Current"}:
            raise BankError("Account type must be Savings or Current.")
        if amount < 0:
            raise BankError("Opening balance cannot be negative.")

        account = Account(
            account_number=self._next_account_number(),
            holder_name=name.title(),
            phone=clean_phone,
            account_type=kind,
            balance=amount,
        )
        self.accounts.append(account)
        self._record(account, "OPEN", amount, "Account opened")
        self._save()
        return account

    def deposit(self, account_number: str, amount: object) -> Account:
        account = self.get_active_account(account_number)
        money = as_money(amount)
        if money <= 0:
            raise BankError("Deposit amount must be greater than zero.")
        account.balance += money
        self._record(account, "DEPOSIT", money)
        self._save()
        return account

    def withdraw(self, account_number: str, amount: object) -> Account:
        account = self.get_active_account(account_number)
        money = as_money(amount)
        if money <= 0:
            raise BankError("Withdrawal amount must be greater than zero.")
        if money > account.balance:
            raise BankError("Insufficient balance.")
        account.balance -= money
        self._record(account, "WITHDRAWAL", money)
        self._save()
        return account

    def mini_statement(self, account_number: str, limit: int = 5) -> List[Transaction]:
        self.get_active_account(account_number)
        matches = [
            item for item in self.transactions if item.account_number == account_number.strip().upper()
        ]
        return matches[-limit:]

    def search(self, search_text: str, include_closed: bool = False) -> List[Account]:
        term = search_text.strip().lower()
        if not term:
            raise BankError("Enter an account number or holder name to search.")
        return [
            account
            for account in self.accounts
            if (include_closed or account.is_active)
            and (term in account.account_number.lower() or term in account.holder_name.lower())
        ]

    def close_account(self, account_number: str) -> Account:
        account = self.get_active_account(account_number)
        if account.balance != Decimal("0.00"):
            raise BankError("Withdraw the full balance before closing the account.")
        account.is_active = False
        self._record(account, "CLOSE", Decimal("0.00"), "Account closed")
        self._save()
        return account

    def apply_monthly_interest(self, account_number: str, annual_rate: object) -> Decimal:
        account = self.get_active_account(account_number)
        if account.account_type != "Savings":
            raise BankError("Monthly interest is available only for Savings accounts.")
        rate = as_money(annual_rate)
        if rate <= 0 or rate > 100:
            raise BankError("Annual interest rate must be above 0 and at most 100.")
        interest = (account.balance * rate / Decimal("1200")).quantize(
            MONEY_PLACES, rounding=ROUND_HALF_UP
        )
        account.balance += interest
        self._record(account, "INTEREST", interest, f"Annual rate {rate}%")
        self._save()
        return interest

    def get_active_account(self, account_number: str) -> Account:
        number = account_number.strip().upper()
        for account in self.accounts:
            if account.account_number == number:
                if not account.is_active:
                    raise BankError("This account is closed.")
                return account
        raise BankError("Account not found.")

    def _next_account_number(self) -> str:
        highest = 1000
        for account in self.accounts:
            if account.account_number.startswith("VA"):
                try:
                    highest = max(highest, int(account.account_number[2:]))
                except ValueError:
                    pass
        return f"VA{highest + 1}"

    def _record(
        self,
        account: Account,
        transaction_type: str,
        amount: Decimal,
        note: str = "",
    ) -> None:
        self.transactions.append(
            Transaction(
                timestamp=datetime.now().isoformat(timespec="seconds"),
                account_number=account.account_number,
                transaction_type=transaction_type,
                amount=amount,
                balance_after=account.balance,
                note=note,
            )
        )

    def _save(self) -> None:
        self.storage.save(self.accounts, self.transactions)
