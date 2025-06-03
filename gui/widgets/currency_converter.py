
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout,
    QLabel, QComboBox, QDoubleSpinBox,
    QPushButton, QHBoxLayout, 
)
from PyQt6.QtCore import Qt
from core.controllers.currency_controller import CurrencyController

class CurrencyConverterTable(QWidget):
    def __init__(self, controller: CurrencyController = None):
        super().__init__()
        self.controller = controller or CurrencyController()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.from_cb = QComboBox()
        form.addRow("Z:", self.from_cb)

        self.to_cb = QComboBox()
        form.addRow("Na:", self.to_cb)

        amount_layout = QHBoxLayout()
        self.amount_sb = QDoubleSpinBox()
        self.amount_sb.setDecimals(2)
        self.amount_sb.setMaximum(1_000_000_000)
        amount_layout.addWidget(self.amount_sb)

        self.convert_btn = QPushButton("Przelicz")
        amount_layout.addWidget(self.convert_btn)
        amount_layout.addStretch()
        form.addRow("Kwota:", amount_layout)

        main_layout.addLayout(form)

        self.result_lbl = QLabel("")
        self.result_lbl.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        main_layout.addWidget(self.result_lbl)
        main_layout.addStretch()

        self._load_currencies()
        self.convert_btn.clicked.connect(self.on_convert)

    def _load_currencies(self):
        self.from_cb.clear()
        self.to_cb.clear()

        for code in self.controller.get_currencies():
            rate = self.controller.get_rate(code)
            label = f"{code} ({rate:.4f})"
            self.from_cb.addItem(label, code)
            self.to_cb.addItem(label, code)

        # PLN → EUR
        i_pln = self.from_cb.findData("PLN")
        i_eur = self.to_cb.findData("EUR")
        if i_pln >= 0: self.from_cb.setCurrentIndex(i_pln)
        if i_eur >= 0: self.to_cb.setCurrentIndex(i_eur)

    def on_convert(self):
        from_code = self.from_cb.currentData()
        to_code   = self.to_cb.currentData()
        amount    = self.amount_sb.value()

        result = self.controller.convert(from_code, to_code, amount)
        self.result_lbl.setText(
            f"{amount:.2f} {from_code} = {result:.4f} {to_code}"
        )
