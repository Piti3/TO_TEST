import sys
from PyQt6.QtWidgets import QApplication
from gui.windows.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Ładowanie stylów
    with open("gui/styles/main_style.qss", "r") as f:
        app.setStyleSheet(f.read())
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()