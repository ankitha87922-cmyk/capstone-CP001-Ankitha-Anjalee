# Problem Title: VaultCore

**Problem ID: CP001**

## Team Members

- Name: Anjalee | USN: 1AT24CS020
- Name: Ankitha M | USN: 1AT24CS021


## How to Run the Program

**Prerequisites:**

- Python 3.10 or newer installed.
- No external packages are required.

**Steps:**

1. Clone or download this repository.
2. Open the project folder in your terminal.
3. Navigate to the project directory:

   ```bash
   cd capstone-CP001-Anjalee-Ankitha
   ```

4. Run the program:

   ```bash
   python main.py
   ```

5. The program automatically creates and maintains the following CSV files for storing account and transaction details:

   - `data/accounts.csv`
   - `data/transactions.csv`

## Features Implemented

1. Open a Savings or Current bank account with an automatically generated account number.
2. Deposit and withdraw money with proper validation.
3. Display the latest five transactions as a mini statement.
4. Search active accounts using account number or account holder name.
5. Close a bank account only when its balance is zero.
6. Store and retrieve account and transaction details using CSV files.

## Sample Run

**Input:**

The user interacts with the program through a Python console menu to perform banking operations such as opening an account, depositing money, withdrawing money, searching for accounts, and viewing transaction history.

**Output:**

The program displays account details, updated balances, transaction history, and appropriate success or validation messages based on the user's selections.

## Testing

To execute the automated test cases, run:

```bash
python -m unittest discover -s tests -v
```

The test suite checks account operations, transaction handling, validations, and CSV storage functionality.

## Important Notes

- Monetary values are handled using `Decimal` to ensure accurate calculations.
- Withdrawals cannot exceed the available account balance.
- Closed accounts cannot be used for further transactions.
- An account must have a zero balance before closure.
- Account and transaction records are automatically saved and loaded using CSV files.