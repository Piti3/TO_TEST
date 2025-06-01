import sys
from PyQt6.QtWidgets import QApplication
from gui.windows.main_window import MainWindow
from gui.windows.login_dialog import LoginDialog
from core.controllers.settings_controller import SettingsController

def main():
    app = QApplication(sys.argv)

    settings_ctrl = SettingsController()
    
    if settings_ctrl.has_password():
        login = LoginDialog()
        if login.exec() != LoginDialog.DialogCode.Accepted:
            # użytkownik anulował lub podał złe hasło → zamykamy aplikację
            sys.exit(0)

    # 2) Lub jeśli hasła nie było, albo logowanie się powiodło → pokazujemy główne okno
    # Ładowanie stylów
    with open("gui/styles/main_style.qss", "r") as f:
        app.setStyleSheet(f.read())
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()