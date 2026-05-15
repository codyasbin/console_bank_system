# Console Bank System

Console-based banking application implemented in Python.

## Features
- Create accounts (in-memory):
  - **SavingsAccount**
  - **CheckingAccount**
  - **Generic Account**
- Deposit money
- Withdraw money
- Check account balance
- View transaction history per account
- View all created accounts

## Account Types & Rules

### 1) Generic Account
- Supports `deposit(amount)` and `withdraw(amount)`.
- Validations:
  - Deposit/withdraw amount must be **> 0**.

### 2) Savings Account
- Parameters:
  - `interest_rate` (default: `0.02`)
  - `minimum_balance` (default: `100.0`)
- Rules:
  - Initial balance must be **>= minimum_balance**.
  - Withdrawals are allowed only if the **remaining balance** stays **>= minimum_balance**.
- Note: Interest application is implemented (`apply_interest`) but is not currently exposed in the console menu.

### 3) Checking Account
- Parameters:
  - `transaction_fee` (default: `1.0`)
- Rules:
  - On withdrawal, the fee is included in the total debited amount: `total = amount + transaction_fee`.

## Error Handling
The application raises and catches these domain exceptions:
- `InvalidAmountError`: amount is missing, non-numeric, or **<= 0**
- `InsufficientBalanceError`: withdrawal would overdraw (or violate Savings minimum balance)
- `AccountNotFoundError`: requested account number does not exist

## How to Run
From the project root:

```bash
python main.py
```

## Console Menu
After starting, choose an option:
1. **Create Account**
2. **Deposit Money**
3. **Withdraw Money**
4. **Check Balance**
5. **View Transaction History**
6. **View All Accounts**
7. **Exit**

## Project Structure
- `main.py` — entry point (calls `banking.ui.main()`)
- `banking/`
  - `ui.py` — console user interface + input helpers
  - `bank.py` — `Bank` class managing accounts
  - `accounts.py` — `Account`, `SavingsAccount`, `CheckingAccount`
  - `exceptions.py` — custom exception types
  - `__init__.py` — package marker

## Notes
- Accounts and transaction history are stored **in memory** and will be lost when the program exits.

