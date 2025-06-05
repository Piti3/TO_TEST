
from typing import List, Optional
from database.models.budget import Budget
from database.session import Session
from database.models.transaction import Transaction
from datetime import date

class BudgetRepository:
    def __init__(self, session_factory=Session):
        self.session_factory = session_factory

    def get_all_budgets(self) -> List[Budget]:
        with self.session_factory() as session:
            return session.query(Budget).order_by(Budget.year.desc(), Budget.month.desc(), Budget.category).all()

    def get_budget(self, budget_id: int) -> Optional[Budget]:
        with self.session_factory() as session:
            return session.get(Budget, budget_id)

    def find_budget_for_category_month(self, category: str, year: int, month: int) -> Optional[Budget]:
        with self.session_factory() as session:
            return (
                session
                .query(Budget)
                .filter_by(category=category, year=year, month=month)
                .first()
            )

    def add_budget(self, category: str, year: int, month: int, limit_amount: float) -> int:
        with self.session_factory() as session:
            b = Budget(category=category, year=year, month=month, limit_amount=limit_amount)
            session.add(b)
            session.commit()
            return b.id

    def update_budget(self, budget_id: int, category: str, year: int, month: int, limit_amount: float) -> None:
        with self.session_factory() as session:
            b = session.get(Budget, budget_id)
            if b:
                b.category = category
                b.year = year
                b.month = month
                b.limit_amount = limit_amount
                session.commit()

    def delete_budget(self, budget_id: int) -> None:
        with self.session_factory() as session:
            b = session.get(Budget, budget_id)
            if b:
                session.delete(b)
                session.commit()

    def get_budgets_for_month(self, year: int, month: int) -> List[Budget]:
        with self.session_factory() as session:
            return (
                session
                .query(Budget)
                .filter_by(year=year, month=month)
                .order_by(Budget.category)
                .all()
            )
        
    def calculate_spent_for_category_month(self, category: str, year: int, month: int) -> float:
        start_date = date(year, month, 1)
        next_month = (month % 12) + 1
        next_year = year + (month // 12) if next_month == 1 else year
        end_date = date(next_year, next_month, 1)

        with self.session_factory() as session:
            transactions = (
                session.query(Transaction)
                       .filter(
                           Transaction.type == "Wydatek",
                           Transaction.category == category,
                           Transaction.date >= start_date,
                           Transaction.date < end_date
                       )
                       .all()
            )
            return sum(t.amount for t in transactions)
