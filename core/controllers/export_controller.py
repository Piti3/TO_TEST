# core/controllers/export_controller.py

import os
from datetime import datetime
import pandas as pd  # pandas do obsługi DataFrame i zapisu do Excela

# reportlab (platypus) do generowania „pięknego” PDF-a
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

from database.models.account import Account
from database.models.transaction import Transaction
from database.session import Session


class ExportController:
    def __init__(self):
        self.session = Session()

    def fetch_accounts(self):
        return self.session.query(Account).order_by(Account.id).all()

    def fetch_transactions(self):
        return self.session.query(Transaction).order_by(Transaction.date).all()

    def export_all_excel(self, path: str) -> str:

        if not path.lower().endswith(".xlsx"):
            path = path + ".xlsx"
        
        #Konta
        accounts = self.fetch_accounts()
        accounts_data = []
        for a in accounts:
            accounts_data.append({
                "ID": a.id,
                "Name": a.name,
                "Balance": round(a.balance or 0, 2),
                "Type": a.type,
            })
        df_accounts = pd.DataFrame(accounts_data)

        #transakcje
        txs = self.fetch_transactions()
        tx_data = []
        for t in txs:
            tx_data.append({
                "ID": t.id,
                "Date": t.date.strftime("%Y-%m-%d"),
                "Type": t.type,
                "Amount": round(t.amount, 2),
                "Currency": t.currency,
                "Category": t.category or "",
                "Description": t.description or "",
                "Account_ID": t.account_id,
                "Account_Name": t.account.name,
            })
        df_txs = pd.DataFrame(tx_data)

        with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
            df_accounts.to_excel(writer, sheet_name="Accounts", index=False)
            df_txs.to_excel(writer, sheet_name="Transactions", index=False)

            workbook = writer.book
            header_format = workbook.add_format({
                "bold": True,
                "bg_color": "#4F81BD",
                "font_color": "white",
                "border": 1
            })
            # Dla zakładki Accounts
            worksheet_acc = writer.sheets["Accounts"]
            for col_num, value in enumerate(df_accounts.columns.values):
                worksheet_acc.set_column(col_num, col_num, 15)  # szerokość każdej kolumny
                worksheet_acc.write(0, col_num, value, header_format)

            # Dla zakładki Transactions
            worksheet_t = writer.sheets["Transactions"]
            for col_num, value in enumerate(df_txs.columns.values):
                worksheet_t.set_column(col_num, col_num, 15)
                worksheet_t.write(0, col_num, value, header_format)

            writer.save()

        return os.path.abspath(path)

    def export_pdf(self, path: str) -> str:

        if not path.lower().endswith(".pdf"):
            path = f"{path}.pdf"

        accounts = self.fetch_accounts()
        txs = self.fetch_transactions()

        doc = SimpleDocTemplate(
            path,
            pagesize=A4,
            rightMargin=20,
            leftMargin=20,
            topMargin=30,
            bottomMargin=20,
        )

        styles = getSampleStyleSheet()
        elements = []

        title_style = ParagraphStyle(
            name="Title",
            parent=styles["Heading1"],
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=10,
        )
        date_style = ParagraphStyle(
            name="Date",
            parent=styles["Normal"],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.grey,
            spaceAfter=20,
        )
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elements.append(Paragraph("Raport Finansowy", title_style))
        elements.append(Paragraph(f"Data wygenerowania: {now_str}", date_style))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Konta:", styles["Heading2"]))
        elements.append(Spacer(1, 6))

        acc_table_data = [
            ["ID", "Nazwa", "Saldo", "Typ"]
        ]
        for a in accounts:
            acc_table_data.append([
                a.id,
                a.name,
                f"{a.balance:,.2f} zł",
                a.type
            ])

        t_acc = Table(acc_table_data, hAlign="LEFT", repeatRows=1)
        t_acc.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (2, 1), (2, -1), "RIGHT"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, 0), 11),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
            ])
        )
        elements.append(t_acc)
        elements.append(PageBreak())

        elements.append(Paragraph("Transakcje:", styles["Heading2"]))
        elements.append(Spacer(1, 6))

        tx_table_data = [
            ["ID", "Data", "Typ", "Kwota", "Waluta", "Kategoria", "Opis", "Konto ID", "Nazwa Konta"]
        ]
        for t in txs:
            tx_table_data.append([
                t.id,
                t.date.strftime("%Y-%m-%d"),
                t.type,
                f"{t.amount:,.2f}",
                t.currency,
                t.category or "",
                t.description or "",
                t.account_id,
                t.account.name
            ])

        t_tx = Table(tx_table_data, hAlign="LEFT", repeatRows=1)
        t_tx.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (3, 1), (3, -1), "RIGHT"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
            ])
        )
        elements.append(t_tx)

        doc.build(elements)
        return os.path.abspath(path)
