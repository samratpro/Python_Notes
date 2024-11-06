## 01. Simple Login and Dashboard
```py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from login import Ui_LoginWindow  # Import the converted login UI
from dashboard import Ui_DashboardWindow  # Import the converted dashboard UI

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.loginButton.clicked.connect(self.handle_login)  # Assume you have a button named loginButton

    def handle_login(self):
        # Add login validation logic here
        username = self.ui.usernameInput.text()  # Assuming usernameInput is your input field for username
        password = self.ui.passwordInput.text()  # Assuming passwordInput is your input field for password

        if self.validate_login(username, password):
            self.dashboard = DashboardWindow()  # If login is successful, open dashboard
            self.dashboard.show()
            self.close()

    def validate_login(self, username, password):
        # This is a placeholder; add your authentication logic here
        return username == "admin" and password == "password"

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DashboardWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
```
