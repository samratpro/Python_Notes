from PyQt6.QtWidgets import QDialog
from forms.usersForm_ui import Ui_userForm
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from models import *
from PyQt6.QtGui import QFont, QFontDatabase  # for font file load


class userForm(QDialog):
        def __init__(self, username):
            super().__init__()
            self.ui = Ui_userForm()
            self.ui.setupUi(self)  # Call setupUi to apply the design to this dialog
            self.username = username
            self.setup_database()
            self.setup_ui()

        def setup_database(self):
            self.Base = declarative_base()
            self.engine = create_engine('sqlite:///business.db')
            self.Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)

        def setup_ui(self):
            session = self.Session()
            if self.username != 'new':
                user = session.query(UserModel).filter(UserModel.username == self.username).one_or_none()
                if user:
                    self.ui.username.setText(user.username)
                    self.ui.username.setDisabled(True)
                    self.ui.password.setText(user.password)
                    if user.id == 1:
                        self.ui.role.setDisabled(True)
            session.close()

        def entry_validation(self):
            username = self.ui.username.text().strip()
            password = self.ui.password.text().strip()
            if not username:
                return False, "ইউজার নাম লিখুন দয়া করে.."
            if not password:
                return False, 'পাসওয়ার্ড লিখুন দয়া করে..'
            return True, None

