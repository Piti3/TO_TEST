from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base

import database.models 
import database.models.account
import database.models.transaction
import database.models.planned_transaction

engine = create_engine('sqlite:///finanse.db', echo=False)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)