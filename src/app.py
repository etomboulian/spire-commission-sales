import sys
from PySide6.QtWidgets import QApplication, QDialog
from ui.main_window import MainWindow
from ui.login_dialog import LoginDialog
from ui.company_select_dialog import CompanySelectionDialog


def run_application():
    app = QApplication(sys.argv)

    window = MainWindow()

    login_dlg = LoginDialog(window)
    if login_dlg.exec() == QDialog.Accepted:
        company_select_dlg = CompanySelectionDialog(window)
        if company_select_dlg.exec() == QDialog.Accepted:
            window.show()
            app.exec()


if __name__ == '__main__':
    run_application()
