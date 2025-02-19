from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget
from datetime import datetime, timedelta
from PyQt6.QtCore import Qt, QDate
from pages.buyerProfileView import BuyerProfileView
from features.data_save_signals import data_save_signals
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ui.buyerProfiles_ui import buyerProfiles_ui
from models import UserModel, BuyerProfileModel, SettingModel
from features.printmemo import Print_Form
from PyQt6 import QtWidgets, QtGui, QtPrintSupport
from PyQt6.QtWidgets import QFileDialog
import xlsxwriter
from PyQt6.QtGui import QFont, QFontDatabase

class buyerProfiles(QWidget):
    def __init__(self, username):

        super().__init__()
        self.username = username
        self.setup_database()  # First setup database
        self.ui = buyerProfiles_ui()
        self.ui.setupUi(self)
        self.setup_ui()
        session = self.Session()
        user = session.query(UserModel).filter(UserModel.username==self.username).one()
        self.user_role = user.role



    def setup_ui(self):
        self.ui.tableWidget.horizontalHeader().setDefaultSectionSize(135)
        self.ui.tableWidget.horizontalHeader().setMinimumSectionSize(135)
        self.ui.tableWidget.verticalHeader().setVisible(False)

        # Set current date ****************
        self.ui.startDateInput.setDisplayFormat("dd/MM/yyyy")
        self.ui.endDateInput.setDisplayFormat("dd/MM/yyyy")
        self.today_date_raw = datetime.now()
        self.today_date = self.today_date_raw.strftime("%d/%m/%Y").lstrip('0').replace('/0', '/')
        self.qdate_today = QDate.fromString(self.today_date, "d/M/yyyy")
        self.ui.startDateInput.setDate(self.qdate_today)
        self.ui.endDateInput.setDate(self.qdate_today)

        data_save_signals.data_saved.connect(self.filter_data)
        self.filter_data()
        self.ui.filterBtn.clicked.connect(self.filter_data)

        # ************ Autocomplete *****************************
        self.auto_completer()
        data_save_signals.data_saved.connect(lambda: self.auto_completer())
        # *************** end autocomplete *******************************
        self.ui.buyerFilterInput.textChanged.connect(lambda : self.make_capital(self.ui.buyerFilterInput))

        session = self.Session()
        user = session.query(UserModel).filter(UserModel.username==self.username).one()
        self.user_role = user.role

        self.ui.printBtn.clicked.connect(self.openPrintMemo)
        self.ui.saveBtn.clicked.connect(self.save_xlsx)

        self.apply_bangla_font() # apply bangla font first
        self.update_setting_font()
        data_save_signals.data_saved.connect(self.update_setting_font)

    def apply_bangla_font(self):
        bangla_font_path = "font/nato.ttf"
        font_id = QFontDatabase.addApplicationFont(bangla_font_path)
        custom_font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(custom_font_family, 13)  # Font size 14
        self.ui.tableWidget.horizontalHeader().setFont(custom_font)
        self.ui.tableWidget.verticalHeader().setFont(custom_font)
        self.ui.startDateLabel.setFont(custom_font)
        self.ui.endDateLabel.setFont(custom_font)
        self.ui.filterLabel.setFont(custom_font)
        self.ui.filterBtn.setFont(custom_font)
        self.ui.saveBtn.setFont(custom_font)
        self.ui.printBtn.setFont(custom_font)

    def update_setting_font(self):
        session = self.Session()
        setting = session.query(SettingModel).first()
        bangla_font_path = "font/nato.ttf"
        english_font_path = "font/arial.ttf"
        # Load the appropriate font
        if setting.font == "Bangla":
            font_id = QFontDatabase.addApplicationFont(bangla_font_path)
            custom_font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            custom_font = QFont(custom_font_family, 12)  # Font size 12
        else:
            font_id = QFontDatabase.addApplicationFont(english_font_path)
            custom_font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            custom_font = QFont(custom_font_family, 12)  # Font size 12

        from features.bangla_typing import enable_bangla_typing
        self.ui.buyerFilterInput.setFont(custom_font)
        enable_bangla_typing(self.ui.buyerFilterInput, setting.font)

    def setup_database(self):
        self.Base = declarative_base()
        self.engine = create_engine('sqlite:///business.db')
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def auto_completer(self):
        """Refresh the QCompleter with the latest seller names."""
        self.all_name = self.get_all_names()
        self.completer = QtWidgets.QCompleter(self.all_name, self)    # QT object parameter memoPageMain
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui.buyerFilterInput.setCompleter(self.completer)   # change input field

    def get_all_names(self):
        """Fetch all seller names from the database for autocomplete."""
        session = self.Session()
        name_entires = session.query(BuyerProfileModel).all()     # change Model name
        session.close()
        return [name_entry.buyer_name for name_entry in name_entires]    # change field name

    def make_capital(self, element):
        element.textChanged.disconnect()
        element.setText(element.text().title())
        element.textChanged.connect(lambda: self.make_capital(element))

    def filter_data(self):
        try:
            start_date = self.ui.startDateInput.date().toPyDate()
            start_date = start_date - timedelta(days=7)
            end_date = self.ui.endDateInput.date().toPyDate()
            buyer_filter = self.ui.buyerFilterInput.text()


            # Retrieve data from the database
            session = self.Session()
            query = session.query(BuyerProfileModel).filter(BuyerProfileModel.date.between(start_date, end_date))
            query = query.filter(BuyerProfileModel.buyer_name.ilike(f"%{buyer_filter}%"))
            buyers = query.all()
            # Clear existing table data
            self.ui.tableWidget.clearContents()
            self.ui.tableWidget.setRowCount(0)

            # Populate the table with queried data
            row = 0
            for buyer in buyers:
                self.ui.tableWidget.insertRow(row)
                self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(buyer.id)))
                self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(buyer.buyer_name)))
                self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(buyer.phone)))
                self.ui.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(buyer.buyer_rank)))
                self.ui.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(buyer.total_payable)))
                self.ui.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(buyer.total_paid)))
                self.ui.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(buyer.date)))
                self.ui.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(str(buyer.entry_by)))

                # Add a delete button in the last column
                view_button = QtWidgets.QPushButton("")
                view_icon = QtGui.QIcon("./images/view.png")  # Path to your delete icon
                view_button.setIcon(view_icon)
                view_button.setIconSize(QtCore.QSize(24, 24))  # Set icon size if needed
                view_button.setStyleSheet("background-color: white; border: none;margin-left:50px;")  # Set wh
                view_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                view_button.clicked.connect(lambda _, seller_name=buyer.buyer_name: self.view_profile(seller_name))
                self.ui.tableWidget.setCellWidget(row, 8, view_button)

                delete_button = QtWidgets.QPushButton("")
                delete_icon = QtGui.QIcon("./images/delete.png")  # Path to your delete icon
                delete_button.setIcon(delete_icon)
                delete_button.setIconSize(QtCore.QSize(24, 24))  # Set icon size if needed
                delete_button.setStyleSheet("background-color: white; border: none;margin-left:50px;")  # Set wh
                delete_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                delete_button.clicked.connect(lambda _, r=row: self.delete_row(r))
                self.ui.tableWidget.setCellWidget(row, 9, delete_button)
                row += 1

        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Buyer Profile Error:", f"An error occurred while filtering data: {e}")

    def delete_row(self, row):
        if self.user_role == "editor":
            QtWidgets.QMessageBox.warning(None, "Delete Error", f"এই প্রোফাইলে ডিলিট করার একসেস নেই..")
            return
        try:
            reply = QtWidgets.QMessageBox.question(
                None,
                'মুছে ফেলা নিশ্চিত করুন',
                'আপনি কি নিশ্চিত যে আপনি এই প্রোফাইল মুছে ফেলতে চান?',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No
            )

            # If the user confirms, proceed with deletion
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                entry_id = self.ui.tableWidget.item(row, 0).text()
                session = self.Session()
                session.query(BuyerProfileModel).filter(BuyerProfileModel.id == entry_id).delete()
                session.commit()
                self.ui.tableWidget.removeRow(row)
        except Exception as ops:
            print(f'error in delete of buyer profile: ({ops})')
        data_save_signals.data_saved.emit()

    def view_profile(self, buyer_name):
        try:
            session = self.Session()
            self.transactions_window = BuyerProfileView(buyer_name, session)
            self.transactions_window.show()
        except Exception as e:
            print(f' err o : {str(e)}')



    def openPrintMemo(self):
        try:
            # ✅ Create the print window
            self.ui_print_form = Print_Form()
            self.ui_print_form.ui.memoLabel.setText("ক্রেতাদের প্রোফাইল")

            # ✅ Define columns to exclude
            excluded_columns = {0, 2, 3, 7, 8, 9}
            column_count = self.ui.tableWidget.columnCount()
            row_count = self.ui.tableWidget.rowCount()
            headers = [self.ui.tableWidget.horizontalHeaderItem(i).text() for i in range(column_count) if
                       i not in excluded_columns]

            self.ui_print_form.ui.tableWidget.verticalHeader().setVisible(False)
            self.ui_print_form.ui.tableWidget.setColumnCount(len(headers))
            self.ui_print_form.ui.tableWidget.setHorizontalHeaderLabels(headers)
            self.ui_print_form.ui.tableWidget.setRowCount(row_count)

            self.ui_print_form.ui.recevied_frame.setVisible(False)

            # ✅ Copy table data excluding specified columns
            for row_idx in range(row_count):
                new_col_idx = 0
                for col_idx in range(column_count):
                    if col_idx in excluded_columns:
                        continue  # Skip excluded columns
                    item = self.ui.tableWidget.item(row_idx, col_idx)
                    if item:
                        self.ui_print_form.ui.tableWidget.setItem(row_idx, new_col_idx, QtWidgets.QTableWidgetItem(item.text()))
                    new_col_idx += 1

            # ✅ Show the print window
            self.ui_print_form.show()

            # ✅ Set up the printer
            printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.PrinterMode.HighResolution)
            printer.setPageSize(QtGui.QPageSize(QtGui.QPageSize.PageSizeId.A4))  # Set paper size to A4

            # ✅ Open print preview dialog
            preview_dialog = QtPrintSupport.QPrintPreviewDialog(printer)
            preview_dialog.paintRequested.connect(self.renderPrintPreview)  # Connect to the custom render function
            preview_dialog.exec()

        except Exception as e:
            print(f"An error occurred: {e}")

    def renderPrintPreview(self, printer):
        """
        Custom function to render the print window content for the preview.
        """
        try:
            # ✅ Use QPainter to render the print content
            painter = QtGui.QPainter(printer)

            # ✅ Improve rendering quality
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

            # ✅ Calculate the scaling factor
            dpi_x = printer.logicalDpiX()  # Printer DPI in X direction
            dpi_y = printer.logicalDpiY()  # Printer DPI in Y direction
            scale_x = dpi_x / 96.0  # Assume screen DPI is 96
            scale_y = dpi_y / 96.0

            # ✅ Apply scaling to the painter
            painter.scale(scale_x, scale_y)

            # ✅ Render the print window content
            self.ui_print_form.render(painter)

            # ✅ Finish painting
            painter.end()

        except Exception as e:
            print(f"An error occurred during print preview: {e}")



    def save_xlsx(self):
        try:
            # Open a file dialog to select the location to save the Excel file
            file_path, _ = QFileDialog.getSaveFileName(
                None,  # Use the actual QWidget as the parent
                "Save Excel File",
                "",
                "Excel Files (*.xlsx);;All Files (*)"
            )

            # If no file is selected, return early
            if not file_path:
                return

            # Ensure the file has the correct extension
            if not file_path.endswith(".xlsx"):
                file_path += ".xlsx"

            # Create an Excel file using xlsxwriter
            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet("Table Data")

            # Retrieve data from the tableWidget
            row_count = self.ui.tableWidget.rowCount()
            column_count = self.ui.tableWidget.columnCount()

            # Write headers to the first row
            headers = [self.ui.tableWidget.horizontalHeaderItem(i).text() for i in range(column_count)]
            for col_idx, header in enumerate(headers):
                worksheet.write(0, col_idx, header)

            # Write table data to the worksheet
            for row_idx in range(row_count):
                for col_idx in range(column_count):
                    item = self.ui.tableWidget.item(row_idx, col_idx)
                    worksheet.write(row_idx + 1, col_idx, item.text() if item else "")

            # Close and save the workbook
            workbook.close()
            print(f"Excel file saved successfully at {file_path}")

        except Exception as e:
            print(f"An error occurred while saving Excel file: {e}")