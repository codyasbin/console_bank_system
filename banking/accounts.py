from __future__ import annotations

from .exceptions import InsufficientBalanceError, InvalidAmountError


class Account:
    """Base class representing a bank account."""

    def __init__(self, name: str, account_number: int, initial_balance: float):
        self._name = name
        self._account_number = int(account_number)
        self.__balance = 0.0  # encapsulated
        self._transactions: list[str] = []

        # Use validation for initial deposit
        self.deposit(initial_balance, record_action=True)

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
            self._add_transaction(
                f"Deposited: {amt} | Balance: {old} -> {self.__balance}"
            )

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

        if earned > 0:
            old = self.get_balance()
            # deposit() will validate > 0; record_action=False so we control formatting.
            super().deposit(earned, record_action=False)
            self._add_transaction(
                f"Interest applied: {earned} | Balance: {old} -> {self.get_balance()}"
            )

    def withdraw(self, amount: float, *, record_action: bool = True) -> None:
        # Validate amount > 0
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

        # Base withdraw subtracts the provided amount; we use total and avoid duplicate transaction.
        super().withdraw(total, record_action=False)

        if record_action:
            self._add_transaction(
                f"Withdrawn: {amt} | Fee: {self._transaction_fee} | Balance: {old} -> {self.get_balance()}"
            )

