import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QVBoxLayout

class FrameExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QFrame Example")

        # Create a QFrame
        frame = QFrame()
        frame_layout = QVBoxLayout()

        # Create a label and add it to the frame
        label = QLabel("This is a QFrame")
        frame_layout.addWidget(label)

        frame.setLayout(frame_layout)

        # Set the central widget of the main window to the frame
        self.setCentralWidget(frame)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FrameExample()
    window.show()
    sys.exit(app.exec())




import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout

class WidgetExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QWidget Example")

        # Create a QWidget
        widget = QWidget()
        widget_layout = QVBoxLayout()

        # Create a label and add it to the widget
        label = QLabel("This is a QWidget")
        widget_layout.addWidget(label)

        widget.setLayout(widget_layout)

        # Set the central widget of the main window to the widget
        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WidgetExample()
    window.show()
    sys.exit(app.exec())
