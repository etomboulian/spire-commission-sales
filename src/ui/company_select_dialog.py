from PySide6.QtWidgets import QDialog, QLabel, QGridLayout, QComboBox, QPushButton
from PySide6.QtCore import QSize
from PySide6.QtGui import QScreen
from .main_window import font


class CompanySelectionDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Commission Sales App - Select Company")
        self.setSize()
        self.setUI()

    def select_company(self):
        company_name = self.combobox_select_company.currentText()
        self.parent().api_client = self.parent().api_client.Company(company_name)
        self.accept()

    def center(self):
        qr = self.frameGeometry()
        center_point = QScreen().availableGeometry().center()
        qr.moveCenter(center_point)

    def setSize(self):
        window_size = QSize(300, 100)
        self.center()
        self.resize(window_size)

    def setUI(self):
        self.layout = QGridLayout()
        self.setFont(font)

        self.label_select_company = QLabel("Select a company")
        companies_list = self.parent().api_client.Companies.list()

        company_names_list = [
            company.name for company in companies_list.records]

        self.combobox_select_company = QComboBox()
        self.combobox_select_company.addItems(company_names_list)

        self.button_select = QPushButton(text='Select')
        self.button_select.clicked.connect(self.select_company)

        self.button_cancel = QPushButton(text='Cancel')
        self.button_cancel.clicked.connect(self.reject)

        self.layout.addWidget(self.label_select_company, 0, 0)
        self.layout.addWidget(self.combobox_select_company, 0, 1)
        self.layout.addWidget(self.button_select, 1, 0)
        self.layout.addWidget(self.button_cancel, 1, 1)

        self.setLayout(self.layout)
