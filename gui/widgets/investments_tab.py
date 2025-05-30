from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QComboBox, QLineEdit, QPushButton, QLabel, QHBoxLayout, QDateEdit, QTableWidget

class investmentTable(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.investments_table = QTableWidget()
        self.investments_table.setColumnCount(5)
        self.investments_table.setHorizontalHeaderLabels([
            "Typ", "Symbol", "Ilość", "Cena zakupu", "Data"
        ])
        
        btn_add = QPushButton("Dodaj inwestycję")
        btn_edit = QPushButton("Edytuj")
        btn_remove = QPushButton("Usuń")
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_remove)
        
        layout.addWidget(self.investments_table)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    