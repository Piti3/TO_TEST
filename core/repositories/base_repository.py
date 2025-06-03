
from typing import Generic, Type, TypeVar, List, Optional
from sqlalchemy.orm import Session as SASession

_T = TypeVar("_T")  

class BaseRepository(Generic[_T]):
    def __init__(self, model: Type[_T], session_factory):
        self._model = model
        self._session_factory = session_factory

    def get_all(self) -> List[_T]:
        with self._session_factory() as session: 
            return session.query(self._model).all()

    def get_by_id(self, obj_id: int) -> Optional[_T]:
        with self._session_factory() as session:
            return session.get(self._model, obj_id)

    def delete_by_id(self, obj_id: int) -> None:
        with self._session_factory() as session:
            obj = session.get(self._model, obj_id)
            if obj:
                session.delete(obj)
                session.commit()
