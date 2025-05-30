from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QDateEdit, QComboBox, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QBrush, QColor
from core.controllers.history_controller import HistoryController

from gui.styles.table_style import apply_history_table_style

class historyTable(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = HistoryController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        filter_layout = QHBoxLayout()

        self.date_from = QDateEdit(calendarPopup=True)
        self.date_from.setDate(QDate.currentDate().addMonths(-1))

        self.date_to = QDateEdit(calendarPopup=True)
        self.date_to.setDate(QDate.currentDate())

        self.filter_category = QComboBox()
        self.filter_category.addItems(["Wszystkie", "Jedzenie", "Mieszkanie", "Transport"])

        self.filter_description = QLineEdit()
        self.filter_description.setPlaceholderText("Opis zawiera...")

        btn_apply = QPushButton("Filtruj")
        btn_apply.clicked.connect(self.load_transactions)

        for widget, label in [
            (self.date_from, "Od:"),
            (self.date_to, "Do:"),
            (self.filter_category, "Kategoria:"),
            (self.filter_description, "Opis:")
        ]:
            filter_layout.addWidget(QLabel(label))
            filter_layout.addWidget(widget)

        filter_layout.addWidget(btn_apply)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "Data", "Typ", "Kwota", "Waluta", "Kategoria", "Opis"
        ])

        apply_history_table_style(self.history_table)

        layout.addLayout(filter_layout)
        layout.addWidget(self.history_table)
        self.setLayout(layout)

        self.load_transactions()

    def load_transactions(self):
        date_from = self.date_from.date().toPyDate()
        date_to = self.date_to.date().toPyDate()
        category = self.filter_category.currentText()
        desc = self.filter_description.text().strip() or None

        transactions = self.controller.fetch_transactions(
            date_from=date_from,
            date_to=date_to,
            category=category,
            description_contains=desc
        )

        self.history_table.setRowCount(len(transactions))
        for row, tx in enumerate(transactions):
            values = [
                tx.date.strftime("%Y-%m-%d"),
                tx.type,
                f"{tx.amount:.2f}",
                tx.currency,
                tx.category or "",
                tx.description or ""
            ]
            for col, text in enumerate(values):
                item = QTableWidgetItem(text)
                item.setForeground(QBrush(QColor("black")))
                self.history_table.setItem(row, col, item)
