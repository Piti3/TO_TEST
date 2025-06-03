
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QComboBox, QSpinBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate
from core.controllers.budget_controller import BudgetController
from gui.windows.budget_dialog import BudgetDialog

class BudgetTab(QWidget):
    def __init__(self):
        super().__init__()
        self.ctrl = BudgetController()
        self._init_ui()

        today = QDate.currentDate()
        self.year_cb.setCurrentText(str(today.year()))
        self.month_cb.setCurrentIndex(today.month() - 1)
        self._load_budgets()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)

        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Rok:"))

        self.year_cb = QComboBox()
        current_year = QDate.currentDate().year()
        years = [str(y) for y in range(current_year - 3, current_year + 2)]
        self.year_cb.addItems(years)
        self.year_cb.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        top_layout.addWidget(self.year_cb)

        top_layout.addWidget(QLabel("Miesiąc:"))
        self.month_cb = QComboBox()
        months = [
            "Styczeń", "Luty", "Marzec", "Kwiecień",
            "Maj", "Czerwiec", "Lipiec", "Sierpień",
            "Wrzesień", "Październik", "Listopad", "Grudzień"
        ]
        self.month_cb.addItems(months)
        self.month_cb.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        top_layout.addWidget(self.month_cb)

        self.btn_refresh = QPushButton("Odśwież")
        self.btn_refresh.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        top_layout.addWidget(self.btn_refresh)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Kategoria", "Rok", "Miesiąc", "Limit"])
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        main_layout.addWidget(self.table)

        # Dolny pasek CRUD
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Dodaj")
        self.btn_edit = QPushButton("Edytuj")
        self.btn_delete = QPushButton("Usuń")

        for btn in (self.btn_add, self.btn_edit, self.btn_delete):
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn_layout.addWidget(btn)

        main_layout.addLayout(btn_layout)
        self.btn_refresh.clicked.connect(self._load_budgets)
        self.year_cb.currentIndexChanged.connect(self._load_budgets)
        self.month_cb.currentIndexChanged.connect(self._load_budgets)
        self.btn_add.clicked.connect(self._add_budget)
        self.btn_edit.clicked.connect(self._edit_budget)
        self.btn_delete.clicked.connect(self._delete_budget)

    def _load_budgets(self):
        year = int(self.year_cb.currentText())
        month = self.month_cb.currentIndex() + 1
        budgets = self.ctrl.get_budgets_for_month(year, month)

        self.table.setRowCount(len(budgets))
        for row, b in enumerate(budgets):
            vals = [
                b.category,
                str(b.year),
                str(b.month),
                f"{b.limit_amount:.2f}"
            ]
            for col, v in enumerate(vals):
                item = QTableWidgetItem(v)
                item.setForeground(Qt.GlobalColor.black)
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()

    def _add_budget(self):
        dlg = BudgetDialog(parent=self)
        today = QDate.currentDate()
        dlg.year_spin.setValue(today.year())
        dlg.month_spin.setValue(today.month())
        if dlg.exec():
            data = dlg.get_data()
            self.ctrl.create_budget(data)
            self._load_budgets()

    def _edit_budget(self):
        row = self.table.currentRow()
        if row < 0:
            return
        year = int(self.year_cb.currentText())
        month = self.month_cb.currentIndex() + 1
        budgets = self.ctrl.get_budgets_for_month(year, month)
        budget = budgets[row]
        dlg = BudgetDialog(parent=self, budget=budget)
        if dlg.exec():
            data = dlg.get_data()
            self.ctrl.update_budget(budget.id, data)
            self._load_budgets()

    def _delete_budget(self):
        row = self.table.currentRow()
        if row < 0:
            return
        year = int(self.year_cb.currentText())
        month = self.month_cb.currentIndex() + 1
        budgets = self.ctrl.get_budgets_for_month(year, month)
        budget = budgets[row]

        self.ctrl.delete_budget(budget.id)
        self._load_budgets()
