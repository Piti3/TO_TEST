# gui/windows/change_password_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QPushButton,
    QLabel, QMessageBox, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtCore import Qt
from core.controllers.settings_controller import SettingsController

class ChangePasswordDialog(QDialog):
    """
    Dialog do ustawiania/zmiany/ usunięcia hasła dostępu.
    Jeżeli hasło już istnieje:
      - pojawi się pole na aktualne hasło
      - przycisk „Usuń hasło”
    Jeżeli hasła nie ma:
      - nie ma pola „Aktualne hasło”
      - brak przycisku „Usuń hasło”
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ustaw/zmień hasło dostępu")
        self.settings_ctrl = SettingsController()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # Sprawdźmy, czy hasło jest już ustawione
        self.existing = self.settings_ctrl.has_password()

        # Nagłówek informacyjny
        if self.existing:
            self.lbl_info = QLabel("Aby zmienić lub usunąć hasło, najpierw podaj aktualne.")
        else:
            self.lbl_info = QLabel("Nie wykryto dotychczasowego hasła. Ustaw nowe.")
        self.lbl_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_info)

        # --- Formularz pól ---
        form_layout = QFormLayout()

        # Jeżeli istnieje hasło, dodajemy pole na aktualne
        if self.existing:
            self.current_edit = QLineEdit()
            self.current_edit.setEchoMode(QLineEdit.EchoMode.Password)
            form_layout.addRow("Aktualne hasło:", self.current_edit)

        # Pole na nowe hasło
        self.new_edit = QLineEdit()
        self.new_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Nowe hasło:", self.new_edit)

        # Pole na potwierdzenie hasła
        self.confirm_edit = QLineEdit()
        self.confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Potwierdź hasło:", self.confirm_edit)

        layout.addLayout(form_layout)

        # --- Przycisk „Usuń hasło” (tylko jeśli istnieje) ---
        if self.existing:
            self.btn_remove = QPushButton("Usuń hasło")
            # Po kliknięciu: wywołujemy _remove_password()
            self.btn_remove.clicked.connect(self._remove_password)
            layout.addWidget(self.btn_remove)
        else:
            # Jeżeli nie ma hasła, nie tworzymy przycisku
            self.btn_remove = None

        # --- Przycisk „Zapisz” i „Anuluj” ---
        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("Zapisz")
        self.btn_cancel = QPushButton("Anuluj")
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        # Po kliknięciu „Zapisz” wykonujemy sprawdzenie i ewentualne zapisanie
        self.btn_ok.clicked.connect(self._save_password)
        self.btn_cancel.clicked.connect(self.reject)

    def _save_password(self):
        new_pw = self.new_edit.text().strip()
        confirm_pw = self.confirm_edit.text().strip()

        # 1) Nowe hasło nie może być puste
        if not new_pw:
            QMessageBox.warning(self, "Błąd", "Nowe hasło nie może być puste.")
            return

        # 2) Musi się zgadzać z potwierdzeniem
        if new_pw != confirm_pw:
            QMessageBox.warning(self, "Błąd", "Nowe hasło i potwierdzenie nie są takie same.")
            return

        # 3) Jeśli istniało już hasło, trzeba podać poprawnie stare
        if self.existing:
            current_pw = self.current_edit.text().strip()
            if not current_pw:
                QMessageBox.warning(self, "Błąd", "Podaj aktualne hasło.")
                return
            if not self.settings_ctrl.check_password(current_pw):
                QMessageBox.warning(self, "Błąd", "Aktualne hasło nieprawidłowe.")
                self.current_edit.clear()
                return

        # 4) Zapamiętaj nowe hasło
        self.settings_ctrl.set_password(new_pw)
        QMessageBox.information(self, "OK", "Hasło zostało zapisane pomyślnie.")
        self.accept()

    def _remove_password(self):
        """
        Usuwamy hasło z bazy (ustawiamy puste), dezaktywujemy przycisk i czyścimy pola.
        """
        reply = QMessageBox.question(
            self, "Usuń hasło",
            "Czy na pewno chcesz usunąć hasło? Po usunięciu aplikacja nie będzie już wymagać logowania.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.settings_ctrl.remove_password()
            QMessageBox.information(self, "OK", "Hasło zostało usunięte.")

            # Dezaktywujemy przycisk „Usuń hasło”
            if self.btn_remove:
                self.btn_remove.setDisabled(True)

            # Wyłączamy pole „Aktualne hasło”, jeśli istniało
            if self.existing:
                self.current_edit.clear()
                self.current_edit.setDisabled(True)

            # Czyścimy pola nowych haseł
            self.new_edit.clear()
            self.confirm_edit.clear()

            # Oznaczamy, że hasła już nie ma
            self.existing = False
