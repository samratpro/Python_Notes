import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel

class TabWidgetExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TabWidget Example")

        tab_widget = QTabWidget()

        tab1 = QWidget()
        label1 = QLabel("This is Tab 1")
        tab1.setLayout(QVBoxLayout())
        tab1.layout().addWidget(label1)

        tab2 = QWidget()
        label2 = QLabel("This is Tab 2")
        tab2.setLayout(QVBoxLayout())
        tab2.layout().addWidget(label2)

        tab_widget.addTab(tab1, "Tab 1")
        tab_widget.addTab(tab2, "Tab 2")

        self.setCentralWidget(tab_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TabWidgetExample()
    window.show()
    sys.exit(app.exec())
