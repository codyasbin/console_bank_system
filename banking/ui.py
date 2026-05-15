from __future__ import annotations

from .bank import Bank
from .exceptions import AccountNotFoundError, InsufficientBalanceError, InvalidAmountError


def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Invalid input. Please enter an integer.")


def _read_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Invalid input. Please enter a number.")


def _read_non_empty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty.")


def main() -> None:
    bank = Bank()

    while True:
        print("\n====== BANK MENU ======")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. View Transaction History")
        print("6. View All Accounts")
        print("7. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            print("\n--- Create Account ---")
            name = _read_non_empty("Enter Name: ")
            account_number = _read_int("Enter Account Number: ")
            initial_balance = _read_float("Enter Initial Balance: ")

            print("Account Types: 1) Savings  2) Checking  3) Generic Account")
            t = input("Choose account type (1-3): ").strip()
            try:
                if t == "1":
                    interest_rate = _read_float("Enter Interest Rate (e.g., 0.02): ")
                    min_balance = _read_float("Enter Minimum Balance (e.g., 100): ")
                    bank.create_account(
                        "savings",
                        name,
                        account_number,
                        initial_balance,
                        interest_rate=interest_rate,
                        minimum_balance=min_balance,
                    )
                elif t == "2":
                    fee = _read_float("Enter Transaction Fee (e.g., 1.0): ")
                    bank.create_account(
                        "checking",
                        name,
                        account_number,
                        initial_balance,
                        transaction_fee=fee,
                    )
                elif t == "3":
                    bank.create_account("account", name, account_number, initial_balance)
                else:
                    print("Invalid account type selection.")
                    continue

                print("Account created successfully.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            print("\n--- Deposit Money ---")
            acct_no = _read_int("Enter Account Number: ")
            amount = _read_float("Deposit Amount: ")
            try:
                a = bank.find_account(acct_no)
                a.deposit(amount)
                print(f"Deposit successful. Current Balance: {a.check_balance()}")
            except (InvalidAmountError, InsufficientBalanceError, ValueError) as e:
                print(f"Error: {e}")
            except AccountNotFoundError as e:
                print(f"Error: {e}")

        elif choice == "3":
            print("\n--- Withdraw Money ---")
            acct_no = _read_int("Enter Account Number: ")
            amount = _read_float("Withdraw Amount: ")
            try:
                a = bank.find_account(acct_no)
                a.withdraw(amount)
                print(f"Withdrawal successful. Current Balance: {a.check_balance()}")
            except (InvalidAmountError, InsufficientBalanceError) as e:
                print(f"Error: {e}")
            except AccountNotFoundError as e:
                print(f"Error: {e}")

        elif choice == "4":
            print("\n--- Check Balance ---")
            acct_no = _read_int("Enter Account Number: ")
            try:
                a = bank.find_account(acct_no)
                print(f"Current Balance: {a.check_balance()}")
            except AccountNotFoundError as e:
                print(f"Error: {e}")

        elif choice == "5":
            print("\n--- Transaction History ---")
            acct_no = _read_int("Enter Account Number: ")
            try:
                a = bank.find_account(acct_no)
                print(
                    f"Transactions for Account No: {a.account_number} (Name: {a.name})"
                )
                a.show_transactions()
            except AccountNotFoundError as e:
                print(f"Error: {e}")

        elif choice == "6":
            print("\n--- View All Accounts ---")
            bank.show_all_accounts()

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please choose 1-7.")

