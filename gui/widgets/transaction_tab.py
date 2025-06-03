
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QHBoxLayout,QPushButton, QTableWidgetItem, QComboBox, QLabel, QSizePolicy,QMessageBox)
from PyQt6.QtCore import Qt, QDate
from gui.windows.transaction_dialog import TransactionDialog
from core.controllers.transaction_controller import TransactionController
from core.controllers.account_controller import AccountsController
from core.controllers.budget_controller import BudgetController
from gui.styles.table_style import apply_transaction_table_style


MONTHS = [
    "Styczeń", "Luty", "Marzec", "Kwiecień",
    "Maj", "Czerwiec", "Lipiec", "Sierpień",
    "Wrzesień", "Październik", "Listopad", "Grudzień"
]

class TransactionTable(QWidget):
    def __init__(self):
        super().__init__()
        self.tx_controller = TransactionController()
        self.acc_controller = AccountsController()
        self.budget_controller = BudgetController()
        self.init_ui()
        self.load_transactions()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(5, 5, 5, 5)
        header_layout.setSpacing(10)

        header_layout.addWidget(QLabel("Miesiąc:"))
        self.month_cb = QComboBox()
        self.month_cb.addItems(MONTHS)
        current_month = QDate.currentDate().month() - 1
        self.month_cb.setCurrentIndex(current_month)
        self.month_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        header_layout.addWidget(self.month_cb)

        header_layout.addWidget(QLabel("Rok:"))
        self.year_cb = QComboBox()
        current_year = QDate.currentDate().year()
        years = [str(y) for y in range(current_year - 5, current_year + 1)]
        self.year_cb.addItems(years)
        self.year_cb.setCurrentText(str(current_year))
        self.year_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        header_layout.addWidget(self.year_cb)

        self.btn_refresh = QPushButton("Odśwież")
        self.btn_refresh.setFixedWidth(80)
        header_layout.addWidget(self.btn_refresh)

        main_layout.addLayout(header_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Data", "Typ", "Kwota", "Waluta", "Kategoria", "Opis", "Konto"
        ])
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        apply_transaction_table_style(self.table)

        main_layout.addWidget(self.table)

        #dolny pasek CRUD
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(5, 5, 5, 5)
        footer_layout.setSpacing(10)

        self.btn_add = QPushButton("Dodaj")
        self.btn_edit = QPushButton("Edytuj")
        self.btn_remove = QPushButton("Usuń")
        for btn in (self.btn_add, self.btn_edit, self.btn_remove):
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            footer_layout.addWidget(btn)

        main_layout.addLayout(footer_layout)

        self.btn_refresh.clicked.connect(self.load_transactions)
        self.month_cb.currentIndexChanged.connect(self.load_transactions)
        self.year_cb.currentIndexChanged.connect(self.load_transactions)
        self.btn_add.clicked.connect(self.add_tx)
        self.btn_edit.clicked.connect(self.edit_tx)
        self.btn_remove.clicked.connect(self.remove_tx)


    def load_transactions(self):
        year = int(self.year_cb.currentText())
        month = self.month_cb.currentIndex() + 1

        txs = self.tx_controller.get_transactions_for_month(year, month)
        self.table.setRowCount(len(txs))

        for row, t in enumerate(txs):
            vals = [
                t.date.strftime("%Y-%m-%d"),
                t.type,
                f"{t.amount:.2f}",
                t.currency,
                t.category or "",
                t.description or "",
                t.account.name
            ]
            for col, v in enumerate(vals):
                item = QTableWidgetItem(v)
                item.setForeground(Qt.GlobalColor.black)
                if col == 2:
                    if t.type == "Wydatek":
                        item.setForeground(Qt.GlobalColor.red)
                    else:
                        item.setForeground(Qt.GlobalColor.darkGreen)
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                self.table.setItem(row, col, item)


    def add_tx(self):
            dlg = TransactionDialog(self)
            if dlg.exec():
                data = dlg.get_data()
                tx_id = self.tx_controller.create_transaction(data)
                delta = data['amount'] if data['type'] == "Przychód" else -data['amount']
                self.acc_controller.change_balance(data['account_id'], delta)

                if data['type'] == "Wydatek":
                    dt = data['date']
                    cat = data['category']
                    year = dt.year
                    month = dt.month

                    budget = self.budget_controller.get_budget_for_category_month(cat, year, month)
                    if budget:
                        spent = self.budget_controller.current_month_spent_for_category(cat, year, month)
                        if spent > budget.limit_amount:
                            QMessageBox.warning(
                                self,
                                "Przekroczenie budżetu",
                                f"Przekroczyłeś limit budżetu dla kategorii „{cat}”!\n"
                                f"Limit: {budget.limit_amount:.2f} zł, Wydano: {spent:.2f} zł"
                            )

                self.load_transactions()

    def edit_tx(self):
        row = self.table.currentRow()
        if row < 0:
            return
        year = int(self.year_cb.currentText())
        month = self.month_cb.currentIndex() + 1
        txs = self.tx_controller.get_transactions_for_month(year, month)
        tx = txs[row]

        old_amt, old_type, old_acc = tx.amount, tx.type, tx.account_id
        dlg = TransactionDialog(self, tx)
        if dlg.exec():
            new = dlg.get_data()
            self.tx_controller.update_transaction(tx.id, new)
            rev = -old_amt if old_type == "Przychód" else old_amt
            adj = new['amount'] if new['type'] == "Przychód" else -new['amount']
            if new['account_id'] != old_acc:
                self.acc_controller.change_balance(old_acc, rev)
                self.acc_controller.change_balance(new['account_id'], adj)
            else:
                self.acc_controller.change_balance(old_acc, rev + adj)
            self.load_transactions()

    def remove_tx(self):
        row = self.table.currentRow()
        if row < 0:
            return
        year = int(self.year_cb.currentText())
        month = self.month_cb.currentIndex() + 1
        txs = self.tx_controller.get_transactions_for_month(year, month)
        tx = txs[row]

        with self.tx_controller.session_factory() as s:
            s.delete(tx)
            s.commit()
        delta = -tx.amount if tx.type == "Przychód" else tx.amount
        self.acc_controller.change_balance(tx.account_id, delta)
        self.load_transactions()
