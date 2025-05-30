from database.models import Account, Transaction
from database.session import Session
from datetime import date
from typing import List, Optional

class AccountRepository:
    def __init__(self, session_factory=Session):
        self.session_factory = session_factory

    def get_all_accounts(self):
        with self.session_factory() as session:
            return session.query(Account).all()
        
    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        with self.session_factory() as session:
            return session.query(Account).filter_by(id=account_id).first()

    def add_account(self, name, balance, type="Normalny"):
        with self.session_factory() as session:
            account = Account(name=name, balance=balance, type=type)
            session.add(account)
            session.commit()

    def update_account(self, account_id, name, balance, type):
        with self.session_factory() as session:
            account = session.query(Account).get(account_id)
            if account:
                account.name = name
                account.balance = balance
                account.type = type
                session.commit()

    def delete_account(self, account_id: int):
        with self.session_factory() as session:
            session.query(Transaction) \
                   .filter(Transaction.account_id == account_id) \
                   .delete(synchronize_session=False)

            session.query(Account) \
                   .filter(Account.id == account_id) \
                   .delete(synchronize_session=False)

            session.commit()

    def change_balance(self, account_id, delta):

        with self.session_factory() as session:
            account = session.query(Account).filter_by(id=account_id).first()
            if account:
                account.balance = (account.balance or 0) + delta
                session.commit()

    def update_account_balance_from_transactions(self, account_id):

        with self.session_factory() as session:
            account = session.query(Account).filter_by(id=account_id).first()
            if account:
                income = sum(t.amount for t in session.query(Transaction).filter_by(account_id=account_id, type="Przychód"))
                expense = sum(t.amount for t in session.query(Transaction).filter_by(account_id=account_id, type="Wydatek"))
                account.balance = income - expense
                session.commit()


    def get_transactions(
        self,
        date_from: date,
        date_to: date,
        category: Optional[str] = None,
        description_contains: Optional[str] = None
    ) -> List[Transaction]:

        with self.session_factory() as session:
            q = session.query(Transaction) \
                       .filter(Transaction.date >= date_from) \
                       .filter(Transaction.date <= date_to)

            if category and category != "Wszystkie":
                q = q.filter(Transaction.category == category)

            if description_contains:
                q = q.filter(Transaction.description.ilike(f"%{description_contains}%"))

            return q.order_by(Transaction.date.desc()).all()