from PyQt6 import QtCore
from forms.add_buyer_form import AddBuyer_Form
from PyQt6.QtCore import QDate, Qt
from datetime import datetime
from models import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from features.data_save_signals import data_save_signals
from features.printmemo import Print_Form
from PyQt6 import QtWidgets, QtGui, QtPrintSupport
from PyQt6.QtWidgets import QFileDialog
import xlsxwriter
from PyQt6.QtGui import QFont, QFontDatabase  # for font file load
from ui.memoPage_ui import Ui_memoPageMain
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt


class memoPage(QWidget):
    def __init__(self, username):

        super().__init__()
        self.username = username
        self.setup_database()  # First setup database
        self.ui = Ui_memoPageMain()
        self.ui.setupUi(self)
        self.setup_ui()
        session = self.Session()
        user = session.query(UserModel).filter(UserModel.username == self.username).one()
        self.entry_by = user.role


    def setup_database(self):
        self.Base = declarative_base()
        self.engine = create_engine('sqlite:///business.db')
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def setup_ui(self):
        self.ui.voucharInput.setDisabled(True)
        self.ui.voucharInput.setStyleSheet("background-color:#E1E1E1")
        self.ui.tableWidget.horizontalHeader().setDefaultSectionSize(180)
        self.ui.tableWidget.horizontalHeader().setMinimumSectionSize(180)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.mosqueInput.setText('10')
        self.ui.somitiInput.setText('10')
        self.ui.otherInput.setText('0')

        # Set current date ****************
        self.ui.sellingDateInput.setDisplayFormat("dd/MM/yyyy")
        self.ui.today_date_raw = datetime.now()
        self.ui.today_date = self.ui.today_date_raw.strftime("%d/%m/%Y").lstrip('0').replace('/0', '/')
        self.ui.qdate_today = QDate.fromString(self.ui.today_date, "d/M/yyyy")
        self.ui.sellingDateInput.setDate(self.ui.qdate_today)

        # open seller dialog
        self.ui.addBuyerBtn.clicked.connect(self.open_seller_information)

        # Update Cost change by user interact    **********************************
        self.ui.commissionInput.textChanged.connect(self.change_in_cost_section)
        self.ui.somitiInput.textChanged.connect(self.change_in_cost_section)
        self.ui.mosqueInput.textChanged.connect(self.change_in_cost_section)
        self.ui.otherInput.textChanged.connect(self.change_in_cost_section)

        # Total taka or total cost update
        self.ui.totalTakaInput.textChanged.connect(self.change_in_total_taka)
        self.ui.totalCostInput.textChanged.connect(self.change_in_total_taka)

        # final taka or paying taka update
        self.ui.finalTakaInput.textChanged.connect(self.change_in_final_taka)
        self.ui.sellerPaidTakaInput.textChanged.connect(self.change_in_final_taka)

        # if change cell price   ****************************************************
        self.ui.tableWidget.itemChanged.connect(self.handle_change_in_fish_price_column)
        # This signal is passing to when adding new buyer

        # ************ Autocomplete *****************************
        self.auto_completer()
        data_save_signals.data_saved.connect(lambda: self.auto_completer)
        # *************** end autocomplete *******************************

        # self.sellerNameInput.textChanged.connect(lambda:self.make_capital(self.sellerNameInput))

        self.commision = ''
        self.commision_call()
        data_save_signals.data_saved.connect(self.commision_call)

        self.ui.printBtn.clicked.connect(self.openPrintMemo)
        self.ui.saveExcelBtn.clicked.connect(self.save_xlsx)

        # save all data
        self.ui.save_db_Btn.clicked.connect(self.save_data)

        self.apply_bangla_font()
        self.update_setting_font()
        data_save_signals.data_saved.connect(self.update_setting_font)
        self.update_voucher()


    def update_voucher(self):
        session = self.Session()
        last_voucher = session.query(VoucherNoModel).order_by(VoucherNoModel.voucher_no.desc()).first()
        if not last_voucher:
            next_voucher_no = 1
        else:
            next_voucher_no = last_voucher.voucher_no + 1
        self.ui.voucharInput.setText(str(next_voucher_no))
        session.close()

    def apply_bangla_font(self):
        bangla_font_path = "font/nato.ttf"
        font_id = QFontDatabase.addApplicationFont(bangla_font_path)
        custom_font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(custom_font_family, 13)  # Font size 14
        self.ui.tableWidget.horizontalHeader().setFont(custom_font)
        self.ui.tableWidget.verticalHeader().setFont(custom_font)
        self.ui.voucharLabel.setFont(custom_font)
        self.ui.sellerNameLabel.setFont(custom_font)
        self.ui.sellerAddresslabel.setFont(custom_font)
        self.ui.sellingDatelabel.setFont(custom_font)
        self.ui.sellerMobilelabel.setFont(custom_font)
        self.ui.addBuyerBtn.setFont(custom_font)
        self.ui.commissionLabel.setFont(custom_font)
        self.ui.mosqueLabel.setFont(custom_font)
        self.ui.somitiLabel.setFont(custom_font)
        self.ui.otherLabel.setFont(custom_font)
        self.ui.totalTakaLabel.setFont(custom_font)
        self.ui.totalCostLabel.setFont(custom_font)
        self.ui.finalTakaLabel.setFont(custom_font)
        self.ui.sellerPaidTakaLabel.setFont(custom_font)
        self.ui.remainTakaLabel.setFont(custom_font)
        self.ui.save_db_Btn.setFont(custom_font)
        self.ui.saveExcelBtn.setFont(custom_font)
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
        self.ui.sellerNameInput.setFont(custom_font)
        self.ui.sellerAddressInput.setFont(custom_font)
        enable_bangla_typing(self.ui.sellerNameInput, setting.font)
        enable_bangla_typing(self.ui.sellerAddressInput, setting.font)

    # work with QFontComboBox
    # def update_setting_font(self):
    #     session = Session()
    #     setting = session.query(SettingModel).first()
    #     self.setting_font = QtGui.QFont()
    #     self.setting_font.setFamily(setting.font)
    #     self.setting_font.setPointSize(12)
    #     self.sellerNameInput.setFont(self.setting_font)
    #     self.sellerAddressInput.setFont(self.setting_font)

    def auto_completer(self):
        self.completer = QtWidgets.QCompleter(self.get_all_names(), self)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui.sellerNameInput.setCompleter(self.completer)
        self.completer.activated.connect(lambda text: self.fill_seller_info(text))
    def get_all_names(self):
        """Fetch all seller names from the database for autocomplete."""
        session = self.Session()
        name_entires = session.query(SellerProfileModel).all()
        session.close()
        return [name_entry.seller_name for name_entry in name_entires]
    def fill_seller_info(self, name):
        session = self.Session()
        name_model = session.query(SellerProfileModel).filter_by(seller_name=name).first()
        self.ui.sellerAddressInput.setText(name_model.address)
        self.ui.sellerMobileInput.setText(name_model.phone)
        session.close()



    def commision_call(self):
        session = self.Session()
        setting = session.query(SettingModel).first()
        self.commision = (1/100) * setting.commission
        session.close()


    # Dynamic make capital event pass
    def make_capital(self, element):
        element.textChanged.disconnect()
        element.setText(element.text().title())
        element.textChanged.connect(lambda: self.make_capital(element))


    ## Open dialog to get seller information *************
    def open_seller_information(self):
        # Create and show the SellerInformation dialog
        self.seller_form_ui = AddBuyer_Form(self.username)
        self.seller_form_ui.setWindowTitle("Add Buyer")
        self.seller_form_ui.ui.addBtn.clicked.connect(self.handle_and_accept_information)
        self.seller_form_ui.ui.cancelBtn.clicked.connect(self.seller_form_ui.close)
        self.seller_form_ui.exec()

    def handle_and_accept_information(self):
        success, error_message = self.seller_form_ui.handle_name_entry()
        if success:
            self.accept_information()
        else:
            error_dialog = QtWidgets.QMessageBox(self.seller_form_ui)
            error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Input Error")
            error_dialog.setText(error_message)
            error_dialog.exec()
    def accept_information(self):
        try:
            # Handle the information acceptance logic here
            buyer_name = self.seller_form_ui.ui.buyerName.text().strip()
            buyer_phone = self.seller_form_ui.ui.mobile.text().strip()
            fish_name = self.seller_form_ui.ui.fishName.text().strip()
            fish_rate = self.seller_form_ui.ui.fishRate.text().strip()
            raw_weight = self.seller_form_ui.ui.rawWeight.text().strip()
            final_weight = self.seller_form_ui.ui.finalWeight.text().strip()
            total_price = self.seller_form_ui.ui.totalPrice.text().strip()

            # Check if all fields are filled
            if buyer_name and fish_name and total_price:
                if total_price.isdigit():
                    row_position = self.ui.tableWidget.rowCount()
                    self.ui.tableWidget.insertRow(row_position)
                    # Create table items for buyer_name and fish_name
                    buyer_item = QtWidgets.QTableWidgetItem(buyer_name)
                    fish_item = QtWidgets.QTableWidgetItem(fish_name)
                    # Add the items with fonts to specific columns
                    self.ui.tableWidget.setItem(row_position, 0, buyer_item)
                    self.ui.tableWidget.setItem(row_position, 1, fish_item)
                    self.ui.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(fish_rate))
                    self.ui.tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(raw_weight))
                    self.ui.tableWidget.setItem(row_position, 4, QtWidgets.QTableWidgetItem(final_weight))
                    self.ui.tableWidget.setItem(row_position, 5, QtWidgets.QTableWidgetItem(total_price))

                    # Add a delete button in the last column
                    delete_button = QtWidgets.QPushButton("")
                    delete_icon = QtGui.QIcon("./images/delete.png")  # Path to your delete icon
                    delete_button.setIcon(delete_icon)
                    delete_button.setIconSize(QtCore.QSize(24, 24))  # Set icon size if needed
                    delete_button.setStyleSheet("background-color: white; border: none;margin-left:50px;")  # Set wh
                    delete_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                    delete_button.clicked.connect(lambda _, r=row_position: self.delete_row(r))
                    self.ui.tableWidget.setCellWidget(row_position, 6, delete_button)

                    # Close the dialog
                    self.seller_form_ui.close()
                else:
                    # print("Total price is not a digit.")
                    # Show error message if total_price is not a digit
                    error_dialog = QtWidgets.QMessageBox(self.seller_form_ui)
                    error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    error_dialog.setWindowTitle("Input Error")
                    error_dialog.setText("মোট মূল্য সংখ্যা হতে হবে.")
                    error_dialog.exec()
            else:
                # print("Required fields are empty.")
                # Show error message if any required field is empty
                error_dialog = QtWidgets.QMessageBox(self.seller_form_ui)
                error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                error_dialog.setWindowTitle("Input Error")
                error_dialog.setText("স্টার চিহ্নিত ফিল্ড গুলো অবশ্যই পূরণ করতে হবে.")
                error_dialog.exec()
        except Exception as e:
            print(f"Error in accept_information: {e}")
            error_dialog = QtWidgets.QMessageBox(self.seller_form_ui)
            error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            error_dialog.setWindowTitle("Error")
            # error_dialog.setText(f"An unexpected error occurred: {e}")
            error_dialog.setText(f"ইনভ্যালিড ইনপুট")
            error_dialog.exec()




    # event in price column **************************************
    # int_validation
    def int_v(self, value):
        try:
            return round(float(value.text().strip()) + 0.01)
        except ValueError:
            return 0
    def handle_change_in_fish_price_column(self, item):
        if item.column() == 5:
            self.row_calculate()

    def row_calculate(self):
        def custom_round(value):
            try:
                return round(float(value) + 0.01)
            except ValueError:
                return 0
        total_sum = 0
        row_count = self.ui.tableWidget.rowCount()

        # Calculate the total sum from column 5 cells
        for row in range(row_count):
            cell_item = self.ui.tableWidget.item(row, 5)
            if cell_item and cell_item.text().isdigit():
                total_sum += int(cell_item.text())

        # Update the totalTakaInput field
        self.ui.totalTakaInput.setText(str(total_sum))
        commission_value = custom_round(int(total_sum * self.commision)/10) * 10
        if commission_value < 10:
            commission_value = 10
        self.ui.commissionInput.setText(str(commission_value))
        total_cost_taka = int(round(commission_value + self.int_v(self.ui.mosqueInput) + self.int_v(self.ui.somitiInput) + self.int_v(self.ui.otherInput)))
        self.ui.totalCostInput.setText(str(total_cost_taka))
        self.ui.finalTakaInput.setText(str(int(round(total_sum - total_cost_taka))))  # Update final taka input

        # Cost Update Function -> Update total cost and finalTaka
    def change_in_cost_section(self):
        try:
            # Round and convert values to integers
            total_cost_taka = int(round(self.int_v(self.ui.commissionInput) + self.int_v(self.ui.mosqueInput) + self.int_v(self.ui.somitiInput) + self.int_v(self.ui.otherInput)))
            self.ui.totalCostInput.setText(str(total_cost_taka))  # Update total cost input
            # Calculate the final taka
            final_taka = int(round(self.int_v(self.ui.totalTakaInput) - total_cost_taka))
            self.ui.finalTakaInput.setText(str(final_taka))  # Update final taka input
        except Exception as e:
            print(f"Error in change_in_cost_section: {e}")

    # change_in_total_taka -> Update finalTaka
    def change_in_total_taka(self):
        try:
            self.ui.finalTakaInput.setText(
                str(self.int_v(self.ui.totalTakaInput) - self.int_v(self.ui.totalCostInput)))  # Update final taka based on total cost
        except Exception as e:
            print(f"Error in change_in_total_taka: {e}")

    # Final Taka Update -> Update remaining taka
    def change_in_final_taka(self):
        try:
            self.ui.remainTakaInput.setText(str(self.int_v(self.ui.finalTakaInput) - self.int_v(self.ui.sellerPaidTakaInput)))  # Update remaining taka
        except Exception as e:
            print(f"Error in change_in_final_taka: {e}")

    # Edit or Delete Cell **************************************
    def delete_row(self, row):
        self.ui.tableWidget.removeRow(row)
        self.reconnect_delete_buttons()
        self.row_calculate()
    def cell_edited(self, row, column):
        # Reconnect the delete button after a cell is edited
        if column < 6:  # Only do this for data columns, not the button column
            delete_button = self.ui.tableWidget.cellWidget(row, 6)
            if delete_button is not None:
                delete_button.clicked.disconnect()
                delete_button.clicked.connect(lambda _, r=row: self.delete_row(r))
    def reconnect_delete_buttons(self):
        # Reconnect all delete buttons after a row is deleted
        row_count = self.ui.tableWidget.rowCount()
        for row in range(row_count):
            delete_button = self.ui.tableWidget.cellWidget(row, 6)
            if delete_button is not None:
                delete_button.clicked.disconnect()
                delete_button.clicked.connect(lambda _, r=row: self.delete_row(r))

    # Clear the tableWidget, including all widgets and items
    def clear_table_widget(self):
        for row in range(self.ui.tableWidget.rowCount()):
            for column in range(self.ui.tableWidget.columnCount()):
                cell_widget = self.ui.tableWidget.cellWidget(row, column)
                if cell_widget:  # If there's a widget, delete it
                    cell_widget.deleteLater()
                self.ui.tableWidget.takeItem(row, column)  # Remove the QTableWidgetItem if it exists
        self.ui.tableWidget.setRowCount(0)  # Reset the row count to 0


    def save_data(self):
        try:
            print("Starting save_data method")
            reply = QtWidgets.QMessageBox.question(
                None,
                'নিশ্চিত করুন',
                'আপনি কি নিশ্চিত সব এন্ট্রি ঠিক আছে, ঠিক থাকলে সেভ করার জন্য Yes  চাপুন, বাতিল করার জন্য No চাপুন',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No
            )

            # If the user confirms, proceed with deletion
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:

                # Get data from inputs
                voucher_no = self.ui.voucharInput.text()
                seller_name = self.ui.sellerNameInput.text()
                selling_date = self.ui.sellingDateInput.date().toPyDate()
                address = self.ui.sellerAddressInput.text()
                seller_phone = self.ui.sellerMobileInput.text()
                commission_amount = self.ui.commissionInput.text()
                total_cost_amount = self.ui.totalCostInput.text()
                sell_amount = self.ui.totalTakaInput.text()
                seller_get_paid_amount = self.ui.sellerPaidTakaInput.text()
                remaining_get_paid_amount = self.ui.remainTakaInput.text()
                mosque = self.ui.mosqueInput.text()
                somiti = self.ui.somitiInput.text()
                other_cost = self.ui.otherInput.text()

                def amount_valid(amout_text_list):
                    for amount_text in amout_text_list:
                        try:
                            amount_int = float(amount_text)
                        except ValueError:
                            amount_int = -1
                        if amount_int < 0:
                            return False
                    return True

                # Validate required fields
                print(" Seller Name : ", seller_name)
                if not voucher_no or not seller_name or not selling_date:
                    QtWidgets.QMessageBox.warning(None, "Error", "সব স্টার চিহ্নিত তথ্য অবশ্যই পূরণ করতে হবে..")
                    return
                if not (amount_valid([commission_amount, total_cost_amount, sell_amount, seller_get_paid_amount, remaining_get_paid_amount, mosque, somiti, other_cost])):
                    QtWidgets.QMessageBox.warning(None, "Error", "নিচের কোন হিসাবের ইনপুট টাকার পরিমান অনুপস্থিত ..")
                    return
                if self.ui.tableWidget.rowCount() < 1:
                    QtWidgets.QMessageBox.warning(None, "Error", "কোনো ক্রেতার এন্ট্রি পাওয়া যায়নি..")
                    return
                # make it integer after validation
                commission_amount = int(commission_amount)
                total_cost_amount = int(total_cost_amount)
                sell_amount = int(sell_amount)
                seller_get_paid_amount = int(seller_get_paid_amount)
                remaining_get_paid_amount = int(remaining_get_paid_amount)
                # Check if seller profile exists
                session = self.Session()
                # entry cost
                if amount_valid([somiti, mosque, other_cost]):
                    cost_entry = session.query(CostModel).first()
                    if int(mosque) > 0:
                        cost_entry.mosque += int(mosque)
                    if int(somiti) > 0:
                        cost_entry.somiti += int(somiti)
                    if int(other_cost) > 0:
                        cost_entry.other_cost += int(other_cost)
                    session.commit()
                seller_profile = session.query(SellerProfileModel).filter_by(seller_name=seller_name).first()
                if not seller_profile:
                    seller_profile = SellerProfileModel(
                        seller_name=seller_name,
                        phone = seller_phone,
                        address=address,
                        entry_by=self.entry_by
                    )
                    session.add(seller_profile)
                    session.commit()
                    print("New SellerProfile created")

                # Update SellerProfileModel's total_receivable
                seller_profile.total_receivable += remaining_get_paid_amount
                seller_profile.total_get_paid_amount += seller_get_paid_amount
                seller_profile.total_commission += commission_amount
                seller_profile.seller_rank += 1
                seller_profile.date = selling_date
                session.commit()

                # Create or update Seller record
                seller = SellingModel(
                    vouchar_no=voucher_no,
                    seller_name=seller_name,
                    date=selling_date,
                    sell_amount=sell_amount,
                    commission_amount=commission_amount,
                    total_cost_amount=total_cost_amount,
                    category_id=seller_profile.id,
                    entry_by=self.entry_by
                )
                session.add(seller)
                session.commit()
                print("Seller record saved successfully")

                # Create Dealer record for Seller
                if seller_get_paid_amount > 0:
                    dealer = DealerModel(
                        entry_name="paid_to_seller",
                        name=seller_name,
                        date=selling_date,
                        paying_amount=seller_get_paid_amount,
                        receiving_amount=0,
                        entry_by=self.entry_by
                    )
                    session.add(dealer)
                    session.commit()
                    accounting = session.query(FinalAccounting).first()
                    if accounting:
                        accounting.capital -= seller_get_paid_amount
                    print("Dealer record for Seller saved successfully")
                else:
                    print("No take paid to seller")

                # Loop through tableWidget rows to save Buyer data
                for row in range(self.ui.tableWidget.rowCount()):
                    buyer_name = self.ui.tableWidget.item(row, 0).text()
                    fish_name = self.ui.tableWidget.item(row, 1).text()
                    fish_rate = self.ui.tableWidget.item(row, 2).text()
                    raw_weight = self.ui.tableWidget.item(row, 3).text()
                    final_weight = self.ui.tableWidget.item(row, 4).text()
                    buying_amount = int(self.ui.tableWidget.item(row, 5).text())

                    print(f"Row {row} - Buyer Name: {buyer_name}, Fish Name: {fish_name}")

                    # Check if buyer profile exists
                    buyer_profile = session.query(BuyerProfileModel).filter_by(buyer_name=buyer_name).first()
                    if not buyer_profile:
                        buyer_profile = BuyerProfileModel(
                            buyer_name=buyer_name,
                            date=selling_date,
                            entry_by=self.entry_by
                        )
                        session.add(buyer_profile)
                        session.commit()
                        print("New BuyerProfile created for : ", buyer_name)

                    # Update BuyerProfileModel's total_payable
                    buyer_profile.buyer_rank += 1
                    buyer_profile.total_payable += buying_amount
                    buyer_profile.date = selling_date
                    session.commit()

                    # Create Buyer record
                    buyer = BuyingModel(
                        vouchar_no=voucher_no,
                        buyer_name=buyer_name,
                        date=selling_date,
                        fish_name=fish_name,
                        fish_rate=fish_rate,
                        raw_weight=raw_weight,
                        final_weight=final_weight,
                        buying_amount=buying_amount,
                        seller_name=seller_name,
                        entry_by=self.entry_by,
                        category_id=buyer_profile.id  # Link to the buyer profile
                    )
                    session.add(buyer)
                    session.commit()
                session.commit()
                print("All Buyer records saved successfully")
                QtWidgets.QMessageBox.information(None, "Success", "ডেটা সফলভাবে সংরক্ষণ করা হয়েছে.")

                data_save_signals.data_saved.emit()   # send signal to save data

                # Clear form fields
                self.clear_table_widget()
                self.ui.totalTakaInput.setText("0")
                self.ui.commissionInput.setText("0")
                self.ui.totalCostInput.setText("0")
                self.ui.sellerPaidTakaInput.setText("0")
                self.ui.remainTakaInput.setText("0")
                self.ui.otherInput.setText("0")
                self.ui.voucharInput.clear()
                self.ui.sellerNameInput.clear()
                self.ui.sellerAddressInput.clear()
                self.ui.sellerMobileInput.clear()


                new_voucher = VoucherNoModel(voucher_no=voucher_no)
                session.add(new_voucher)
                session.commit()
                self.update_voucher()

        except Exception as e:
            print(f"An error occurred: {e}")
            # QtWidgets.QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")
            QtWidgets.QMessageBox.critical(None, "Error", f"ইনভ্যালিড ইনপুট")
            print(f"Error: {e}")

    def openPrintMemo(self):
        try:
            # ✅ Create the print window
            self.ui_print_form = Print_Form()
            self.ui_print_form.ui.tableWidget.horizontalHeader().setMinimumSectionSize(120)
            self.ui_print_form.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

            # ✅ Set up labels with corresponding values
            self.ui_print_form.ui.memoLabel.setText("ক্যাশমেমো")
            self.ui_print_form.ui.name.setText(str(self.ui.sellerNameInput.text()))
            self.ui_print_form.ui.date.setText(str(self.ui.sellingDateInput.text()))
            self.ui_print_form.ui.address.setText(str(self.ui.sellerAddressInput.text()))
            self.ui_print_form.ui.mobile.setText(str(self.ui.sellerMobileInput.text()))
            self.ui_print_form.ui.commission.setText(str(self.ui.commissionInput.text()))
            self.ui_print_form.ui.mosque.setText(str(self.ui.mosqueInput.text()))
            self.ui_print_form.ui.somiti.setText(str(self.ui.somitiInput.text()))
            self.ui_print_form.ui.others.setText(str(self.ui.otherInput.text()))
            self.ui_print_form.ui.totalCost_raw.setText(str(self.ui.totalCostInput.text()))
            self.ui_print_form.ui.totalCost.setText(str(self.ui.totalCostInput.text()))
            self.ui_print_form.ui.totalTaka.setText(str(self.ui.totalTakaInput.text()))
            self.ui_print_form.ui.finalTaka.setText(str(self.ui.finalTakaInput.text()))

            self.ui_print_form.ui.recevied_frame.setVisible(False)

            # ✅ Exclude column 6
            excluded_columns = {6}
            column_count = self.ui.tableWidget.columnCount()
            row_count = self.ui.tableWidget.rowCount()
            headers = [self.ui.tableWidget.horizontalHeaderItem(i).text() for i in range(column_count) if
                       i not in excluded_columns]

            self.ui_print_form.ui.tableWidget.verticalHeader().setVisible(False)
            self.ui_print_form.ui.tableWidget.setColumnCount(len(headers))
            self.ui_print_form.ui.tableWidget.setHorizontalHeaderLabels(headers)
            self.ui_print_form.ui.tableWidget.setRowCount(row_count)

            # ✅ Copy table data excluding column 6
            for row_idx in range(row_count):
                new_col_idx = 0
                for col_idx in range(column_count):
                    if col_idx in excluded_columns:
                        continue  # Skip excluded column
                    item = self.ui.tableWidget.item(row_idx, col_idx)
                    if item:
                        self.ui_print_form.ui.tableWidget.setItem(row_idx, new_col_idx,
                                                                  QtWidgets.QTableWidgetItem(item.text()))
                    new_col_idx += 1

            # ✅ Show the print window
            self.ui_print_form.show()

            # ✅ Set up the printer
            printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.PrinterMode.HighResolution)
            printer.setPageSize(QtGui.QPageSize(QtGui.QPageSize.PageSizeId.A4))

            # ✅ Open print preview dialog
            preview_dialog = QtPrintSupport.QPrintPreviewDialog(printer)
            preview_dialog.paintRequested.connect(self.renderPrintPreview)
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


