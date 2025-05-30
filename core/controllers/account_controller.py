from typing import List, Optional
from core.repositories.account_repository import AccountRepository
from database.models import Account

class AccountsController:
    def __init__(self, repo: AccountRepository = None):
        self.repo = repo or AccountRepository()

    def list_accounts(self) -> List[Account]:
        for acc in self.repo.get_all_accounts():
            self.repo.update_account_balance_from_transactions(acc.id)
        return self.repo.get_all_accounts()

    def get_account(self, account_id: int) -> Optional[Account]:
        return self.repo.get_account_by_id(account_id)

    def create_account(self, name: str, balance: float, type: str = "Normalny"):
        self.repo.add_account(name, balance, type)

    def update_account(self, account_id: int, name: str, balance: float, type: str):
        self.repo.update_account(account_id, name, balance, type)

    def delete_account(self, account_id: int):
        self.repo.delete_account(account_id)

    def change_balance(self, account_id: int, delta: float):
        self.repo.change_balance(account_id, delta)

