from typing import List, Optional
from core.repositories.budget_repository import BudgetRepository
from database.models.budget import Budget
from database.models.transaction import Transaction
from database.session import Session
from datetime import date

class BudgetController:
    """
    Controller odpowiedzialny za operacje na budżetach (tworzenie, aktualizacja, usuwanie)
    oraz pomocniczo: sprawdzanie stanu wydatków w danym miesiącu vs. limit.
    """
    def __init__(self, repo: BudgetRepository = None, session_factory=Session):
        self.repo = repo or BudgetRepository(session_factory)
        self.session_factory = session_factory

    def list_all_budgets(self) -> List[Budget]:
        return self.repo.get_all_budgets()

    def get_budget_by_id(self, budget_id: int) -> Optional[Budget]:
        return self.repo.get_budget(budget_id)

    def get_budgets_for_month(self, year: int, month: int) -> List[Budget]:
        return self.repo.get_budgets_for_month(year, month)

    def create_budget(self, data: dict) -> int:
        """
        `data` to dict z polami: 'category', 'year', 'month', 'limit_amount'
        """
        return self.repo.add_budget(
            data['category'], data['year'], data['month'], data['limit_amount']
        )

    def update_budget(self, budget_id: int, data: dict) -> None:
        self.repo.update_budget(
            budget_id,
            data['category'], data['year'], data['month'], data['limit_amount']
        )

    def delete_budget(self, budget_id: int) -> None:
        self.repo.delete_budget(budget_id)

    def get_budget_for_category_month(self, category: str, year: int, month: int) -> Optional[Budget]:
        return self.repo.find_budget_for_category_month(category, year, month)

    def current_month_spent_for_category(self, category: str, year: int, month: int) -> float:
        """
        Zwraca sumę wydatków (Transaction.type == 'Wydatek') dla danej kategorii w zadanym roku/miesiącu.
        """
        with self.session_factory() as session:
            total = (
                session
                .query(Transaction)
                .filter(
                    Transaction.type == "Wydatek",
                    Transaction.category == category,
                    Transaction.date >= date(year, month, 1),
                    Transaction.date < (date(year + (month // 12), ((month % 12) + 1), 1))
                )
                .all()
            )
            return sum(t.amount for t in total)
