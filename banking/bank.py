from __future__ import annotations

from .accounts import Account, SavingsAccount, CheckingAccount
from .exceptions import AccountNotFoundError


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

