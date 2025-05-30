from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QLabel, QSizePolicy, QFrame
from PyQt6.QtCore import Qt
from core.controllers.overview_controller import OverviewController
from datetime import date

# Matplotlib for charts
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class OverviewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ctrl = OverviewController()
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        main_layout.addWidget(self.scroll)

        self.container = QWidget()
        self.scroll.setWidget(self.container)

        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setSpacing(20)
        self.container_layout.setContentsMargins(10,10,10,10)

        self.build_content()

    def build_content(self):
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.container_layout.addWidget(self._create_balance_card())

        today = date.today()
        inc, exp = self.ctrl.month_summary(today.year, today.month)
        period = today.strftime("%B %Y")
        self.container_layout.addWidget(
            self._create_month_summary_card("Obecny miesiąc", inc, exp, period)
        )

        prev_month = today.month-1 or 12
        prev_year = today.year if today.month>1 else today.year-1
        inc2, exp2 = self.ctrl.month_summary(prev_year, prev_month)
        prev_period = date(prev_year, prev_month, 1).strftime("%B %Y")
        self.container_layout.addWidget(
            self._create_month_summary_card("Poprzedni miesiąc", inc2, exp2, prev_period)
        )

        data_line  = self.ctrl.yearly_balance_trend()
        line_chart = self._make_line_chart(data_line)
        self.container_layout.addWidget(QLabel("<b>Trend bilansu w roku</b>",
                                      alignment=Qt.AlignmentFlag.AlignCenter))
        self.container_layout.addWidget(line_chart)

        data_bar   = self.ctrl.weekly_flow()
        bar_chart  = self._make_bar_chart(data_bar)
        self.container_layout.addWidget(QLabel("<b>Przychody i wydatki (ostatni tydzień)</b>",
                                      alignment=Qt.AlignmentFlag.AlignCenter))
        self.container_layout.addWidget(bar_chart)

        self.container_layout.addWidget(
            self._create_transaction_preview()
        )

    def refresh(self):
        self.ctrl = OverviewController()
        self.build_content()

    def _create_balance_card(self):
        frame = QFrame()
        frame.setStyleSheet("background-color:#333; padding:10px; border-radius:5px;")
        layout = QVBoxLayout(frame)

        bal = self.ctrl.total_balance()
        color = 'green' if bal>=0 else 'red'
        lbl = QLabel(f"Bilans: <b>{bal:,.2f} zł</b>")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet(f"font-size:24px; color:{color};")
        layout.addWidget(lbl)

        breakdown = QHBoxLayout()
        for acc in self.ctrl.acc_ctrl.list_accounts():
            sub = QFrame()
            sub.setStyleSheet("background-color:#444; padding:5px; border-radius:3px;")
            sl = QVBoxLayout(sub)
            sl.addWidget(QLabel(f"{acc.name}: <b>{acc.balance:,.2f} zł</b>"))
            breakdown.addWidget(sub)
        layout.addLayout(breakdown)
        return frame

    def _create_month_summary_card(self, title, inc, exp, period):
        frame = QFrame()
        frame.setStyleSheet("background-color:#333; padding:5px; border-radius:5px;")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(5,5,15,5)
        layout.setSpacing(5)

        text_widget = QWidget()
        text_widget.setFixedWidth(180)
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(0,0,0,0)
        text_layout.setSpacing(2)

        text_layout.addWidget(QLabel(f"<b>{title}</b> ({period})"))
        text_layout.addWidget(QLabel(f"Przychód: <font color='green'>{inc:,.2f} zł</font>"))
        text_layout.addWidget(QLabel(f"Wydatki: <font color='red'>{exp:,.2f} zł</font>"))
        diff = inc - exp
        txt_color = 'green' if diff >= 0 else 'red'
        text_layout.addWidget(QLabel(f"Wynik: <font color='{txt_color}'>{diff:,.2f} zł</font>"))
        text_layout.addStretch()

        layout.addWidget(text_widget) 
        
        layout.addStretch()

        fig = Figure(figsize=(4.5,2.5), dpi=100)
        ax = fig.add_subplot(111)
        fig.set_facecolor('#333')
        ax.set_facecolor('#333')
        total = inc + exp
        if total > 0:
            wedges, _, autotexts = ax.pie(
                [inc, exp],
                colors=['#4caf50', '#f44336'],
                autopct='%1.1f%%',
                startangle=90,
                labels=['',''],
                pctdistance=0.7,
                textprops={'color':'white','fontsize':11}
            )
            ax.legend(
                wedges,
                ["Przychód", "Wydatki"],
                loc="center left",
                bbox_to_anchor=(0.75,0.75),
                frameon=False,
                labelcolor='white',
                fontsize=9
                
            )
        else:
            ax.text(0.5,0.5,"Brak danych",ha='center',va='center',color='white')

        ax.axis('equal')
        
        fig.tight_layout(pad=1.0)

        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(canvas, 1)

        return frame


    def _make_line_chart(self, data):
        fig = Figure(figsize=(5,2))
        ax = fig.add_subplot(111)
        ax.set_facecolor('#222'); fig.set_facecolor('#222')
        xs = [d.strftime("%b") for d,v in data]
        ys = [v for d,v in data]
        all_months = [date(date.today().year, m,1).strftime("%b") for m in range(1,13)]
        ys_full = []
        data_dict = {d.strftime("%b"):v for d,v in data}
        for mon in all_months:
            ys_full.append(data_dict.get(mon,0))
        ax.plot(all_months, ys_full, marker='o', color='cyan')
        ax.fill_between(all_months, ys_full, alpha=0.1, color='cyan')
        ax.set_ylabel("Saldo", color='white')
        ax.tick_params(colors='white')
        fig.tight_layout()
        fc = FigureCanvas(fig)
        fc.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        return fc

    def _make_bar_chart(self, data):
        fig = Figure(figsize=(5,2))
        ax = fig.add_subplot(111)
        ax.set_facecolor('#222'); fig.set_facecolor('#222')
        xs = [d.strftime("%d.%m") for d,inc,exp in data]
        incs = [inc for d,inc,exp in data]
        exps = [exp for d,inc,exp in data]
        w=0.4
        ax.bar([i-w/2 for i in range(len(xs))], incs, width=w, color='#4caf50', label='Przychód')
        ax.bar([i+w/2 for i in range(len(xs))], exps, width=w, color='#f44336', label='Wydatki')
        ax.set_xticks(range(len(xs))); ax.set_xticklabels(xs, rotation=45, color='white')
        ax.tick_params(colors='white'); ax.legend()
        fig.tight_layout()
        bc = FigureCanvas(fig)
        bc.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        return bc

    def _create_transaction_preview(self):
        frame = QFrame()
        frame.setStyleSheet("background-color:#333; padding:10px; border-radius:5px;")
        layout = QVBoxLayout(frame)
        layout.addWidget(QLabel("<b>Ostatnie transakcje</b>", alignment=Qt.AlignmentFlag.AlignCenter))

        txs = self.ctrl.recent_transactions(7)
        for t in txs:
            h = QHBoxLayout()
            desc = t.category or t.description or ""
            h.addWidget(QLabel(f"{desc} ({t.date.strftime('%d/%m/%Y')})"))
            amt = t.amount if t.type == 'Przychód' else -t.amount
            clr = 'green' if amt >= 0 else 'red'
            lab = QLabel(f"<font color='{clr}'>{amt:,.2f} zł</font>")
            h.addWidget(lab, alignment=Qt.AlignmentFlag.AlignRight)
            layout.addLayout(h)
        return frame
