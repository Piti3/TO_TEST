from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database.base import Base

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    type = Column(String, default="Normalny")  # np. gotówka, karta, bank

    transactions = relationship("Transaction", back_populates="account")

    def __repr__(self):
        return f"<Account(name={self.name}, balance={self.balance})>"
