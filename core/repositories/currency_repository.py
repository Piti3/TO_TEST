
import urllib.request
import json
from typing import Dict

class CurrencyRepository:
    """
    Odpowiada za pobranie i przechowanie kursów z API NBP
    bez potrzeby instalowania requests.
    """
    API_URL = "https://api.nbp.pl/api/exchangerates/tables/a/?format=json"

    def __init__(self):
        self._rates: Dict[str, float] = {}
        self._loaded = False

    def load_rates(self) -> None:
        if self._loaded:
            return

        with urllib.request.urlopen(self.API_URL, timeout=5) as resp:
            body = resp.read()
            data = json.loads(body)[0]["rates"]

        self._rates = {r["code"]: r["mid"] for r in data}
        self._rates["PLN"] = 1.0
        self._loaded = True

    def get_rate(self, code: str) -> float:
        if not self._loaded:
            self.load_rates()
        return self._rates.get(code, 0.0)

    def list_currencies(self) -> list[str]:
        if not self._loaded:
            self.load_rates()
        return sorted(self._rates.keys())
