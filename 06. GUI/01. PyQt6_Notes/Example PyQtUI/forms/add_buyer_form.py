from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt
from models import *
from datetime import datetime
from PyQt6.QtGui import QFont, QFontDatabase  # for font file load
from forms.add_buyer_form_ui import Ui_AddBuyer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from features.data_save_signals import data_save_signals


class AddBuyer_Form(QDialog):
    def __init__(self, username):
        super().__init__()
        self.ui = Ui_AddBuyer()
        self.ui.setupUi(self)  # Call setupUi to apply the design to this dialog
        self.entry_by = username
        self.setup_database()
        self.setup_ui()

    def setup_database(self):
        self.Base = declarative_base()
        self.engine = create_engine('sqlite:///business.db')
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def setup_ui(self):
        # self.weightType.currentIndexChanged.connect(self.calculate_price)
        self.ui.rawWeight.textChanged.connect(self.calculate_price)
        self.ui.addBtn.clicked.connect(lambda: self.handle_name_entry())

        # ************ Autocomplete *****************************
        self.auto_completer()
        data_save_signals.data_saved.connect(lambda: self.auto_completer())
        # *************** end autocomplete *******************************
        # self.ui.buyerName.textChanged.connect(lambda: self.make_capital(self.buyerName))

        # final weight change
        self.ui.finalWeight.textEdited.connect(self.final_weight_change)

        self.dhol_amount = ''
        self.dhol_amount_calculation()
        data_save_signals.data_saved.connect(self.dhol_amount_calculation)


        self.apply_bangla_font()
        self.update_setting_font()
        data_save_signals.data_saved.connect(self.update_setting_font)


    def apply_bangla_font(self):
        bangla_font_path = "font/nato.ttf"
        font_id = QFontDatabase.addApplicationFont(bangla_font_path)
        custom_font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(custom_font_family, 13)  # Font size 14
        self.ui.label.setFont(custom_font)
        self.ui.label_6.setFont(custom_font)
        self.ui.label_2.setFont(custom_font)
        self.ui.weightType.setFont(custom_font)
        self.ui.label_5.setFont(custom_font)
        self.ui.label_7.setFont(custom_font)
        self.ui.label_8.setFont(custom_font)
        self.ui.label_3.setFont(custom_font)
        self.ui.label_4.setFont(custom_font)
        self.ui.cancelBtn.setFont(custom_font)
        self.ui.addBtn.setFont(custom_font)

    # def make_capital(self, element):
    #     element.textChanged.disconnect()
    #     element.setText(element.text().title())
    #     element.textChanged.connect(lambda: self.make_capital(element))

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
        self.ui.buyerName.setFont(custom_font)
        self.ui.fishName.setFont(custom_font)
        enable_bangla_typing(self.ui.buyerName, setting.font)
        enable_bangla_typing(self.ui.fishName, setting.font)

    def get_all_names(self):
        """Fetch all seller names from the database for autocomplete."""
        session = self.Session()
        name_entires = session.query(BuyerProfileModel).all()  # change Model name
        session.close()
        return [name_entry.buyer_name for name_entry in name_entires]  # change field name

    def auto_completer(self):
        """Refresh the QCompleter with the latest seller names."""
        self.all_name = self.get_all_names()
        self.completer = QtWidgets.QCompleter(self.all_name, self)  # # QT object parameter AddBuyer
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui.buyerName.setCompleter(self.completer)  # change input field
        self.completer.activated.connect(lambda text: self.fill_phone_number(text))

    def fill_phone_number(self, name):
        session = self.Session()
        user = session.query(BuyerProfileModel).filter_by(buyer_name=name).first()
        self.ui.mobile.setText(user.phone)

    def dhol_amount_calculation(self):
        session = self.Session()
        setting = session.query(SettingModel).first()
        self.dhol_amount = (1 / 1000) * setting.dhol
        session.close()

    def calculate_price(self):
        def custom_round(value):
            try:
                return round(float(value) + 0.01)
            except ValueError:
                return 0

        # Determine the weight type based on the selected index
        weight_index = self.ui.weightType.currentIndex()
        weight_type = {0: 'kg', 1: 'mann', 2: 'thuya'}.get(weight_index, 'thuya')

        # If the weight type is 'thuya', no calculation is needed
        if weight_type == 'thuya':
            self.ui.finalWeight.clear()
            self.ui.totalPrice.clear()
            return
        # Retrieve input values
        rate = self.ui.fishRate.text().strip()
        raw_weight = self.ui.rawWeight.text().strip()

        if custom_round(rate) == 0 or custom_round(raw_weight) == 0:
            self.dialog = QtWidgets.QDialog()
            error_dialog = QtWidgets.QMessageBox(self.dialog)
            error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Input Error")
            error_dialog.setText("দর ও কাঁচা জিরো থেকে বড় যেকোনো সংখ্যা হতে হবে..")  # Rate and weight must be numeric
            error_dialog.exec()
            return

        # Perform calculations
        try:
            raw_weight = float(raw_weight)
        except:
            raw_weight = 0
        fish_rate = custom_round(rate)

        raw_weight_for_dhol = custom_round(raw_weight)
        dhol = raw_weight_for_dhol * self.dhol_amount  # Deduction for dhol (wastage)
        final_weight = round(raw_weight - dhol, 3)  # take digit
        if weight_type == "kg":
            total_price = custom_round((fish_rate * final_weight) / 10) * 10  # 10 is doing for round figure base 10
        else:
            fish_rate = fish_rate / 40  # 40 kg per moon
            total_price = custom_round((fish_rate * final_weight) / 10) * 10  # 10 is doing for round figure base 10

        # Update UI fields
        self.ui.finalWeight.setText(str(final_weight))  # Rounded to 2 decimal places
        self.ui.totalPrice.setText(str(total_price))  # Rounded to 2 decimal places

    def final_weight_change(self):
        def custom_round(value):
            try:
                return round(float(value) + 0.01)
            except ValueError:
                return 0
            # Determine the weight type based on the selected index

        weight_index = self.ui.weightType.currentIndex()
        weight_type = {0: 'kg', 1: 'mann', 2: 'thuya'}.get(weight_index, 'thuya')

        # If the weight type is 'thuya', no calculation is needed
        if weight_type == 'thuya':
            return
        rate = self.ui.fishRate.text().strip()
        final_weight_raw = self.ui.finalWeight.text().strip()
        if custom_round(rate) == 0 or custom_round(final_weight_raw) == 0:
            self.dialog = QtWidgets.QDialog()
            error_dialog = QtWidgets.QMessageBox(self.dialog)
            error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Input Error")
            error_dialog.setText("দর এবং পাকা জিরো থেকে বড় যেকোনো সংখ্যা হতে হবে..")  # Rate and weight must be numeric
            error_dialog.exec()
            return
        fish_rate = custom_round(rate)
        final_weight = float(final_weight_raw)
        if weight_type == "kg":
            total_price = custom_round((fish_rate * final_weight) / 10) * 10  # 10 is doing for round figure base 10
        else:
            fish_rate = fish_rate / 40  # 40 kg per moon
            total_price = custom_round((fish_rate * final_weight) / 10) * 10  # 10 is doing for round figure base 10
        self.ui.totalPrice.setText(str(total_price))

    def handle_name_entry(self):
        target_name = self.ui.buyerName.text().strip()  # Change input field
        phone = self.ui.mobile.text().strip()

        if not target_name:
            # QtWidgets.QMessageBox.warning(AddBuyer, "Input Error", "ক্রেতার নাম লিখুন দয়া করে..")
            return False, "ক্রেতার নাম লিখুন দয়া করে.."

        if self.name_exists(target_name):
            print(f"Existing Seller: Seller '{target_name}' already exists. Selected.")
        else:
            # Add the new seller to the database
            if not phone:
                # QtWidgets.QMessageBox.warning(AddBuyer, "Input Error", "নতুন ক্রেতার জন্য ফোন নম্বর যোগ করুন.")
                return False, "নতুন ক্রেতার জন্য ফোন নম্বর যোগ করুন."
            self.add_name(target_name, phone)
            print(f"New Seller: Seller '{target_name}' has been added.")

        # self.auto_completer(AddBuyer)  # Refresh completer with updated list
        data_save_signals.data_saved.emit()  # Send signal to save data
        return True, None

    def name_exists(self, name):
        """Check if the seller exists in the database."""
        session = self.Session()
        exists = session.query(BuyerProfileModel).filter(BuyerProfileModel.buyer_name == name).first() is not None  # Change Model & Field name
        session.close()
        return exists

    def add_name(self, name, phone):
        """Add a new seller to the database."""
        print("Save buyer profile from form area name : ", name)
        session = self.Session()
        new_name = BuyerProfileModel(buyer_name=name, phone=phone, date=datetime.now(),
                                     entry_by=self.entry_by)  # Change Model name & Field Name
        try:
            session.add(new_name)
            session.commit()
        except Exception as e:
            session.rollback()
            QtWidgets.QMessageBox.warning(None, "Database Error", f"Failed to add seller: {e}")
        finally:
            session.close()
