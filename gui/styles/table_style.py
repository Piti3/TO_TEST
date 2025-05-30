# ≡≡≡ gui/styles/table_styles.py ≡≡≡

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
    # Kolumna 0: „Typ” → ResizeToContents
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    # Kolumna 1: „Kwota” → ResizeToContents
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    # Kolumna 2: „Kategoria” → Stretch (aby zawsze wypełniała wolne miejsce)
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
    # Kolumna 3: „Opis” → Stretch
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
    # Kolumna 4: „Częstotliwość” → ResizeToContents
    header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
    # Kolumna 5: „Konto” → ResizeToContents
    header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

def apply_history_table_style(table: QTableWidget):

    apply_generic_table_style(table)

    header = table.horizontalHeader()
    # Kolumna 0: Data          → ResizeToContents
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    # Kolumna 1: Typ           → ResizeToContents
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    # Kolumna 2: Kwota         → ResizeToContents
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    # Kolumna 3: Waluta        → ResizeToContents
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
    # Kolumna 4: Kategoria     → Stretch (zabiera wolne miejsce)
    header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
    # Kolumna 5: Opis          → Stretch
    header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)