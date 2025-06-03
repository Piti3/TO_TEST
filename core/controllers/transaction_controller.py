
from datetime import date
import calendar
from typing import List
from database.models import Transaction
from database.session import Session
from sqlalchemy.orm import joinedload

class TransactionController:
    def __init__(self, session_factory=Session):
        self.session_factory = session_factory

    def get_transactions_up_to_date(self, target: date) -> List[Transaction]:
        with self.session_factory() as session:
            txs = (
                session.query(Transaction)
                       .options(joinedload(Transaction.account))
                       .filter(Transaction.date <= target)
                       .order_by(Transaction.date.asc())
                       .all()
            )
        return txs

    def get_recent_transactions(self, limit: int = 7) -> List[Transaction]:
        with self.session_factory() as session:
            txs = (
                session.query(Transaction)
                       .options(joinedload(Transaction.account))
                       .order_by(Transaction.date.desc())
                       .limit(limit)
                       .all()
            )
        return txs

    def get_transactions_for_month(self, year: int, month: int) -> List[Transaction]:
        first = date(year, month, 1)
        last_day = calendar.monthrange(year, month)[1]
        last = date(year, month, last_day)

        with self.session_factory() as session:
            txs = (
                session.query(Transaction)
                    .options(joinedload(Transaction.account))
                    .filter(Transaction.date >= first)
                    .filter(Transaction.date <= last)
                    .order_by(Transaction.date.desc())
                    .all()
            )
        return txs

    def create_transaction(self, data: dict) -> int:
        with self.session_factory() as session:
            t = Transaction(**data)
            session.add(t)
            session.commit()
            return t.id

    def update_transaction(self, tx_id: int, data: dict):
        with self.session_factory() as session:
            tx = session.query(Transaction).get(tx_id)
            if not tx:
                return
            for k, v in data.items():
                setattr(tx, k, v)
            session.commit()

    def delete_transaction(self, tx_id: int):

        with self.session_factory() as session:
            tx = session.query(Transaction).get(tx_id)
            if tx:
                session.delete(tx)
                session.commit()
