from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
    QDateEdit,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QCheckBox,
    QDialog
)
from PySide6.QtCore import QSize, QDate, QRect, QSettings
from PySide6.QtGui import QFont, QScreen
from datetime import date, timedelta
import traceback

font = QFont('Arial', 12)


class MainWindowWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.settings = QSettings('Spire-Evan', 'Spire Commission Sales App')
        self.settings_list = ['start_date', 'end_date', 'post_date']
        self.setUI()

    def setUI(self):
        self.setFont(font)

        self.layout = QGridLayout()
        current_settings = self.load_settings(self.settings_list)

        existing_start_date = current_settings.get(
            self.settings_list[0]) if current_settings else None
        existing_end_date = current_settings.get(
            self.settings_list[1]) if current_settings else None
        existing_post_date = current_settings.get(
            self.settings_list[2]) if current_settings else None

        # Start Date Label
        self.label_start_date = QLabel('Start Date')
        self.layout.addWidget(self.label_start_date, 0, 0)

        # Start Date DateEdit field
        self.field_start_date = QDateEdit()
        self.field_start_date.setCalendarPopup(True)
        self.field_start_date.setDisplayFormat("dd-MM-yyyy")

        if existing_start_date:
            self.field_start_date.setDate(QDate(existing_start_date))
        else:
            self.field_start_date.setDate(
                QDate(QDate.year(QDate.currentDate()), 1, 1))
        self.layout.addWidget(self.field_start_date, 0, 1)

        # End date Label
        self.label_end_date = QLabel('End Date')
        self.layout.addWidget(self.label_end_date, 1, 0)

        # End Date DateEdit field
        self.field_end_date = QDateEdit()
        self.field_end_date.setCalendarPopup(True)
        self.field_end_date.setDisplayFormat("dd-MM-yyyy")
        if existing_end_date:
            self.field_end_date.setDate(QDate(existing_end_date))
        else:
            self.field_end_date.setDate(
                QDate(QDate.year(QDate.currentDate()), 1, 1))
        self.layout.addWidget(self.field_end_date, 1, 1)

        # Post Date Label
        self.label_post_date = QLabel('Post Date')
        self.layout.addWidget(self.label_post_date, 2, 0)

        # Post Date DateEdit field
        self.field_post_date = QDateEdit()
        self.field_post_date.setCalendarPopup(True)
        self.field_post_date.setDisplayFormat("dd-MM-yyyy")
        if existing_post_date:
            self.field_post_date.setDate(QDate(existing_post_date))
        else:
            self.field_post_date.setDate(
                QDate(QDate.year(QDate.currentDate()), 1, 1))
        self.layout.addWidget(self.field_post_date, 2, 1)

        # Preview Label
        self.label_preview_post = QLabel("Preview?")
        self.layout.addWidget(self.label_preview_post, 3, 0)

        # Preview Checkbox
        self.checkbox_preview_post = QCheckBox()
        self.layout.addWidget(self.checkbox_preview_post, 3, 1)

        # Post Commissions Button
        self.button_post_commissions = QPushButton()
        self.button_post_commissions.setText('Post Commissions')
        self.button_post_commissions.clicked.connect(
            self.post_commissions)  # .click.connect(self.post_commissions)
        self.layout.addWidget(self.button_post_commissions, 4, 0, 1, 2)

        self.setLayout(self.layout)

    def save_settings(self, saveSettings):
        for key, value in saveSettings.items():
            self.settings.setValue(key, value)

    def load_settings(self, setting_list):
        settings = {}
        for setting in setting_list:
            if self.settings.contains(setting):
                setting_value = self.settings.value(setting)
                settings[setting] = setting_value
        return settings

    def post_commissions(self):
        def validate(start_date, end_date, post_date):
            if start_date < (date.today() - timedelta(days=730)):
                raise Exception("Start Date is more than 2 years in the past")
            if end_date < (date.today() - timedelta(days=730)):
                raise Exception("End Date is more than 2 years in the past")
            if post_date < (date.today() - timedelta(days=730)):
                raise Exception("Post Date is more than 2 years in the past")

        try:

            start_date = self.field_start_date.date().toPython()
            end_date = self.field_end_date.date().toPython()
            post_date = self.field_post_date.date().toPython()
            is_trial = self.checkbox_preview_post.isChecked()

            self.save_settings({
                self.settings_list[0]: start_date,
                self.settings_list[1]: end_date,
                self.settings_list[2]: post_date
            })

            validate(start_date, end_date, post_date)

            from commission import create_commission_sales_orders
            orders = create_commission_sales_orders(
                self.parent().api_client,
                start_date,
                end_date,
                post_date,
                trial=is_trial
            )

            # Now show a dialog with the created orders?
            results_dlg = QMessageBox(self)
            results_dlg.setWindowTitle('Results')
            if is_trial:
                results_dlg.setText(str(orders))
            else:
                results_dlg.setText(str(orders))
            output_text = results_dlg.exec()

        except Exception as e:
            traceback.print_exc()
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Error')
            dlg.setText(str(e))
            button = dlg.exec()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Commission Sales App")
        self.setSize()
        self.setUI()

    def setUI(self):
        self.widget = MainWindowWidget(self)
        self.setCentralWidget(self.widget)

    def center(self):
        qr = self.frameGeometry()
        center_point = QScreen().availableGeometry().center()
        qr.moveCenter(center_point)

    def setSize(self):
        window_size = QSize(360, 210)
        self.center()
        self.resize(window_size)
