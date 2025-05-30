
from datetime import date, timedelta
import calendar
from typing import Tuple, List
from core.controllers.account_controller import AccountsController
from core.controllers.transaction_controller import TransactionController

class OverviewController:
    def __init__(self):
        self.acc_ctrl = AccountsController()
        self.tx_ctrl  = TransactionController()

    def total_balance(self) -> float:
        """Suma salda ze wszystkich kont."""
        accounts = self.acc_ctrl.list_accounts()
        return sum(a.balance for a in accounts)

    def month_summary(self, year: int, month: int) -> Tuple[float,float]:
        txs = self.tx_ctrl.get_transactions_for_month(year, month)
        inc = sum(t.amount for t in txs if t.type=="Przychód")
        exp = sum(t.amount for t in txs if t.type=="Wydatek")
        return inc, exp

    def yearly_balance_trend(self) -> List[Tuple[date, float]]:
        today = date.today()
        trend = []
        for m in range(1, today.month + 1):
            last_day = calendar.monthrange(today.year, m)[1]
            target = date(today.year, m, last_day)
            txs_up_to = self.tx_ctrl.get_transactions_up_to_date(target)
            # saldo = suma wpływów - suma wydatków
            bal = sum(t.amount if t.type == "Przychód" else -t.amount for t in txs_up_to)
            trend.append((target, bal))
        return trend

    def weekly_flow(self) -> List[Tuple[date, float, float]]:
        today = date.today()
        week = []
        for d in range(6, -1, -1):
            day = today - timedelta(days=d)
            txs = self.tx_ctrl.get_transactions_for_month(day.year, day.month)
            day_txs = [t for t in txs if t.date == day]
            inc = sum(t.amount for t in day_txs if t.type=="Przychód")
            exp = sum(t.amount for t in day_txs if t.type=="Wydatek")
            week.append((day, inc, exp))
        return week

    def recent_transactions(self, limit: int = 7):
        return self.tx_ctrl.get_recent_transactions(limit)