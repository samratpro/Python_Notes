'''
************* change styel sheet **************
QPushButton:hover{border:1px solid #0078D7}
QPushButton{border:1px solid #7A7A7A}

color: blue;
background-color: yellow;
selection-color: yellow;
selection-background-color: red;
'''

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import uic
import sys


class Window(QWidget):  # QWidget....................
    def __init__(self):
        super().__init__()
        self.setGeometry(220, 220, 700, 400)
        self.setWindowTitle('Hello App')
        self.setWindowIcon(QIcon("py.png"))

      
        # ********* Vertical Layout,,, QVBoxLayout ********* 
        VBox = QVBoxLayout(self)
        self.label = QLabel('V Box Test')
        self.line = QLineEdit(self)
        VBox.addWidget(self.label)
        VBox.addWidget(self.line)
        VBox.addStretch(5)
        self.setLayout(VBox)
      
        # ********* Horizontal Layout,, QHBoxLayout *********
        HBox = QHBoxLayout(self)
        self.label = QLabel('Price : ')
        self.spinbox = QSpinBox(self)
        self.spinbox.valueChanged.connect(self.price_change)  # When User will scroll up price will change for price_change function
        self.line = QLineEdit(self)
        HBox.addWidget(self.label)
        HBox.addWidget(self.spinbox)
        HBox.addWidget(self.line)
        VBox.addStretch(5)
        self.setLayout(HBox)

        # ********* Grid Layout, it like Tkinter *********
        grid = QGridLayout(self)
        self.label = QLabel('V Box Test')
        self.line = QLineEdit(self)
        self.line.setFixedWidth(300)
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(self.line, 0, 1)
        self.setLayout(grid)
    
        # ********* Form Layout ********* Gap


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
