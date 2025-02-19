from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt, QDate
from datetime import datetime
from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from features.data_save_signals import data_save_signals
from PyQt6.QtGui import QFont, QFontDatabase  # for font file load
from forms.cost_entry_form_ui import Ui_CostEntry

class CostEntry_Form(QDialog):
    def __init__(self, username):
        super().__init__()
        self.ui = Ui_CostEntry()
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
        # Set current date ****************
        self.ui.entryDate.setDisplayFormat("dd/MM/yyyy")
        self.today_date_raw = datetime.now()
        self.today_date = self.today_date_raw.strftime("%d/%m/%Y").lstrip('0').replace('/0', '/')
        self.qdate_today = QDate.fromString(self.today_date, "d/M/yyyy")
        self.ui.entryDate.setDate(self.qdate_today)

        # ************ Autocomplete Payer Name *****************************
        self.payerCompleter = QtWidgets.QCompleter(self.get_all_payer_names(), self)
        self.payerCompleter.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui.payerName.setCompleter(self.payerCompleter)                        # change input field
        # *************** end autocomplete *******************************

        # ************ Autocomplete Receiver Name*****************************
        self.receiverCompleter = QtWidgets.QCompleter(self.get_all_receiver_names(), self)
        self.receiverCompleter.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui.receiverName.setCompleter(self.receiverCompleter)

        # change input field
        # *************** end autocomplete *******************************
        self.ui.payerName.textChanged.connect(lambda: self.make_capital(self.ui.payerName))
        self.ui.receiverName.textChanged.connect(lambda: self.make_capital(self.ui.receiverName))

        # autofill amount
        self.receiverCompleter.activated.connect(lambda text: self.autofill_amount(text))
        self.payerCompleter.activated.connect(lambda text: self.autofill_amount(text))

        # disable entry name
        self.ui.entryName.currentIndexChanged.connect(lambda: self.entry_disable(self.ui.entryName.currentIndex()))
        self.ui.entryName.currentIndexChanged.connect(self.autofill_cost)
        # by default payer name disable cause selected zero index
        self.ui.payerName.setDisabled(True)
        self.ui.payerName.setStyleSheet("background-color: #F0F0F0;")

        self.apply_bangla_font()
        self.update_setting_font()
        data_save_signals.data_saved.connect(self.update_setting_font)

    def apply_bangla_font(self):
        bangla_font_path = "font/nato.ttf"
        font_id = QFontDatabase.addApplicationFont(bangla_font_path)
        custom_font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(custom_font_family, 13)
        self.ui.label_3.setFont(custom_font)
        self.ui.label_4.setFont(custom_font)
        self.ui.label_5.setFont(custom_font)
        self.ui.label_7.setFont(custom_font)
        self.ui.label_8.setFont(custom_font)
        self.ui.label_9.setFont(custom_font)
        self.ui.cancelBtn.setFont(custom_font)
        self.ui.addBtn.setFont(custom_font)
        self.ui.entryName.setFont(custom_font)

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
        self.ui.payerName.setFont(custom_font)
        self.ui.receiverName.setFont(custom_font)
        self.ui.description.setFont(custom_font)
        enable_bangla_typing(self.ui.payerName, setting.font)
        enable_bangla_typing(self.ui.receiverName, setting.font)
        enable_bangla_typing(self.ui.description, setting.font)


    def make_capital(self, element):
        element.textChanged.disconnect()
        element.setText(element.text().title())
        element.textChanged.connect(lambda: self.make_capital(element))

    def get_all_payer_names(self):
        """Fetch all payer names from the database for autocomplete."""
        session = self.Session()
        try:
            buyer_names = [name_entry.buyer_name for name_entry in session.query(BuyerProfileModel).all()]
            loan_receiver_names = [name_entry.loan_receiver_name for name_entry in session.query(PayingLoanModel).filter(PayingLoanModel.amount > 0)]
            unique_names = set(buyer_names + loan_receiver_names)
            return list(unique_names)  # Convert set back to list
        finally:
            session.close()

    def get_all_receiver_names(self):
        """Fetch all receiver names from the database for autocomplete."""
        session = self.Session()
        try:
            seller_names = [name_entry.seller_name for name_entry in session.query(SellerProfileModel).all()]
            loan_payer_names = [name_entry.loan_payer_name for name_entry in session.query(LoanModel).filter(LoanModel.amount > 0)]
            loan_receiver_names = [name_entry.loan_receiver_name for name_entry in session.query(PayingLoanModel).filter(PayingLoanModel.amount > 0)]
            unique_names = set(seller_names + loan_payer_names + loan_receiver_names)
            return list(unique_names)  # Convert set back to list
        finally:
            session.close()

    def entry_disable(self, entry_index):
        if entry_index in [0, 2, 5, 6, 7, 8, 9, 10, 11]:
            self.ui.payerName.clear()
            self.ui.amount.clear()
            self.ui.payerName.setDisabled(True)
            self.ui.payerName.setStyleSheet("background-color: #F0F0F0;")
            self.ui.receiverName.setDisabled(False)
            self.ui.receiverName.setStyleSheet("background-color: #FFFFFF;")
        else:
            self.ui.payerName.setDisabled(False)
            self.ui.payerName.setStyleSheet("background-color: #FFFFFF;")
            self.ui.receiverName.clear()
            self.ui.amount.clear()
            self.ui.receiverName.setDisabled(True)
            self.ui.receiverName.setStyleSheet("background-color: #F0F0F0")

    def autofill_amount(self, name):
        entry_index = self.ui.entryName.currentIndex()
        session = self.Session()
        if entry_index == 0:
            seller_name = session.query(SellerProfileModel).filter_by(seller_name=name).first()
            if seller_name:
                self.ui.amount.setText(str(seller_name.total_receivable))
        if entry_index == 1:
            buyer_name = session.query(BuyerProfileModel).filter_by(buyer_name=name).first()
            if buyer_name:
                self.ui.amount.setText(str(buyer_name.total_payable))
        if entry_index == 5:
            loan_payer_name = session.query(LoanModel).filter_by(loan_payer_name=name).first()
            if loan_payer_name:
                self.ui.amount.setText(str(loan_payer_name.amount))
        if entry_index == 12:
            loan_payer_name = session.query(PayingLoanModel).filter_by(loan_receiver_name=name).first()
            if loan_payer_name:
                self.ui.amount.setText(str(loan_payer_name.amount))
        session.close()
    def autofill_cost(self):
        entry_index = self.ui.entryName.currentIndex()
        session = self.Session()
        if entry_index == 8:
            mosque = session.query(CostModel.mosque).first()
            if mosque:
                self.ui.amount.setText(str(mosque[0]))
        if entry_index == 9:
            somiti = session.query(CostModel.somiti).first()
            if somiti:
                self.ui.amount.setText(str(somiti[0]))
        if entry_index == 10:
            other_cost = session.query(CostModel.other_cost).first()
            if other_cost:
                self.ui.amount.setText(str(other_cost[0]))
        session.close()
