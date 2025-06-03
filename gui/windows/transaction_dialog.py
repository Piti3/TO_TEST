
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import QDate
from database import Account
from core.repositories.account_repository import AccountRepository

class TransactionDialog(QDialog):
    def __init__(self, parent=None, transaction=None):
        super().__init__(parent)
        self.setWindowTitle("Dodaj/Edycja transakcji")
        self.transaction = transaction
        self.account_repo = AccountRepository()
        self.init_ui()

        if self.account_combo.count() == 0:
            default_acc = Account(name="Portfel")
            self.session.add(default_acc)
            self.session.commit()
            self.account_combo.addItem(default_acc.name, default_acc.id)
        if transaction:
            self.load_transaction()

    def init_ui(self):
        layout = QFormLayout(self)
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Wydatek", "Przychód"])
        self.amount_edit = QLineEdit()
        self.currency_edit = QLineEdit("PLN")
        self.category_edit = QLineEdit()
        self.desc_edit = QLineEdit()
        self.account_combo = QComboBox()
       
        accounts = self.account_repo.get_all_accounts()
        for account in accounts:
            self.account_combo.addItem(account.name, account.id)

        layout.addRow("Data:", self.date_edit)
        layout.addRow("Typ:", self.type_combo)
        layout.addRow("Kwota:", self.amount_edit)
        layout.addRow("Waluta:", self.currency_edit)
        layout.addRow("Kategoria:", self.category_edit)
        layout.addRow("Opis:", self.desc_edit)
        layout.addRow("Konto:", self.account_combo)

        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("Zapisz")
        self.btn_cancel = QPushButton("Anuluj")
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addRow(btn_layout)

        self.btn_ok.clicked.connect(self.on_accept)
        self.btn_cancel.clicked.connect(self.reject)

    def load_transaction(self):
        t = self.transaction
        self.date_edit.setDate(QDate(t.date.year, t.date.month, t.date.day))
        self.type_combo.setCurrentText(t.type)
        self.amount_edit.setText(str(t.amount))
        self.currency_edit.setText(t.currency)
        self.category_edit.setText(t.category)
        self.desc_edit.setText(t.description or "")
        idx = self.account_combo.findData(t.account_id)
        if idx >= 0:
            self.account_combo.setCurrentIndex(idx)

    def get_data(self):
        acc_id = self.account_combo.currentData()
        if acc_id is None and self.account_combo.count() > 0:
            acc_id = self.account_combo.itemData(0)
        data = {
            'date': self.date_edit.date().toPyDate(),
            'type': self.type_combo.currentText(),
            'amount': float(self.amount_edit.text()),
            'currency': self.currency_edit.text(),
            'category': self.category_edit.text(),
            'description': self.desc_edit.text(),
            'account_id': acc_id
        }
        return data

    def on_accept(self):
        self.accept()



