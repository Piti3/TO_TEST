from PyQt6.QtWidgets import (
    QDialog, QFormLayout,
    QLineEdit, QComboBox, QSpinBox,
    QDoubleSpinBox, QDialogButtonBox,
    QLabel, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from core.controllers.account_controller import AccountsController

class BudgetDialog(QDialog):

    def __init__(self, parent=None, budget=None):
        super().__init__(parent)
        self.budget = budget
        self.setWindowTitle("Dodaj/Edytuj limit budżetu")
        self._init_ui()
        if self.budget:
            self._load(self.budget)

    def _init_ui(self):
        layout = QFormLayout(self)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.category_edit = QLineEdit()
        layout.addRow("Kategoria:", self.category_edit)

        current_year = QDate.currentDate().year()
        self.year_spin = QSpinBox()
        self.year_spin.setRange(current_year - 5, current_year + 5)
        self.year_spin.setValue(current_year)
        layout.addRow("Rok:", self.year_spin)

        self.month_spin = QSpinBox()
        self.month_spin.setRange(1, 12)
        self.month_spin.setValue(QDate.currentDate().month())
        layout.addRow("Miesiąc (1–12):", self.month_spin)

        self.limit_spin = QDoubleSpinBox()
        self.limit_spin.setDecimals(2)
        self.limit_spin.setMaximum(1_000_000_000)
        self.limit_spin.setValue(0.00)
        layout.addRow("Limit (PLN):", self.limit_spin)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._on_accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _load(self, budget):
        self.category_edit.setText(budget.category)
        self.year_spin.setValue(budget.year)
        self.month_spin.setValue(budget.month)
        self.limit_spin.setValue(budget.limit_amount)

    def _on_accept(self):
        cat = self.category_edit.text().strip()
        if not cat:
            QMessageBox.warning(self, "Błąd", "Kategoria nie może być pusta.")
            return

        lim = self.limit_spin.value()
        if lim <= 0:
            QMessageBox.warning(self, "Błąd", "Limit budżetu powinien być > 0.")
            return

        self.accept()

    def get_data(self) -> dict:

        return {
            'category': self.category_edit.text().strip(),
            'year': self.year_spin.value(),
            'month': self.month_spin.value(),
            'limit_amount': self.limit_spin.value()
        }
