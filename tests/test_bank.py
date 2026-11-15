import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from vaultcore.bank import Bank, BankError
from vaultcore.storage import CsvStorage


class BankTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_folder = tempfile.TemporaryDirectory()
        self.bank = Bank(CsvStorage(Path(self.temp_folder.name)))

    def tearDown(self) -> None:
        self.temp_folder.cleanup()

    def open_savings(self, balance: str = "1000"):
        return self.bank.open_account("Asha Rao", "9876543210", "savings", balance)

    def test_open_account_assigns_number_and_formats_data(self):
        account = self.open_savings()
        self.assertEqual(account.account_number, "VA1001")
        self.assertEqual(account.holder_name, "Asha Rao")
        self.assertEqual(account.balance, Decimal("1000.00"))

    def test_account_numbers_increase(self):
        first = self.open_savings()
        second = self.bank.open_account("Ravi Kumar", "9123456780", "current", "0")
        self.assertEqual((first.account_number, second.account_number), ("VA1001", "VA1002"))

    def test_open_account_rejects_bad_phone(self):
        with self.assertRaisesRegex(BankError, "10 digits"):
            self.bank.open_account("Asha Rao", "123", "Savings", "0")

    def test_open_account_rejects_unknown_type(self):
        with self.assertRaisesRegex(BankError, "Savings or Current"):
            self.bank.open_account("Asha Rao", "9876543210", "Fixed", "0")

    def test_open_account_rejects_negative_balance(self):
        with self.assertRaisesRegex(BankError, "cannot be negative"):
            self.bank.open_account("Asha Rao", "9876543210", "Savings", "-1")

    def test_deposit_updates_balance(self):
        account = self.open_savings()
        self.bank.deposit(account.account_number, "250.505")
        self.assertEqual(account.balance, Decimal("1250.51"))

    def test_deposit_rejects_zero(self):
        account = self.open_savings()
        with self.assertRaisesRegex(BankError, "greater than zero"):
            self.bank.deposit(account.account_number, "0")

    def test_withdraw_updates_balance(self):
        account = self.open_savings()
        self.bank.withdraw(account.account_number, "400")
        self.assertEqual(account.balance, Decimal("600.00"))

    def test_withdraw_rejects_insufficient_balance(self):
        account = self.open_savings()
        with self.assertRaisesRegex(BankError, "Insufficient"):
            self.bank.withdraw(account.account_number, "1000.01")

    def test_mini_statement_returns_last_five(self):
        account = self.open_savings()
        for _ in range(6):
            self.bank.deposit(account.account_number, "1")
        statement = self.bank.mini_statement(account.account_number)
        self.assertEqual(len(statement), 5)
        self.assertTrue(all(item.transaction_type == "DEPOSIT" for item in statement))

    def test_search_by_partial_name_and_number(self):
        account = self.open_savings()
        self.assertEqual(self.bank.search("asha"), [account])
        self.assertEqual(self.bank.search("1001"), [account])

    def test_close_requires_zero_balance(self):
        account = self.open_savings()
        with self.assertRaisesRegex(BankError, "full balance"):
            self.bank.close_account(account.account_number)

    def test_close_zero_balance_account(self):
        account = self.open_savings("0")
        self.bank.close_account(account.account_number)
        self.assertFalse(account.is_active)
        with self.assertRaisesRegex(BankError, "closed"):
            self.bank.deposit(account.account_number, "10")

    def test_interest_on_savings(self):
        account = self.open_savings("12000")
        interest = self.bank.apply_monthly_interest(account.account_number, "6")
        self.assertEqual(interest, Decimal("60.00"))
        self.assertEqual(account.balance, Decimal("12060.00"))

    def test_interest_rejects_current_account(self):
        account = self.bank.open_account("Ravi Kumar", "9123456780", "Current", "1000")
        with self.assertRaisesRegex(BankError, "Savings"):
            self.bank.apply_monthly_interest(account.account_number, "6")

    def test_data_survives_reload(self):
        account = self.open_savings()
        self.bank.deposit(account.account_number, "50")
        reloaded = Bank(self.bank.storage)
        same_account = reloaded.get_active_account(account.account_number)
        self.assertEqual(same_account.balance, Decimal("1050.00"))
        self.assertEqual(len(reloaded.transactions), 2)


if __name__ == "__main__":
    unittest.main()
