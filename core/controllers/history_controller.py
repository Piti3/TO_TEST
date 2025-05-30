from datetime import date
from typing import List, Optional
from core.repositories.account_repository import AccountRepository
from database.models import Transaction

class HistoryController:
    def __init__(self, repo: AccountRepository = None):
        self.repo = repo or AccountRepository()

    def fetch_transactions(
        self,
        date_from: date,
        date_to: date,
        category: Optional[str] = None,
        description_contains: Optional[str] = None
    ) -> List[Transaction]:
        return self.repo.get_transactions(
            date_from=date_from,
            date_to=date_to,
            category=category,
            description_contains=description_contains
        )