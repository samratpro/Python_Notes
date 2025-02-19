from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget
from features.data_save_signals import data_save_signals
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from ui.usersPage_ui import Ui_usersPage
from models import *
from forms.usersForm import userForm
from PyQt6.QtGui import QFont, QFontDatabase


class userPage(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setup_database()  # First setup database
        self.username = username
        session = self.Session()
        user = session.query(UserModel).filter(UserModel.username == self.username).one()
        self.user_role = user.role
        self.ui = Ui_usersPage()
        self.ui.setupUi(self)
        self.setup_ui()

    def setup_database(self):
        self.Base = declarative_base()
        self.engine = create_engine('sqlite:///business.db')
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def setup_ui(self):
        if self.user_role == "admin":
            self.ui.tableWidget.horizontalHeader().setDefaultSectionSize(180)
            self.ui.tableWidget.horizontalHeader().setMinimumSectionSize(180)
            self.ui.tableWidget.verticalHeader().setVisible(False)
            data_save_signals.data_saved.connect(self.filter_data)
            self.filter_data()
            self.ui.addUser.clicked.connect(lambda: self.open_add_user_form())
            self.apply_bangla_font()

    def apply_bangla_font(self):
        bangla_font_path = "font/nato.ttf"
        font_id = QFontDatabase.addApplicationFont(bangla_font_path)
        custom_font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(custom_font_family, 13)  # Font size 14
        # self.setFont(custom_font)
        self.ui.tableWidget.horizontalHeader().setFont(custom_font)
        self.ui.tableWidget.verticalHeader().setFont(custom_font)

    def edit_profile(self, username):
        self.open_add_user_form(username)

    def open_add_user_form(self, username='new'):
        self.dialog = userForm(username)  # Instantiate userForm as the dialog
        self.dialog.setWindowTitle("User Form")
        self.dialog.ui.done.clicked.connect(self.validation_and_accept_information)
        self.dialog.ui.cancel.clicked.connect(self.dialog.close)  # Use dialog's close method
        self.dialog.exec()  # Show the userForm dialog

    def validation_and_accept_information(self):
        success, error_message = self.dialog.entry_validation()  # Call entry_validation correctly
        if success:
            self.accept_information()
        else:
            error_dialog = QtWidgets.QMessageBox(self.dialog)
            error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Input Error")
            error_dialog.setText(error_message)
            error_dialog.exec()

    def accept_information(self):
        try:
            session = self.Session()
            username = self.dialog.ui.username.text().strip()
            password = self.dialog.ui.password.text().strip()
            role_index = self.dialog.ui.role.currentIndex()
            role = "editor" if role_index == 1 else "admin"

            if self.dialog.username == 'new':
                # Adding a new user
                existing_user = session.query(UserModel).filter(UserModel.username == username).one_or_none()
                if existing_user:
                    raise Exception("A user with this username already exists.")
                new_user = UserModel(username=username, password=password, role=role, delete=True)
                session.add(new_user)
            else:
                # Editing an existing user
                user = session.query(UserModel).filter(UserModel.username == self.dialog.username).one_or_none()
                if not user:
                    raise Exception("User not found.")
                user.username = username
                user.password = password
                user.role = role

            session.commit()
            session.close()

            # Emit signal to refresh the data in the table
            self.filter_data()
            self.dialog.close()

        except Exception as e:
            print(f"Error in accept_information: {e}")
            error_dialog = QtWidgets.QMessageBox(self.dialog)
            error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText(f"Error: {str(e)}")
            error_dialog.exec()

    def filter_data(self):
        try:
            session = self.Session()
            users = session.query(UserModel).all()
            session.close()
            # Clear existing table data
            self.ui.tableWidget.clearContents()
            self.ui.tableWidget.setRowCount(0)

            # Populate the table with queried data
            row = 0
            for user in users:
                self.ui.tableWidget.insertRow(row)
                self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user.id)))
                self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(user.username)))
                self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(user.role)))

                # Add a delete button in the last column
                edit_button = QtWidgets.QPushButton("")
                edit_icon = QtGui.QIcon("./images/edit.png")  # Path to your delete icon
                edit_button.setIcon(edit_icon)
                edit_button.setIconSize(QtCore.QSize(24, 24))  # Set icon size if needed
                edit_button.setStyleSheet("background-color: white; border: none;margin-left:50px;")  # Set wh
                edit_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                edit_button.clicked.connect(lambda _, username=user.username: self.edit_profile(username))
                self.ui.tableWidget.setCellWidget(row, 3, edit_button)

                delete_button = QtWidgets.QPushButton("")
                delete_icon = QtGui.QIcon("./images/delete.png")  # Path to your delete icon
                delete_button.setIcon(delete_icon)
                delete_button.setIconSize(QtCore.QSize(24, 24))  # Set icon size if needed
                delete_button.setStyleSheet("background-color: white; border: none;margin-left:50px;")  # Set wh
                delete_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                delete_button.clicked.connect(lambda _, r=row: self.delete_row(r))
                self.ui.tableWidget.setCellWidget(row, 4, delete_button)
                row += 1

        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Users Profile Error:", f"An error occurred while filtering data: {e}")

    def delete_row(self, row):
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
                user = session.query(UserModel).filter(UserModel.id == entry_id).one()
                if user.delete == False:
                    user.password = 'admin'
                    session.commit()
                else:
                    session.delete(user)
                    session.commit()
                    session.close()
                self.ui.tableWidget.removeRow(row)
                self.filter_data()
        except Exception as ops:
            print(f'error in delete of buyer profile: ({ops})')
