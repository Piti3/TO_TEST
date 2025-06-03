from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class PlannedTransaction(Base):
    __tablename__ = 'planned_transactions'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="PLN")
    category = Column(String)
    description = Column(String)
    frequency = Column(String, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
   
    account = relationship('Account')