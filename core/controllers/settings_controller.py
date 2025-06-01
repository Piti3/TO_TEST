# core/controllers/settings_controller.py

import hashlib
from typing import Optional
from core.repositories.settings_repository import SettingsRepository

class SettingsController:
    """
    Kontroler do operacji konfiguracyjnych, m.in. zarządzania hasłem aplikacji.
    """
    def __init__(self, repo: SettingsRepository = None):
        self.repo = repo or SettingsRepository()
        self.PASSWORD_KEY = "password_hash"

    def has_password(self) -> bool:
        """
        Sprawdza, czy w bazie już zapisano hash hasła.
        """
        existing = self.repo.get_value(self.PASSWORD_KEY)
        return existing is not None and existing != ""

    def check_password(self, plain_password: str) -> bool:
        """
        Porównuje hash podanego hasła z tym zapisanym w bazie.
        Zwraca True, jeśli pasuje, False w przeciwnym razie.
        """
        stored_hash = self.repo.get_value(self.PASSWORD_KEY)
        if not stored_hash:
            return False
        hashed = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
        return hashed == stored_hash

    def set_password(self, new_plain_password: str):
        """
        Ustawia (lub zmienia) hasło aplikacji – zapisuje hash w bazie.
        """
        hashed = hashlib.sha256(new_plain_password.encode("utf-8")).hexdigest()
        self.repo.set_value(self.PASSWORD_KEY, hashed)

    def remove_password(self):
        """
        (Opcjonalnie) – usuwa hasło, pozostawiając puste miejsce.
        """
        self.repo.set_value(self.PASSWORD_KEY, "")
