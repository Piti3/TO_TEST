# database/models/budget.py

from sqlalchemy import Column, Integer, String, Float, SmallInteger
from database.base import Base

class Budget(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True)
    # nazwa kategorii, do której odnosi się ten budżet
    category = Column(String, nullable=False)
    # rok (np. 2025)
    year = Column(SmallInteger, nullable=False)
    # miesiąc (1–12)
    month = Column(SmallInteger, nullable=False)
    # limit budżetowy (kwota max wydatków w tej kategorii w danym roku/miesiącu)
    limit_amount = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Budget(category={self.category}, {self.month}/{self.year}, limit={self.limit_amount})>"
