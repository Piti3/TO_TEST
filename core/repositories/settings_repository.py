
from database.models.app_config import AppConfig
from database.session import Session

class SettingsRepository:

    def __init__(self, session_factory=Session):
        self.session_factory = session_factory

    def get_value(self, key: str):
        with self.session_factory() as session:
            row = (
                session
                .query(AppConfig)
                .filter(AppConfig.key == key)
                .first()
            )
            if row:
                return row.value
            return None

    def set_value(self, key: str, value: str):
        with self.session_factory() as session:
            row = session.query(AppConfig).filter(AppConfig.key == key).first()
            if row:
                row.value = value
            else:
                row = AppConfig(key=key, value=value)
                session.add(row)
            session.commit()
