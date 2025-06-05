from database.session import Session
from core.repositories.planned_transaction_repository import PlannedTransactionRepository


class PlannedTransactionController:
    def __init__(self, session_factory=Session):
        self.session_factory = session_factory
        self.repository = PlannedTransactionRepository(session_factory)

    def list_for_date(self, date):
        return self.repository.get_by_date(date)

    def create(self, data):
        return self.repository.create(data)

    def update(self, pt_id, data):
        self.repository.update(pt_id, data)

    def delete(self, pt_id):
        self.repository.delete(pt_id)

    def get_all_dates(self):
        return self.repository.get_all_distinct_dates()
