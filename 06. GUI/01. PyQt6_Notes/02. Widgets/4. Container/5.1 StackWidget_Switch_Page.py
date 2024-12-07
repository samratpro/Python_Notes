import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton, QWidget, QVBoxLayout, QLabel

class StackedWidgetExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("StackedWidget Example")

        # Create a QStackedWidget
        stacked_widget = QStackedWidget()

        # Create Page 1
        page1 = QWidget()
        page1_layout = QVBoxLayout()

        label1 = QLabel("This is Page 1")
        button1 = QPushButton("Switch to Page 2")

        page1_layout.addWidget(label1)
        page1_layout.addWidget(button1)

        page1.setLayout(page1_layout)

        # Create Page 2
        page2 = QWidget()
        page2_layout = QVBoxLayout()

        label2 = QLabel("The Page Number is  2")
        button2 = QPushButton("Switch Page 1")

        page2_layout.addWidget(label2)
        page2_layout.addWidget(button2)

        page2.setLayout(page2_layout)

        # Add both pages to the stacked widget
        stacked_widget.addWidget(page1)
        stacked_widget.addWidget(page2)

        # Set the central widget of the main window to the stacked widget
        self.setCentralWidget(stacked_widget)

        # Connect button clicks to switch between pages
        button1.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
        button2.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StackedWidgetExample()
    window.show()
    sys.exit(app.exec())
