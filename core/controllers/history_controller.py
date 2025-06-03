from datetime import date
from typing import List, Optional
from core.repositories.transaction_repository import TransactionRepository
from database.models import Transaction

class HistoryController:

    def __init__(self, repo: TransactionRepository = None):
        self.repo = repo or TransactionRepository()

    def fetch_transactions(
        self,
        date_from: date,
        date_to: date,
        category: Optional[str] = None,
        description_contains: Optional[str] = None
    ) -> List[Transaction]:
        return self.repo.get_transactions_for_period(date_from, date_to, category, description_contains)