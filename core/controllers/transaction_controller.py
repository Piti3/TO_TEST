
from datetime import date
from typing import List

from core.repositories.transaction_repository import TransactionRepository
from database.models import Transaction

class TransactionController:
    def __init__(self, repository: TransactionRepository = TransactionRepository()):
        self.repository = repository

    def get_transactions_up_to_date(self, target: date) -> List[Transaction]:
        return self.repository.get_transactions_up_to_date(target)

    def get_recent_transactions(self, limit: int = 7) -> List[Transaction]:
        return self.repository.get_recent_transactions(limit)

    def get_transactions_for_month(self, year: int, month: int) -> List[Transaction]:
        return self.repository.get_transactions_for_month(year, month)

    def create_transaction(self, data: dict) -> int:
        return self.repository.create(data)

    def update_transaction(self, tx_id: int, data: dict) -> None:
        self.repository.update(tx_id, data)

    def delete_transaction(self, tx_id: int) -> None:
        self.repository.delete(tx_id)