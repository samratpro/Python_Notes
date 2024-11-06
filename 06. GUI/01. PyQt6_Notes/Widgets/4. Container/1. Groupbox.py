import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGroupBox, QVBoxLayout, QPushButton

class GroupBoxExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GroupBox Example")

        group_box = QGroupBox("Group Box Title")
        layout = QVBoxLayout()

        button1 = QPushButton("Button 1")
        button2 = QPushButton("Button 2")

        layout.addWidget(button1)
        layout.addWidget(button2)
        group_box.setLayout(layout)

        self.setCentralWidget(group_box)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GroupBoxExample()
    window.show()
    sys.exit(app.exec())
