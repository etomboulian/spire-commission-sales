from PySide6.QtWidgets import QDialog, QLabel, QGridLayout, QComboBox, QPushButton


class CompanySelectionDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setUI()

    def select_company(self):
        company_name = self.combobox_select_company.currentText()
        self.parent().api_client = self.parent().api_client.Company(company_name)
        self.accept()

    def setUI(self):
        self.layout = QGridLayout()
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
