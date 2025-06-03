
from sqlalchemy import Column, Integer, String
from database.base import Base

class AppConfig(Base):
    __tablename__ = 'app_config'

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=True)

    def __repr__(self):
        return f"<AppConfig(key={self.key}, value={self.value})>"
