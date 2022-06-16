from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QDialogButtonBox,
    QMessageBox
)

from PySide6.QtCore import QSize
from PySide6.QtGui import QFont, QScreen
from spire_client import Server as ApiClient
from .main_window import font


class LoginDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Commission Sales App - Login")
        self.set_size_and_position()
        self.setUI()

    def do_login(self):
        hostname = self.field_hostname.text()
        port = self.field_port.text()
        username = self.field_username.text()
        password = self.field_password.text()

        try:
            self.parent().api_client = ApiClient(hostname, username, password, port=port)
            self.accept()
        except Exception as e:
            # Bubble up any exceptions on login to the UI
            error_dlg = QMessageBox(self)
            error_dlg.setWindowTitle('Error')
            error_dlg.setText(str(e))
            error_dlg.exec()

    def center(self):
        qr = self.frameGeometry()
        center_point = QScreen().availableGeometry().center()
        qr.moveCenter(center_point)

    def set_size_and_position(self):
        window_size = QSize(300, 200)
        self.center()
        self.resize(window_size)

    def setUI(self):
        self.setFont(font)

        #self.setStyleSheet("QLabel {font: Arial 12pt}")
        self.layout = QGridLayout()

        self.label_hostname = QLabel("Hostname")
        self.field_hostname = QLineEdit()

        self.label_port = QLabel("Port")
        self.field_port = QLineEdit(text='10880')

        self.label_username = QLabel("Username")
        self.field_username = QLineEdit()

        self.label_password = QLabel("Password")
        self.field_password = QLineEdit()
        self.field_password.setEchoMode(QLineEdit.Password)

        self.button_login = QPushButton(text="Login")
        self.button_login.clicked.connect(self.do_login)

        self.button_cancel = QPushButton(text="Cancel")
        self.button_cancel.clicked.connect(self.reject)

        self.layout.addWidget(self.label_hostname, 0, 0)
        self.layout.addWidget(self.field_hostname, 0, 1)

        self.layout.addWidget(self.label_port, 1, 0)
        self.layout.addWidget(self.field_port, 1, 1)

        self.layout.addWidget(self.label_username, 2, 0)
        self.layout.addWidget(self.field_username, 2, 1)

        self.layout.addWidget(self.label_password, 3, 0,)
        self.layout.addWidget(self.field_password, 3, 1)

        self.layout.addWidget(self.button_login, 4, 0)
        self.layout.addWidget(self.button_cancel, 4, 1)

        self.setLayout(self.layout)
