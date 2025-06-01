# core/repositories/settings_repository.py

from database.models.app_config import AppConfig
from database.session import Session

class SettingsRepository:
    """
    Repozytorium do odczytu i zapisu kluczy konfiguracyjnych w tabeli app_config.
    Klucze to proste stringi, np. 'password_hash', 'some_other_setting' itp.
    """
    def __init__(self, session_factory=Session):
        self.session_factory = session_factory

    def get_value(self, key: str):
        """
        Zwraca wartość (string) dla danego klucza. Jeśli nie istnieje, zwraca None.
        """
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
        """
        Ustawia (insert lub update) wartość w tabeli app_config dla danego klucza.
        """
        with self.session_factory() as session:
            row = session.query(AppConfig).filter(AppConfig.key == key).first()
            if row:
                row.value = value
            else:
                row = AppConfig(key=key, value=value)
                session.add(row)
            session.commit()
