from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QComboBox, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt, QDate

class chartsTable(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()
        
        lbl_chart_placeholder = QLabel("Wykresy i statystyki będą widoczne w tej sekcji")
        lbl_chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.summary_label = QLabel("Bilans miesięczny: + 0.00 PLN")
        self.summary_label.setStyleSheet("font-size: 16px; color: green;")
        
        layout.addWidget(self.summary_label)
        layout.addWidget(lbl_chart_placeholder)
        self.setLayout(layout)