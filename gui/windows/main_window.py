from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont
from gui.widgets.transaction_tab import TransactionTable
from gui.widgets.history_tab import historyTable
from gui.widgets.currency_converter import CurrencyConverterTable
from gui.widgets.account_tab import AccountsTable
from gui.widgets.home_tab import OverviewWidget
from gui.widgets.export_tab import ExportTab
from gui.widgets.planned_transaction_tab import PlannedTransactionsTab
from gui.windows.change_password_dialog import ChangePasswordDialog
from gui.widgets.budget_tab import BudgetTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Finance Manager")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.is_menu_expanded = False
        self.init_ui()

    def init_ui(self):

        # Left sidebar for menu
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(75)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)

        # Menu button 
        self.menu_btn = QPushButton()
        self.menu_btn.setObjectName("menu_btn")
        self.menu_btn.setIcon(QIcon("resources/icons/bars-solid.svg"))
        self.menu_btn.setIconSize(QSize(24, 24))
        self.menu_btn.setFixedSize(75, 60)
        self.menu_btn.clicked.connect(self.toggle_menu)
        self.sidebar_layout.addWidget(self.menu_btn)

        # Menu options 
        self.menu_options = QWidget()
        self.menu_options_layout = QVBoxLayout(self.menu_options)
        self.menu_options.setVisible(False)

        # Menu buttons
        self.btn_home = QPushButton("Home/Overview")
        self.btn_home.setObjectName("btn_home")
        self.btn_home.clicked.connect(self.show_home_tab)
        self.btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        self.btn_transactions = QPushButton("Transakcje")
        self.btn_transactions.setObjectName("btn_transactions")
        self.btn_transactions.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.btn_planned_transactions = QPushButton("Zaplanowane Transakcje")
        self.btn_planned_transactions.setObjectName("btn_planned_transactions")
        self.btn_planned_transactions.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        self.btn_budget = QPushButton("Budżet")
        self.btn_budget.setObjectName("btn_budget")
        self.btn_budget.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

        self.btn_accounts = QPushButton("Konta")
        self.btn_accounts.setObjectName("btn_accounts")
        self.btn_accounts.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

        self.btn_currency = QPushButton("Przelicznik walut")
        self.btn_currency.setObjectName("btn_currency")
        self.btn_currency.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))

        self.btn_history = QPushButton("Historia")
        self.btn_history.setObjectName("btn_history")
        self.btn_history.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(6))

        self.btn_export = QPushButton("Eksport")
        self.btn_export.setObjectName("btn_export")
        self.btn_export.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(7))


        for btn in [self.btn_home, self.btn_transactions, self.btn_planned_transactions, self.btn_budget, self.btn_accounts, self.btn_currency, self.btn_history, self.btn_export]:
            btn.setFixedHeight(40)
            self.menu_options_layout.addWidget(btn)

        self.sidebar_layout.addWidget(self.menu_options)
        self.sidebar_layout.addStretch()

        # Bottom icons
        self.account_btn = QPushButton()
        self.account_btn.setObjectName("account_btn")
        self.account_btn.setIcon(QIcon("resources/icons/user-solid.svg"))
        self.account_btn.setIconSize(QSize(24, 24))
        self.account_btn.setFixedSize(75, 60)
        self.sidebar_layout.addWidget(self.account_btn)

        self.settings_btn = QPushButton()
        self.settings_btn.setObjectName("settings_btn")
        self.settings_btn.setIcon(QIcon("resources/icons/gear-solid.svg"))
        self.settings_btn.setIconSize(QSize(24, 24))
        self.settings_btn.setFixedSize(75, 60)
        self.settings_btn.clicked.connect(self.open_change_password)
        self.sidebar_layout.addWidget(self.settings_btn)

        self.stacked_widget = QStackedWidget()

        # ALL TABS
        self.overview_tab = OverviewWidget()
        self.stacked_widget.addWidget(self.overview_tab)

        self.transactions_tab = TransactionTable()
        self.stacked_widget.addWidget(self.transactions_tab)

        self.planned_transactions_tab = PlannedTransactionsTab()
        self.stacked_widget.addWidget(self.planned_transactions_tab)

        self.budget_tab = BudgetTab()
        self.stacked_widget.addWidget(self.budget_tab)

        self.accounts_tab = AccountsTable()
        self.stacked_widget.addWidget(self.accounts_tab)
        self.stacked_widget.currentChanged.connect(self.on_tab_changed)

        self.currency_tab = CurrencyConverterTable()
        self.stacked_widget.addWidget(self.currency_tab)

        self.history_tab = historyTable()
        self.stacked_widget.addWidget(self.history_tab)

        self.export_tab = ExportTab()
        self.stacked_widget.addWidget(self.export_tab)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.stacked_widget, 1)

        content_frame = QWidget()
        content_frame.setLayout(content_layout)

        self.main_layout.addWidget(content_frame, 1)

    def toggle_menu(self):
        self.is_menu_expanded = not self.is_menu_expanded
        if self.is_menu_expanded:
            self.sidebar.setFixedWidth(220)
            self.sidebar.setObjectName("sidebar_expanded")
        else:
            self.sidebar.setFixedWidth(75)
            self.sidebar.setObjectName("sidebar")
        self.sidebar.style().unpolish(self.sidebar)
        self.sidebar.style().polish(self.sidebar)
        self.menu_options.setVisible(self.is_menu_expanded)

    def on_tab_changed(self, index):
        ACCOUNTS_INDEX = 3
        if index == ACCOUNTS_INDEX:
            self.accounts_tab.refresh_accounts()

    def show_home_tab(self):
        self.overview_tab.refresh()
        self.stacked_widget.setCurrentIndex(0)

    def open_change_password(self):
        """
        Metoda wywoływana po kliknięciu ikony USTAWIENIA -> pokazuje 
        dialog ChangePasswordDialog.
        """
        dlg = ChangePasswordDialog(self)
        dlg.exec()