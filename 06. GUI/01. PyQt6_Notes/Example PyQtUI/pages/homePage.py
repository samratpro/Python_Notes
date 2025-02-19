from PyQt6.QtWidgets import QWidget
from datetime import datetime, timedelta
from PyQt6.QtCore import QDate
from features.data_save_signals import data_save_signals
from sqlalchemy import create_engine, not_
from sqlalchemy.orm import sessionmaker, declarative_base
from ui.homePage_ui import Ui_HomePageMain
from PyQt6 import QtWidgets
from models import *
from PyQt6.QtGui import QFont, QFontDatabase


class homepage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_database()  # First setup database
        self.ui = Ui_HomePageMain()
        self.ui.setupUi(self)
        self.setup_ui()

    def setup_database(self):
        self.Base = declarative_base()
        self.engine = create_engine('sqlite:///business.db')    # change db url
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def setup_ui(self):
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
        self.apply_bangla_font()

    def apply_bangla_font(self):
        bangla_font_path = "font/nato.ttf"
        font_id = QFontDatabase.addApplicationFont(bangla_font_path)
        custom_font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(custom_font_family, 13)
        custom_font_low = QFont(custom_font_family, 12)
        custom_font_high = QFont(custom_font_family, 18)
        # Recursively apply font to all child widgets
        self.setFont(custom_font)
        amount_font = QFont(custom_font_family, 22)
        self.ui.capitalAmount.setFont(amount_font)
        self.ui.loanAmount.setFont(amount_font)
        self.ui.receivedAmount.setFont(amount_font)
        self.ui.paidAmount.setFont(amount_font)
        self.ui.payableAmount.setFont(amount_font)
        self.ui.receivableAmount.setFont(amount_font)
        self.ui.label.setFont(custom_font_high)
        self.ui.label_2.setFont(custom_font_low)


    def filter_data(self):
            try:
                # Get the start and end dates from the input fields
                start_date = self.ui.startDateInput.date().toPyDate()
                start_date = start_date - timedelta(days=7)
                end_date = self.ui.endDateInput.date().toPyDate()

                # Retrieve data from the database
                session = self.Session()
                capital = session.query(FinalAccounting).first()

                loan_all = session.query(LoanModel).filter(LoanModel.amount > 0)
                loan_amount = sum(loan.amount for loan in loan_all)

                # Filter received amounts within the date range
                received_all = session.query(DealerModel).filter(
                        DealerModel.receiving_amount != 0,
                        not_(DealerModel.entry_name.in_(['capital_deposit', 'borrowing'])),
                        DealerModel.date.between(start_date, end_date)
                        ).all()

                received_amount = sum(received.receiving_amount for received in received_all)

                # Filter paid amounts within the date range
                paid_all = session.query(DealerModel).filter(
                    DealerModel.paying_amount != 0,
                             not_(DealerModel.entry_name.in_(['loan_repayment','capital_withdrawal'])),
                            DealerModel.date.between(start_date, end_date)
                           ).all()
                paid_amount = sum(paid.paying_amount for paid in paid_all)

                # Get total payable amounts within the date range
                cost_entry = session.query(CostModel).first()
                total_payable = session.query(SellerProfileModel).filter(SellerProfileModel.date.between(start_date, end_date)).all()
                payable_amount = sum(payable.total_receivable for payable in total_payable)
                payable_amount += (cost_entry.other_cost + cost_entry.somiti + cost_entry.mosque)

                # Get total receivable amounts within the date range
                total_receivable = session.query(BuyerProfileModel).filter(BuyerProfileModel.date.between(start_date, end_date)).all()
                receivable_amount = sum(receivable.total_payable for receivable in total_receivable)


                self.ui.capitalAmount.setText(str(capital.capital))
                self.ui.loanAmount.setText(str(loan_amount))
                self.ui.receivedAmount.setText(str(received_amount))
                self.ui.paidAmount.setText(str(paid_amount))
                self.ui.payableAmount.setText(str(payable_amount))
                self.ui.receivableAmount.setText(str(receivable_amount))


            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "seller Profile Error", f"An error occurred while filtering data: {e}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HomePageMain = QtWidgets.QWidget()
    ui = Ui_HomePageMain()
    ui.setupUi(HomePageMain)
    HomePageMain.show()
    sys.exit(app.exec())
