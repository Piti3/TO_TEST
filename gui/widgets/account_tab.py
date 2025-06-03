
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,QListWidget, QListWidgetItem, QMessageBox, QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QBrush
from gui.windows.add_account_dialog import AddAccountDialog
from core.controllers.account_controller import AccountsController

class AccountsTable(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = AccountsController()
        self.layout = QVBoxLayout(self)
        self._build_ui()
        self.refresh_accounts()

    def _build_ui(self):
        self.summary_label = QLabel()
        font_sum = QFont()
        font_sum.setPointSize(14)
        font_sum.setBold(True)
        self.summary_label.setFont(font_sum)
        self.summary_label.setStyleSheet("color: white;")
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.summary_label)

        self.accounts_list = QListWidget()
        self.accounts_list.setAlternatingRowColors(True)
        self.accounts_list.setStyleSheet("""
            QListWidget {
                background-color: #FFFFFF;
                alternate-background-color: #F0F0F0;
                border: 1px solid #E0E0E0;
                outline: none;
            }
            QListWidget::item {
                padding: 8px 12px;
                border-bottom: 1px solid #CCCCCC;
            }
            QListWidget::item:last-child {
                border-bottom: none;
            }
            QListWidget::item:selected {
                background-color: #D0E4FF;
                color: black;
            }
        """)
        self.layout.addWidget(self.accounts_list)

        btn_layout = QHBoxLayout()
        self.add_button = QPushButton("Dodaj")
        self.edit_button = QPushButton("Edytuj")
        self.delete_button = QPushButton("Usuń")
        for btn in (self.add_button, self.edit_button, self.delete_button):
            btn.setMinimumHeight(30)
            btn_layout.addWidget(btn)
        self.layout.addLayout(btn_layout)

        self.add_button.clicked.connect(self.show_add_dialog)
        self.edit_button.clicked.connect(self.show_edit_dialog)
        self.delete_button.clicked.connect(self.show_delete_dialog)

    def refresh_accounts(self):
        accounts = self.controller.list_accounts()
        self.accounts_list.clear()
        total = 0.0

        for acc in accounts:
            total += acc.balance

            text = f"{acc.name:<20s}  {acc.balance:,.2f} zł"
            item = QListWidgetItem(text)

            font_item = QFont()
            font_item.setPointSize(11)
            item.setFont(font_item)

            item.setForeground(QBrush(QColor("black")))

            item.setData(Qt.ItemDataRole.UserRole, acc.id)

            self.accounts_list.addItem(item)

        self.summary_label.setText(f"Razem: {total:,.2f} zł")

    def show_add_dialog(self):
        dlg = AddAccountDialog(self, controller=self.controller)
        if dlg.exec():
            self.refresh_accounts()

    def show_edit_dialog(self):
        item = self.accounts_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Edytuj konto", "Wybierz konto z listy.")
            return
        acc_id = item.data(Qt.ItemDataRole.UserRole)
        dlg = AddAccountDialog(self, account_id=acc_id, controller=self.controller)
        if dlg.exec():
            self.refresh_accounts()

    def show_delete_dialog(self):
        item = self.accounts_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Usuń konto", "Wybierz konto z listy.")
            return
        acc_id = item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(
            self, "Usuń konto", "Czy na pewno usunąć konto?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.delete_account(acc_id)
            self.refresh_accounts()
