from typing import List
from sqlalchemy.orm import joinedload
from database.session import Session
from database.models.account import Account
from database.models.transaction import Transaction


class ExportRepository:
    def fetch_accounts(self) -> List[Account]:
        with Session() as session:
            return session.query(Account).order_by(Account.id).all()

    def fetch_transactions(self) -> List[Transaction]:
        with Session() as session:
            return (
                session.query(Transaction)
                .options(joinedload(Transaction.account))
                .order_by(Transaction.date)
                .all()
            )
