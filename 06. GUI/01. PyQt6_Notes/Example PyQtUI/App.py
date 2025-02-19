from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon, QKeyEvent
from PyQt6.QtCore import Qt, pyqtSignal
from login import LoginPage
from dashboard import DashboardPage
import sys
from features.data_save_signals import data_save_signals

class Dashboard(QMainWindow):
    logout_signal = pyqtSignal()

    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setMinimumSize(1000, 600)

        # Initialize the dashboard UI
        self.dashboard_ui = DashboardPage(username)
        self.dashboard_ui.ui.setupUi(self)
        self.dashboard_ui.setup_ui()

        print("user name from app.py : ", username)

        # Assuming you have a logout button defined in your UI
        self.dashboard_ui.ui.logoutBtn.clicked.connect(self.handle_logout)
        self.dashboard_ui.ui.logoutIconBtn.clicked.connect(self.handle_logout)

    def handle_logout(self):
        """Handle the logout button click."""
        self.logout_signal.emit()
        # data_save_signals.data_saved.emit()


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Company Name")
        self.setMinimumSize(1200, 700)
        self.setWindowIcon(QIcon("images/logo.png"))
        self.login_widget = None
        self.dashboard = None

        # Set the initial widget to login form
        self.show_login()

    def show_login(self):
        try:
            """Switches back to the login page."""
            # Recreate the login form and widget
            self.login_form = LoginPage()
            self.login_form.login_success_signal.connect(self.show_dashboard)
            print("Showing login form")
            self.setCentralWidget(self.login_form)
        except Exception as e:
            print(f"Error in show_login: {e}")

    def show_dashboard(self, username):
        try:
            """Switches to the dashboard after a successful login."""
            # Recreate the dashboard
            print("username  show_dashboard: ", username)
            self.dashboard = Dashboard(username)
            self.dashboard.logout_signal.connect(self.show_login)
            print("Showing dashboard")
            self.setCentralWidget(self.dashboard)
        except Exception as e: 
            print(f"Error in show_dashboard: {e}")

    def keyPressEvent(self, event: QKeyEvent):
        """
        Override the keyPressEvent to handle F11 for fullscreen toggling.
        """
        if event.key() == Qt.Key.Key_F11:
            # Toggle fullscreen mode
            if self.isFullScreen():
                self.showNormal()  # Exit fullscreen
            else:
                self.showFullScreen()  # Enter fullscreen
        else:
            # Call the base class keyPressEvent for other keys
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = App()
    main_window.show()
    sys.exit(app.exec())