import os
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from core.repositories.export_repository import ExportRepository


class ExportController:
    def __init__(self, repository: ExportRepository = None):
        self.repo = repository or ExportRepository()

    def export_all_excel(self, path: str) -> str:
        if not path.lower().endswith(".xlsx"):
            path += ".xlsx"

        accounts = self.repo.fetch_accounts()
        transactions = self.repo.fetch_transactions()

        df_accounts = pd.DataFrame([{
            "ID": a.id,
            "Name": a.name,
            "Balance": round(a.balance or 0, 2),
            "Type": a.type,
        } for a in accounts])

        df_txs = pd.DataFrame([{
            "ID": t.id,
            "Date": t.date.strftime("%Y-%m-%d"),
            "Type": t.type,
            "Amount": round(t.amount, 2),
            "Currency": t.currency,
            "Category": t.category or "",
            "Description": t.description or "",
            "Account_ID": t.account_id,
            "Account_Name": t.account.name,
        } for t in transactions])

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

            for sheet_name, df in [("Accounts", df_accounts), ("Transactions", df_txs)]:
                worksheet = writer.sheets[sheet_name]
                for col_num, col in enumerate(df.columns):
                    worksheet.set_column(col_num, col_num, 15)
                    worksheet.write(0, col_num, col, header_format)

        return os.path.abspath(path)

    def export_pdf(self, path: str) -> str:
        if not path.lower().endswith(".pdf"):
            path += ".pdf"

        accounts = self.repo.fetch_accounts()
        transactions = self.repo.fetch_transactions()

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
        elements.extend([
            Paragraph("Raport Finansowy", title_style),
            Paragraph(f"Data wygenerowania: {now_str}", date_style),
            Spacer(1, 12),
        ])

        # Accounts
        elements.append(Paragraph("Konta:", styles["Heading2"]))
        elements.append(Spacer(1, 6))
        acc_data = [["ID", "Nazwa", "Saldo", "Typ"]] + [
            [a.id, a.name, f"{a.balance:,.2f} zł", a.type] for a in accounts
        ]
        t_acc = Table(acc_data, hAlign="LEFT", repeatRows=1)
        t_acc.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (2, 1), (2, -1), "RIGHT"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, 0), 11),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ]))
        elements.append(t_acc)
        elements.append(PageBreak())

        # Transactions
        elements.append(Paragraph("Transakcje:", styles["Heading2"]))
        elements.append(Spacer(1, 6))
        tx_data = [["ID", "Data", "Typ", "Kwota", "Waluta", "Kategoria", "Opis", "Konto ID", "Nazwa Konta"]] + [
            [t.id, t.date.strftime("%Y-%m-%d"), t.type, f"{t.amount:,.2f}", t.currency,
             t.category or "", t.description or "", t.account_id, t.account.name]
            for t in transactions
        ]
        t_tx = Table(tx_data, hAlign="LEFT", repeatRows=1)
        t_tx.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (3, 1), (3, -1), "RIGHT"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ]))
        elements.append(t_tx)

        doc.build(elements)
        return os.path.abspath(path)
