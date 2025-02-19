from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget
from ui.login_ui import Ui_LoginForm
from models import initialize, UserModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


class LoginPage(QWidget):
    login_success_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setup_database()
        self.ui = Ui_LoginForm()
        self.ui.setupUi(self)
        self.setup_ui()


    def setup_database(self):
        self.Base = declarative_base()
        self.engine = create_engine('sqlite:///business.db')
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def setup_ui(self):
        # Login handle
        self.ui.passwordInput.editingFinished.connect(self.handle_login) # Work with enter press
        self.ui.loginBtn.clicked.connect(self.handle_login)
        self.ui.passwordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        initialize()

    def handle_login(self):
        try:
            username = self.ui.usernameInput.text()
            password = self.ui.passwordInput.text()
            session = self.Session()
            user = session.query(UserModel).filter(UserModel.username==username).one_or_none()
            if user:
                if user.password == password:
                    self.ui.errorMessage.setText('')
                    print("Login successful, emitting signal")
                    self.login_success_signal.emit(username)
                else:
                    self.ui.errorMessage.setText(f'ভুল পাসওয়ার্ড! ইঙ্গিত, {user.password[0]}...{user.password[-1]}')
                    print("Invalid password")
                    self.retry_login()
            else:
                self.ui.errorMessage.setText('ভুল ইউজারনেম!')
                print("Invalid username")
                self.retry_login()
        except Exception as e:
            print(f"Error in handle_login: {e}")

    def retry_login(self):
        try:
            self.ui.loginBtn.setEnabled(True)
        except Exception as e:
            print(f"Error in retry_login: {e}")

    def retranslateUi(self, LoginForm):
        _translate = QtCore.QCoreApplication.translate
        LoginForm.setWindowTitle(_translate("LoginForm", "Form"))
        self.ui.LoginTag.setText(_translate("LoginForm", "মেসার্স ওসমান ফিশ "))
        self.ui.username_label.setText(_translate("LoginForm", "ইউজারনেম"))
        self.ui.password_Label.setText(_translate("LoginForm", "পাসওয়ার্ড"))
        self.ui.loginBtn.setText(_translate("LoginForm", "লগইন"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoginForm = QtWidgets.QWidget()
    ui = Ui_LoginForm()
    ui.setupUi(LoginForm)
    LoginForm.show()
    sys.exit(app.exec())
