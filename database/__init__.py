from .base import Base
from .session import Session
from .models import Account, Transaction

from .session import engine
Base.metadata.create_all(engine)
