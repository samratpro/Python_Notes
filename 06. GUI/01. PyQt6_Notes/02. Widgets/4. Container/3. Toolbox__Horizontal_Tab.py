import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBox, QLabel, QWidget, QVBoxLayout

class ToolBoxExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ToolBox Example")

        tool_box = QToolBox()

        page1 = QWidget()
        layout1 = QVBoxLayout()
        label1 = QLabel("This is Page 1")
        layout1.addWidget(label1)
        page1.setLayout(layout1)

        page2 = QWidget()
        layout2 = QVBoxLayout()
        label2 = QLabel("This is Page 2")
        layout2.addWidget(label2)
        page2.setLayout(layout2)

        tool_box.addItem(page1, "Page 1")
        tool_box.addItem(page2, "Page 2")

        self.setCentralWidget(tool_box)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToolBoxExample()
    window.show()
    sys.exit(app.exec())
