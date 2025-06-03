from database.session import Session
from sqlalchemy.orm import joinedload
from sqlalchemy import distinct
from database.models.planned_transaction import PlannedTransaction

class PlannedTransactionController:
    def __init__(self, session_factory=Session):
        self.session_factory = session_factory

    def list_for_date(self, date):
        with self.session_factory() as session:
            pts = (
                session
                .query(PlannedTransaction)
                .options(joinedload(PlannedTransaction.account))
                .filter_by(date=date)
                .all()
            )
            return pts

    def create(self, data):
        with self.session_factory() as session:
            pt = PlannedTransaction(**data)
            session.add(pt)
            session.commit()
            return pt.id

    def update(self, pt_id, data):
        with self.session_factory() as session:
            pt = session.get(PlannedTransaction, pt_id)
            for k, v in data.items(): setattr(pt, k, v)
            session.commit()

    def delete(self, pt_id):
        with self.session_factory() as session:
            pt = session.get(PlannedTransaction, pt_id)
            session.delete(pt)
            session.commit()

    def get_all_dates(self):
        """Zwraca listę wszystkich dat, dla których co najmniej jedna transakcja jest zaplanowana."""
        with self.session_factory() as session:
            rows = session.query(distinct(PlannedTransaction.date)).all()
            return [r[0] for r in rows]