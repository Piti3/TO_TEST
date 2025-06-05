
from typing import List
from core.repositories.currency_repository import CurrencyRepository

class CurrencyController:
    def __init__(self, repo: CurrencyRepository = None):
        self.repo = repo or CurrencyRepository()
        self.repo.load_rates()

    def get_currencies(self) -> List[str]:
        return self.repo.list_currencies()

    def get_rate(self, code: str) -> float:
        return self.repo.get_rate(code)

    def convert(self, from_code: str, to_code: str, amount: float) -> float:
        rate_from = self.get_rate(from_code)
        rate_to   = self.get_rate(to_code)
        
        in_pln = amount * rate_from
        return in_pln / rate_to if rate_to else 0.0
