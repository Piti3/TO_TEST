from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base
import os

import database.models 

DB_PATH = os.path.join(os.path.dirname(__file__), os.pardir, "finanse.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)