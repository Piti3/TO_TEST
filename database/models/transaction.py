import datetime
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.date.today)
    type = Column(String, nullable=False)       # "Wydatek" lub "Przychód"
    amount = Column(Float, nullable=False)
    currency = Column(String, default="PLN")
    category = Column(String)
    description = Column(String)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)

    account = relationship('Account', back_populates='transactions')
