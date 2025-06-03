
from sqlalchemy import Column, Integer, String, Float, SmallInteger
from database.base import Base

class Budget(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    year = Column(SmallInteger, nullable=False)
    month = Column(SmallInteger, nullable=False)
    limit_amount = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Budget(category={self.category}, {self.month}/{self.year}, limit={self.limit_amount})>"
