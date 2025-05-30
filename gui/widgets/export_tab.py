# gui/widgets/export_tab.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QFileDialog, QHBoxLayout
from core.controllers.export_controller import ExportController


class ExportTab(QWidget):
    def __init__(self):
        super().__init__()
        self.ctrl = ExportController()
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)

        # Lewa kolumna
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        btn_excel = QPushButton("Eksportuj do Excela")
        btn_excel.setMinimumHeight(800)
        btn_excel.clicked.connect(self.on_export_excel)
        left_layout.addWidget(btn_excel)
        left_layout.addStretch()

        # Prawa kolumna
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        btn_pdf = QPushButton("Generuj raport PDF")
        btn_pdf.setMinimumHeight(800)
        btn_pdf.clicked.connect(self.on_export_pdf)
        right_layout.addWidget(btn_pdf)
        right_layout.addStretch()

        layout.addWidget(left_widget)
        layout.addWidget(right_widget)
        self.setLayout(layout)

    def on_export_excel(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz jako Excel",
            "export.xlsx",
            "Excel files (*.xlsx)"
        )
        if not path:
            return
        try:
            result_path = self.ctrl.export_all_excel(path)
            QMessageBox.information(
                self,
                "Eksport do Excela",
                f"Plik został zapisany:\n{result_path}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Błąd eksportu", str(e))

    def on_export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz PDF",
            "report.pdf",
            "PDF files (*.pdf)"
        )
        if not path:
            return
        try:
            pdf_path = self.ctrl.export_pdf(path)
            QMessageBox.information(self, "Generowanie PDF", f"Raport PDF zapisano:\n{pdf_path}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd generowania PDF", str(e))
