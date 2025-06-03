
import hashlib
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QPushButton,
    QLabel, QMessageBox, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtCore import Qt
from core.controllers.settings_controller import SettingsController

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Logowanie")
        self.setModal(True)
        self.settings_ctrl = SettingsController()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
  
        self.lbl_info = QLabel("Podaj hasło dostępu:")
        self.lbl_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_info)

        form_layout = QFormLayout()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Hasło:", self.password_edit)
        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("Zaloguj")
        self.btn_cancel = QPushButton("Anuluj")
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.btn_ok.clicked.connect(self._check_password)
        self.btn_cancel.clicked.connect(self.reject)

    def _check_password(self):
        typed = self.password_edit.text().strip()
        if not typed:
            QMessageBox.warning(self, "Błąd", "Hasło nie może być puste.")
            return
        if self.settings_ctrl.check_password(typed):
            self.accept()
        else:
            QMessageBox.warning(self, "Błąd logowania", "Nieprawidłowe hasło.")
            self.password_edit.clear()
            self.password_edit.setFocus()
