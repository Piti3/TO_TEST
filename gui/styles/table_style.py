from PyQt6.QtWidgets import QTableWidget, QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

def apply_generic_table_style(table: QTableWidget):

    table.setShowGrid(True)
    table.setAlternatingRowColors(True)
    table.setStyleSheet("""
        QTableWidget {
            background-color: #FFFFFF;
            alternate-background-color: #F7F7F7;
            gridline-color: #E0E0E0;
        }
        QHeaderView::section {
            background-color: #2C3E50;
            color: white;
            padding: 4px;
            font-weight: bold;
            border: 0px;
        }
        QTableWidget::item:selected {
            background-color: #D0E4FF;
            color: black;
        }
    """)

    font = QFont()
    font.setPointSize(10)
    table.setFont(font)
    header = table.horizontalHeader()
    header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

    for col in range(table.columnCount()):
        header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)


def apply_transaction_table_style(table: QTableWidget):

    apply_generic_table_style(table)

    header = table.horizontalHeader()

    header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Data
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Typ
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Kwota
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Waluta
    header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)           # Kategoria
    header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)           # Opis
    header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Konto


def apply_planned_transaction_table_style(table: QTableWidget):

    apply_generic_table_style(table)

    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Typ
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) # Kwota
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # Kategoria
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) # Opis
    header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) #Częstotliwość
    header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) # Konto

def apply_history_table_style(table: QTableWidget):

    apply_generic_table_style(table)

    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Data
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) # Typ
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents) # Kwota
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)# Kategoria
    header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch) # Kategoria
    header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch) # Opis

def apply_budget_table_style(table: QTableWidget):

    apply_generic_table_style(table)

    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Kategoria
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Rok
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Miesiąc
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Limit