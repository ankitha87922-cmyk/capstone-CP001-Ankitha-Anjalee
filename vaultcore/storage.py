"""CSV file saving and loading for VaultCore."""

import csv
from decimal import Decimal
from pathlib import Path
from typing import Iterable, List, Tuple

from .models import Account, Transaction


class CsvStorage:
    """Store accounts and transactions in two easy-to-read CSV files."""

    ACCOUNT_FIELDS = [
        "account_number",
        "holder_name",
        "phone",
        "account_type",
        "balance",
        "is_active",
    ]
    TRANSACTION_FIELDS = [
        "timestamp",
        "account_number",
        "transaction_type",
        "amount",
        "balance_after",
        "note",
    ]

    def __init__(self, data_folder: Path) -> None:
        self.data_folder = Path(data_folder)
        self.accounts_file = self.data_folder / "accounts.csv"
        self.transactions_file = self.data_folder / "transactions.csv"
        self.data_folder.mkdir(parents=True, exist_ok=True)

    def load(self) -> Tuple[List[Account], List[Transaction]]:
        accounts: List[Account] = []
        transactions: List[Transaction] = []

        if self.accounts_file.exists():
            with self.accounts_file.open("r", newline="", encoding="utf-8") as file:
                for row in csv.DictReader(file):
                    accounts.append(
                        Account(
                            account_number=row["account_number"],
                            holder_name=row["holder_name"],
                            phone=row["phone"],
                            account_type=row["account_type"],
                            balance=Decimal(row["balance"]),
                            is_active=row["is_active"].lower() == "true",
                        )
                    )

        if self.transactions_file.exists():
            with self.transactions_file.open("r", newline="", encoding="utf-8") as file:
                for row in csv.DictReader(file):
                    transactions.append(
                        Transaction(
                            timestamp=row["timestamp"],
                            account_number=row["account_number"],
                            transaction_type=row["transaction_type"],
                            amount=Decimal(row["amount"]),
                            balance_after=Decimal(row["balance_after"]),
                            note=row["note"],
                        )
                    )

        return accounts, transactions

    def save(
        self,
        accounts: Iterable[Account],
        transactions: Iterable[Transaction],
    ) -> None:
        self._save_accounts(accounts)
        self._save_transactions(transactions)

    def _save_accounts(self, accounts: Iterable[Account]) -> None:
        with self.accounts_file.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.ACCOUNT_FIELDS)
            writer.writeheader()
            for account in accounts:
                writer.writerow(
                    {
                        "account_number": account.account_number,
                        "holder_name": account.holder_name,
                        "phone": account.phone,
                        "account_type": account.account_type,
                        "balance": str(account.balance),
                        "is_active": str(account.is_active),
                    }
                )

    def _save_transactions(self, transactions: Iterable[Transaction]) -> None:
        with self.transactions_file.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.TRANSACTION_FIELDS)
            writer.writeheader()
            for transaction in transactions:
                writer.writerow(
                    {
                        "timestamp": transaction.timestamp,
                        "account_number": transaction.account_number,
                        "transaction_type": transaction.transaction_type,
                        "amount": str(transaction.amount),
                        "balance_after": str(transaction.balance_after),
                        "note": transaction.note,
                    }
                )
