import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QTextEdit

class MDIExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MDI Example")

        mdi_area = QMdiArea()

        sub_window1 = QMdiSubWindow()
        text_edit1 = QTextEdit()
        sub_window1.setWidget(text_edit1)

        sub_window2 = QMdiSubWindow()
        text_edit2 = QTextEdit()
        sub_window2.setWidget(text_edit2)

        mdi_area.addSubWindow(sub_window1)
        mdi_area.addSubWindow(sub_window2)

        self.setCentralWidget(mdi_area)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MDIExample()
    window.show()
    sys.exit(app.exec())
