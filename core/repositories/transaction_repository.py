
from datetime import date
import calendar
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from core.repositories.base_repository import BaseRepository
from database.models import Transaction
from database.session import Session

class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self, session_factory=Session):
        super().__init__(Transaction, session_factory)

    def get_transactions_for_period(
        self,
        date_from: date,
        date_to: date,
        category: Optional[str] = None,
        description_contains: Optional[str] = None
    ) -> List[Transaction]:
        with self._session_factory() as session:
            q = session.query(Transaction).options(joinedload(Transaction.account)) \
                     .filter(Transaction.date >= date_from) \
                     .filter(Transaction.date <= date_to)

            if category and category != "Wszystkie":
                q = q.filter(Transaction.category == category)

            if description_contains:
                q = q.filter(Transaction.description.ilike(f"%{description_contains}%"))

            return q.order_by(Transaction.date.desc()).all()

    def get_transactions_up_to_date(self, target: date) -> List[Transaction]:
        with self._session_factory() as session:
            return (
                session.query(Transaction)
                       .options(joinedload(Transaction.account))
                       .filter(Transaction.date <= target)
                       .order_by(Transaction.date.asc())
                       .all()
            )

    def get_recent_transactions(self, limit: int = 7) -> List[Transaction]:
        with self._session_factory() as session:
            return (
                session.query(Transaction)
                       .options(joinedload(Transaction.account))
                       .order_by(Transaction.date.desc())
                       .limit(limit)
                       .all()
            )

    def get_transactions_for_month(self, year: int, month: int) -> List[Transaction]:
        first = date(year, month, 1)
        last_day = calendar.monthrange(year, month)[1]
        last = date(year, month, last_day)

        with self._session_factory() as session:
            return (
                session.query(Transaction)
                       .options(joinedload(Transaction.account))
                       .filter(Transaction.date >= first)
                       .filter(Transaction.date <= last)
                       .order_by(Transaction.date.desc())
                       .all()
            )

    def create(self, data: dict) -> int:
        with self._session_factory() as session:
            t = Transaction(**data)
            session.add(t)
            session.commit()
            return t.id

    def update(self, tx_id: int, data: dict) -> None:
        with self._session_factory() as session:
            t = session.get(Transaction, tx_id)
            if not t:
                return
            for k, v in data.items():
                setattr(t, k, v)
            session.commit()
