"""Console-Based Banking Application

Features:
- Menu driven console UI
- Multiple account support via Bank class
- OOP: Account base class + SavingsAccount/CheckingAccount inheritance
- Encapsulation: sensitive fields are private
- Transaction history per account
- Robust error handling and input validation

Run:
    python main.py
"""

from __future__ import annotations


class InsufficientBalanceError(Exception):
    pass


class InvalidAmountError(Exception):
    pass


class AccountNotFoundError(Exception):
    pass


class Account:
    """Base class representing a bank account."""

    def __init__(self, name: str, account_number: int, initial_balance: float):
        self._name = name
        self._account_number = int(account_number)
        self.__balance = 0.0  # encapsulated
        self._transactions: list[str] = []

        # Use validation for initial deposit
        self.deposit(initial_balance, record_action=True)
        # deposit() appends transaction; we want it clearly marked
        if initial_balance > 0:
            # Keep deposit transaction already recorded; otherwise no transaction.
            pass
        elif initial_balance == 0:
            # No transaction for zero initial balance.
            pass
        else:
            # Shouldn't happen due to validation in deposit.
            pass

    @property
    def name(self) -> str:
        return self._name

    @property
    def account_number(self) -> int:
        return self._account_number

    def get_balance(self) -> float:
        """Read-only balance accessor."""
        return self.__balance

    def _add_transaction(self, message: str) -> None:
        self._transactions.append(message)

    def deposit(self, amount: float, *, record_action: bool = True) -> None:
        """Deposit money into the account."""
        if amount is None or isinstance(amount, bool):
            raise InvalidAmountError("Invalid amount")
        try:
            amt = float(amount)
        except (TypeError, ValueError):
            raise InvalidAmountError("Invalid amount")

        if amt <= 0:
            raise InvalidAmountError("Deposit amount must be greater than 0")

        old = self.__balance
        self.__balance = old + amt

        if record_action:
            self._add_transaction(f"Deposited: {amt} | Balance: {old} -> {self.__balance}")

    def withdraw(self, amount: float, *, record_action: bool = True) -> None:
        """Withdraw money from the account."""
        if amount is None or isinstance(amount, bool):
            raise InvalidAmountError("Invalid amount")
        try:
            amt = float(amount)
        except (TypeError, ValueError):
            raise InvalidAmountError("Invalid amount")

        if amt <= 0:
            raise InvalidAmountError("Withdraw amount must be greater than 0")

        if amt > self.__balance:
            raise InsufficientBalanceError(
                f"Insufficient balance. Available: {self.__balance}, Requested: {amt}"
            )

        old = self.__balance
        self.__balance = old - amt

        if record_action:
            self._add_transaction(f"Withdrawn: {amt} | Balance: {old} -> {self.__balance}")

    def check_balance(self) -> float:
        return self.__balance

    def show_transactions(self) -> None:
        if not self._transactions:
            print("No transactions yet.")
            return
        print("--- Transaction History ---")
        for i, t in enumerate(self._transactions, start=1):
            print(f"{i}. {t}")


class SavingsAccount(Account):
    """Savings account with interest and minimum balance rule."""

    def __init__(
        self,
        name: str,
        account_number: int,
        initial_balance: float,
        *,
        interest_rate: float = 0.02,
        minimum_balance: float = 100.0,
    ):
        self._interest_rate = float(interest_rate)
        self._minimum_balance = float(minimum_balance)
        super().__init__(name, account_number, initial_balance)

        # Ensure minimum balance constraint (if initial deposit is below minimum, treat as invalid)
        if self.get_balance() < self._minimum_balance:
            raise InvalidAmountError(
                f"Initial balance must be at least {self._minimum_balance} for SavingsAccount"
            )

    def apply_interest(self) -> None:
        bal = self.get_balance()
        if bal <= 0:
            return
        earned = bal * self._interest_rate
        # deposit() will validate > 0
        if earned > 0:
            old = self.get_balance()
            super().deposit(earned, record_action=False)
            self._add_transaction(
                f"Interest applied: {earned} | Balance: {old} -> {self.get_balance()}"
            )

    def withdraw(self, amount: float, *, record_action: bool = True) -> None:
        # First validate base withdraw amount > 0
        try:
            amt = float(amount)
        except (TypeError, ValueError):
            raise InvalidAmountError("Invalid amount")

        if amt <= 0:
            raise InvalidAmountError("Withdraw amount must be greater than 0")

        if amt > self.get_balance():
            raise InsufficientBalanceError(
                f"Insufficient balance. Available: {self.get_balance()}, Requested: {amt}"
            )

        remaining = self.get_balance() - amt
        if remaining < self._minimum_balance:
            raise InsufficientBalanceError(
                f"Minimum balance rule: minimum is {self._minimum_balance}. "
                f"Remaining would be {remaining}"
            )

        # Use base withdraw once constraints pass
        super().withdraw(amt, record_action=record_action)


class CheckingAccount(Account):
    """Checking account with per-withdrawal fee."""

    def __init__(
        self,
        name: str,
        account_number: int,
        initial_balance: float,
        *,
        transaction_fee: float = 1.0,
    ):
        self._transaction_fee = float(transaction_fee)
        super().__init__(name, account_number, initial_balance)

    def withdraw(self, amount: float, *, record_action: bool = True) -> None:
        try:
            amt = float(amount)
        except (TypeError, ValueError):
            raise InvalidAmountError("Invalid amount")

        if amt <= 0:
            raise InvalidAmountError("Withdraw amount must be greater than 0")

        total = amt + self._transaction_fee
        if total > self.get_balance():
            raise InsufficientBalanceError(
                f"Insufficient balance (including fee). Available: {self.get_balance()}, Requested+Fee: {total}"
            )

        old = self.get_balance()
        # Withdraw total and record as two lines
        # We can't call super().withdraw(amt) because fee is extra.
        # Implement safely with encapsulation via base private isn't accessible, so call base withdraw with total.
        # But base withdraw subtracts amount; we want subtract total.
        super().withdraw(total, record_action=False)

        if record_action:
            self._add_transaction(
                f"Withdrawn: {amt} | Fee: {self._transaction_fee} | Balance: {old} -> {self.get_balance()}"
            )


class Bank:
    """Represents a bank containing multiple accounts."""

    def __init__(self):
        self.accounts: dict[int, Account] = {}

    def create_account(
        self,
        account_type: str,
        name: str,
        account_number: int,
        initial_balance: float,
        **kwargs,
    ) -> Account:
        acct_no = int(account_number)
        if acct_no in self.accounts:
            raise ValueError(f"Account number {acct_no} already exists")

        account_type = account_type.strip().lower()
        if account_type == "savings":
            account = SavingsAccount(
                name, acct_no, initial_balance, **kwargs
            )
        elif account_type == "checking":
            account = CheckingAccount(
                name, acct_no, initial_balance, **kwargs
            )
        elif account_type == "account":
            account = Account(name, acct_no, initial_balance)
        else:
            raise ValueError("Unknown account type")

        self.accounts[acct_no] = account
        return account

    def find_account(self, account_number: int) -> Account:
        acct_no = int(account_number)
        if acct_no not in self.accounts:
            raise AccountNotFoundError(f"Account number {acct_no} not found")
        return self.accounts[acct_no]

    def show_all_accounts(self) -> None:
        if not self.accounts:
            print("No accounts available.")
            return
        print("--- All Accounts ---")
        for acct_no in sorted(self.accounts.keys()):
            a = self.accounts[acct_no]
            print(
                f"Account No: {a.account_number} | Name: {a.name} | Balance: {a.check_balance()}"
            )


# ---------------- Console UI helpers ----------------

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
                print(f"Transactions for Account No: {a.account_number} (Name: {a.name})")
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


if __name__ == "__main__":
    main()

