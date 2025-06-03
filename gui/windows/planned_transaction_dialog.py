from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QDateEdit, QComboBox,
    QLineEdit, QDialogButtonBox
)
from PyQt6.QtCore import QDate
from core.controllers.account_controller import AccountsController


class PlannedTransactionDialog(QDialog):
    def __init__(self, parent=None, pt=None):
        super().__init__(parent)
        self.pt = pt
        self.acc_ctrl = AccountsController()
        self.setWindowTitle("Zaplanowana transakcja")
        layout = QFormLayout(self)

        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)

        self.type_cb = QComboBox()
        self.type_cb.addItems(["Wydatek","Przychód"])

        self.amount_edit = QLineEdit()

        self.currency = "PLN"

        self.category_edit = QLineEdit()
        self.desc_edit = QLineEdit()

        self.freq_cb = QComboBox()
        self.freq_cb.addItems(["Jednorazowo","Co miesiąc"])

        self.account_cb = QComboBox()
        for acc in self.acc_ctrl.list_accounts():
            self.account_cb.addItem(acc.name, acc.id)

        layout.addRow("Data:", self.date_edit)
        layout.addRow("Typ:", self.type_cb)
        layout.addRow("Kwota:", self.amount_edit)
        layout.addRow("Kategoria:", self.category_edit)
        layout.addRow("Opis:", self.desc_edit)
        layout.addRow("Częstotliwość:", self.freq_cb)
        layout.addRow("Konto:", self.account_cb)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

        if pt: self._load(pt)

    def _load(self, pt):
        self.date_edit.setDate(pt.date)
        self.type_cb.setCurrentText(pt.type)
        self.amount_edit.setText(str(pt.amount))
        self.category_edit.setText(pt.category or '')
        self.desc_edit.setText(pt.description or '')
        self.freq_cb.setCurrentText(pt.frequency)
        idx = self.account_cb.findData(pt.account_id)
        if idx >= 0: self.account_cb.setCurrentIndex(idx)

    def get_data(self):
        return {
            'date': self.date_edit.date().toPyDate(),
            'type': self.type_cb.currentText(),
            'amount': float(self.amount_edit.text()),
            'currency': self.currency,
            'category': self.category_edit.text(),
            'description': self.desc_edit.text(),
            'frequency': self.freq_cb.currentText(),
            'account_id': self.account_cb.currentData()
        }
