"""Text menu and input/output for VaultCore."""

from decimal import Decimal
from typing import Callable

from .bank import Bank, BankError
from .models import Account


def money(value: Decimal) -> str:
    return f"Rs. {value:,.2f}"


def show_account(account: Account, output: Callable[[str], None] = print) -> None:
    status = "Active" if account.is_active else "Closed"
    output(
        f"{account.account_number} | {account.holder_name} | "
        f"{account.account_type} | {money(account.balance)} | {status}"
    )


def run_console(
    bank: Bank,
    input_fn: Callable[[str], str] = input,
    output: Callable[[str], None] = print,
) -> None:
    menu = """
================ VAULTCORE ================
1. Open account
2. Deposit money
3. Withdraw money
4. Mini statement
5. Search account
6. Close account
0. Exit
===========================================
"""

    while True:
        output(menu)
        choice = input_fn("Choose an option: ").strip()
        try:
            if choice == "1":
                account = bank.open_account(
                    input_fn("Holder name: "),
                    input_fn("10-digit phone number: "),
                    input_fn("Account type (Savings/Current): "),
                    input_fn("Opening balance: "),
                )
                output(f"Account opened successfully. Number: {account.account_number}")
            elif choice == "2":
                account = bank.deposit(
                    input_fn("Account number: "), input_fn("Deposit amount: ")
                )
                output(f"Deposit successful. New balance: {money(account.balance)}")
            elif choice == "3":
                account = bank.withdraw(
                    input_fn("Account number: "), input_fn("Withdrawal amount: ")
                )
                output(f"Withdrawal successful. New balance: {money(account.balance)}")
            elif choice == "4":
                number = input_fn("Account number: ").strip().upper()
                account = bank.get_active_account(number)
                output(f"Mini statement for {account.holder_name} ({number})")
                output("Date and time         | Type       | Amount       | Balance")
                for item in bank.mini_statement(number):
                    stamp = item.timestamp.replace("T", " ")
                    output(
                        f"{stamp:19} | {item.transaction_type:10} | "
                        f"{money(item.amount):12} | {money(item.balance_after)}"
                    )
            elif choice == "5":
                results = bank.search(input_fn("Account number or holder name: "))
                if results:
                    for account in results:
                        show_account(account, output)
                else:
                    output("No matching active account found.")
            elif choice == "6":
                account = bank.close_account(input_fn("Account number: "))
                output(f"Account {account.account_number} closed successfully.")
            elif choice == "7":
                number = input_fn("Savings account number: ")
                interest = bank.apply_monthly_interest(
                    number, input_fn("Annual interest rate (%): ")
                )
                balance = bank.get_active_account(number).balance
                output(f"Interest added: {money(interest)}. New balance: {money(balance)}")
            elif choice == "0":
                output("Thank you for using VaultCore.")
                return
            else:
                output("Invalid option. Choose a number from 0 to 7.")
        except BankError as error:
            output(f"Error: {error}")
