
from typing import List, Optional
from sqlalchemy import func
from core.repositories.base_repository import BaseRepository
from database.models import Account, Transaction
from database.session import Session

class AccountRepository(BaseRepository[Account]):
    def __init__(self, session_factory=Session):
        super().__init__(Account, session_factory)

    def add_account(self, name: str, balance: float, type: str = "Normalny") -> None:
        with self._session_factory() as session:
            acc = Account(name=name, balance=balance, type=type)
            session.add(acc)
            session.commit()

    def update_account(self, account_id: int, name: str, balance: float, type: str) -> None:
        with self._session_factory() as session:
            acc = session.get(Account, account_id)
            if acc:
                acc.name = name
                acc.balance = balance
                acc.type = type
                session.commit()

    def change_balance(self, account_id: int, delta: float) -> None:
        with self._session_factory() as session:
            acc = session.query(Account).filter_by(id=account_id).first()
            if acc:
                acc.balance = (acc.balance or 0) + delta
                session.commit()

    def update_account_balance_from_transactions(self, account_id: int) -> None:
        with self._session_factory() as session:
            acc = session.query(Account).filter_by(id=account_id).first()
            if not acc:
                return

            # suma przychodów
            income = (
                session.query(func.coalesce(func.sum(Transaction.amount), 0.0))
                .filter(Transaction.account_id == account_id, Transaction.type == "Przychód")
                .scalar()
            )
            # suma wydatków
            expense = (
                session.query(func.coalesce(func.sum(Transaction.amount), 0.0))
                .filter(Transaction.account_id == account_id, Transaction.type == "Wydatek")
                .scalar()
            )
            acc.balance = income - expense
            session.commit()

    def delete_account(self, account_id: int) -> None:
        with self._session_factory() as session:
            session.query(Transaction).filter(Transaction.account_id == account_id).delete(synchronize_session=False)

            session.query(Account).filter(Account.id == account_id).delete(synchronize_session=False)
            session.commit()

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        with self._session_factory() as session:
            return session.query(Account).filter_by(id=account_id).first()

    def get_all_accounts(self) -> List[Account]:
        with self._session_factory() as session:
            return session.query(Account).all()
