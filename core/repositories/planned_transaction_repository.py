from sqlalchemy.orm import joinedload
from sqlalchemy import distinct
from database.models.planned_transaction import PlannedTransaction


class PlannedTransactionRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_by_date(self, date):
        with self.session_factory() as session:
            return (
                session.query(PlannedTransaction)
                .options(joinedload(PlannedTransaction.account))
                .filter(PlannedTransaction.date == date)
                .all()
            )

    def create(self, data):
        with self.session_factory() as session:
            pt = PlannedTransaction(**data)
            session.add(pt)
            session.commit()
            return pt.id

    def update(self, pt_id, data):
        with self.session_factory() as session:
            pt = session.get(PlannedTransaction, pt_id)
            if pt:
                for key, value in data.items():
                    setattr(pt, key, value)
                session.commit()

    def delete(self, pt_id):
        with self.session_factory() as session:
            pt = session.get(PlannedTransaction, pt_id)
            if pt:
                session.delete(pt)
                session.commit()

    def get_all_distinct_dates(self):
        with self.session_factory() as session:
            rows = session.query(distinct(PlannedTransaction.date)).all()
            return [r[0] for r in rows]
