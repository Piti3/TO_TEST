from typing import List, Optional
from core.repositories.budget_repository import BudgetRepository
from database.models.budget import Budget

class BudgetController:
    def __init__(self, repo: BudgetRepository = None):
        self.repo = repo or BudgetRepository()

    def list_all_budgets(self) -> List[Budget]:
        return self.repo.get_all_budgets()

    def get_budget_by_id(self, budget_id: int) -> Optional[Budget]:
        return self.repo.get_budget(budget_id)

    def get_budgets_for_month(self, year: int, month: int) -> List[Budget]:
        return self.repo.get_budgets_for_month(year, month)

    def create_budget(self, data: dict) -> int:
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
        return self.repo.calculate_spent_for_category_month(category, year, month)
