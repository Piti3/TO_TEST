from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QComboBox,QDialogButtonBox, QDoubleSpinBox)
from core.controllers.account_controller import AccountsController

class AddAccountDialog(QDialog):
    def __init__(self, parent=None, account_id=None, controller=None):
        super().__init__(parent)
        self.setWindowTitle("Dodaj/Edycja konta")
        self.controller = controller or AccountsController()
        self.account_id = account_id
        self.init_ui()
        if account_id:
            self.load_account()

    def init_ui(self):
        layout = QFormLayout(self)
        self.name_input = QLineEdit()
        self.balance_input = QDoubleSpinBox()
        self.balance_input.setMaximum(1_000_000)
        self.type_input = QComboBox()
        self.type_input.addItems(["Normalny", "Gotówka", "Bankowe", "Karta"])

        layout.addRow("Nazwa:", self.name_input)
        layout.addRow("Saldo:", self.balance_input)
        layout.addRow("Typ:", self.type_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def load_account(self):
        acc = self.controller.get_account(self.account_id)
        if not acc:
            return
        self.name_input.setText(acc.name)
        self.balance_input.setValue(acc.balance)
        idx = self.type_input.findText(acc.type)
        if idx >= 0:
            self.type_input.setCurrentIndex(idx)

    def save(self):
        name = self.name_input.text().strip()
        balance = self.balance_input.value()
        type_ = self.type_input.currentText()
        if self.account_id:
            self.controller.update_account(self.account_id, name, balance, type_)
        else:
            self.controller.create_account(name, balance, type_)
        self.accept()
