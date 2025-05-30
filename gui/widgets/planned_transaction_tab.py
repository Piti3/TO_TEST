# gui/widgets/planned_transaction_tab.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QPushButton, QLabel, QTableWidgetItem
)
from PyQt6.QtCore import QDate, Qt
from core.controllers.planned_transaction_controller import PlannedTransactionController
from gui.windows.planned_transaction_dialog import PlannedTransactionDialog

from gui.widgets.marked_calendar import MarkedCalendar
from gui.styles.table_style import apply_planned_transaction_table_style

class PlannedTransactionsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.ctrl = PlannedTransactionController()
        self._init_ui()

        self._refresh_marks()

        self._load_for_date(QDate.currentDate().toPyDate())

    def _init_ui(self):
        layout = QHBoxLayout(self)

        self.calendar = MarkedCalendar()
        self.calendar.selectionChanged.connect(
            lambda: self._load_for_date(self.calendar.selectedDate().toPyDate())
        )
        layout.addWidget(self.calendar, 1)

        right = QVBoxLayout()
        self.lbl_date = QLabel()
        right.addWidget(self.lbl_date)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Typ", "Kwota", "Kategoria", "Opis", "Częstotliwość", "Konto"
        ])

        apply_planned_transaction_table_style(self.table)
        right.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Dodaj")
        self.btn_edit = QPushButton("Edytuj")
        self.btn_delete = QPushButton("Usuń")
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        right.addLayout(btn_layout)

        self.btn_add.clicked.connect(self._on_add)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_delete.clicked.connect(self._on_delete)

        layout.addLayout(right, 2)

    def _refresh_marks(self):

        dates = self.ctrl.get_all_dates()
        self.calendar.marked_dates = dates
        self.calendar.update()

    def _load_for_date(self, date):

        self.date = date
        self.lbl_date.setText(f"Zaplanowane na: {date}")
        pts = self.ctrl.list_for_date(date)
        self.table.setRowCount(len(pts))

        for row, pt in enumerate(pts):
            vals = [
                pt.type,
                f"{pt.amount:.2f}",
                pt.category or '',
                pt.description or '',
                pt.frequency,
                pt.account.name
            ]
            for col, v in enumerate(vals):
                item = QTableWidgetItem(v)
                item.setForeground(Qt.GlobalColor.black)
                if col == 1:  # „Kwota”
                    if pt.type == "Wydatek":
                        item.setForeground(Qt.GlobalColor.red)
                    else:
                        item.setForeground(Qt.GlobalColor.darkGreen)
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
                )
                self.table.setItem(row, col, item)

    def _on_add(self):
        dlg = PlannedTransactionDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            self.ctrl.create(data)
            self._load_for_date(self.date)
            self._refresh_marks()

    def _on_edit(self):
        row = self.table.currentRow()
        if row < 0:
            return
        pt = self.ctrl.list_for_date(self.date)[row]
        dlg = PlannedTransactionDialog(self, pt)
        if dlg.exec():
            self.ctrl.update(pt.id, dlg.get_data())
            self._load_for_date(self.date)
            self._refresh_marks()

    def _on_delete(self):
        row = self.table.currentRow()
        if row < 0:
            return
        pt = self.ctrl.list_for_date(self.date)[row]
        self.ctrl.delete(pt.id)
        self._load_for_date(self.date)
        self._refresh_marks()
