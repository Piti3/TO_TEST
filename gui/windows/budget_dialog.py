# gui/windows/budget_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QFormLayout,
    QLineEdit, QComboBox, QSpinBox,
    QDoubleSpinBox, QDialogButtonBox,
    QLabel, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from core.controllers.account_controller import AccountsController

class BudgetDialog(QDialog):
    """
    Dialog do stworzenia / edycji pojedynczego budżetu:
      - wybór kategorii (ciąg znaków, podany z klawiatury)
      - wybór roku (QSpinBox)
      - wybór miesiąca (QComboBox)
      - limit (QDoubleSpinBox)
    Jeżeli podany jest argument `budget` (instancja modelu Budget), wczytujemy
    dane do pól i umożliwiamy edycję.
    """

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

        # Pole do podania nazwy kategorii
        self.category_edit = QLineEdit()
        layout.addRow("Kategoria:", self.category_edit)

        # SpinBox do wyboru roku
        current_year = QDate.currentDate().year()
        self.year_spin = QSpinBox()
        self.year_spin.setRange(current_year - 5, current_year + 5)
        self.year_spin.setValue(current_year)
        layout.addRow("Rok:", self.year_spin)

        # ComboBox do wyboru miesiąca
        self.month_spin = QSpinBox()
        self.month_spin.setRange(1, 12)
        self.month_spin.setValue(QDate.currentDate().month())
        layout.addRow("Miesiąc (1–12):", self.month_spin)

        # Limit budżetowy
        self.limit_spin = QDoubleSpinBox()
        self.limit_spin.setDecimals(2)
        self.limit_spin.setMaximum(1_000_000_000)
        self.limit_spin.setValue(0.00)
        layout.addRow("Limit (PLN):", self.limit_spin)

        # Przyciski OK / Anuluj
        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._on_accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _load(self, budget):
        """
        Wczytuje dane istniejącego budżetu do pól dialogu.
        """
        self.category_edit.setText(budget.category)
        self.year_spin.setValue(budget.year)
        self.month_spin.setValue(budget.month)
        self.limit_spin.setValue(budget.limit_amount)

    def _on_accept(self):
        """
        Sprawdza poprawność pól i zamyka dialog, 
        przekazując dane do kontrolera.
        """
        cat = self.category_edit.text().strip()
        if not cat:
            QMessageBox.warning(self, "Błąd", "Kategoria nie może być pusta.")
            return

        # Nie pozwalamy na 0.00 lub ujemne
        lim = self.limit_spin.value()
        if lim <= 0:
            QMessageBox.warning(self, "Błąd", "Limit budżetu powinien być > 0.")
            return

        # wszystko OK
        self.accept()

    def get_data(self) -> dict:
        """
        Zwraca słownik danych:
          { 'category': str, 'year': int, 'month': int, 'limit_amount': float }
        """
        return {
            'category': self.category_edit.text().strip(),
            'year': self.year_spin.value(),
            'month': self.month_spin.value(),
            'limit_amount': self.limit_spin.value()
        }
