import hashlib
from core.repositories.settings_repository import SettingsRepository


class SettingsController:
    PASSWORD_KEY = "password_hash"

    def __init__(self, repo: SettingsRepository = None):
        self.repo = repo or SettingsRepository()

    def has_password(self) -> bool:
        value = self.repo.get_value(self.PASSWORD_KEY)
        return bool(value and value.strip())

    def check_password(self, plain_password: str) -> bool:
        stored_hash = self.repo.get_value(self.PASSWORD_KEY)
        if not stored_hash:
            return False
        input_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
        return stored_hash == input_hash

    def set_password(self, new_plain_password: str):
        new_hash = hashlib.sha256(new_plain_password.encode("utf-8")).hexdigest()
        self.repo.set_value(self.PASSWORD_KEY, new_hash)

    def remove_password(self):
        self.repo.set_value(self.PASSWORD_KEY, "")
