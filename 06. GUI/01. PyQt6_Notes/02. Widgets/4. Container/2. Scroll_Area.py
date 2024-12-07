import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QScrollArea, QWidget, QVBoxLayout, QLabel

class ScrollAreaExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ScrollArea Example")

        scroll_area = QScrollArea()
        widget = QWidget()
        layout = QVBoxLayout()

        for i in range(20):
            label = QLabel(f"Label {i}")
            layout.addWidget(label)

        widget.setLayout(layout)
        scroll_area.setWidget(widget)

        self.setCentralWidget(scroll_area)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrollAreaExample()
    window.show()
    sys.exit(app.exec())
