'''
************* change styel sheet **************
QPushButton:hover{border:1px solid #0078D7}
QPushButton{border:1px solid #7A7A7A}
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

        #  ********* Working with label *********
        label = QLabel('Hi 1', self)
        label.setText('Hi')
        label.setNum(15)
        label.move(100, 100)
        label.setStyleSheet('color:blue')
        label.clear()

        # ********* Add Picture in Label *********
        pixmap = QPixmap('py.png')  
        label.setPixmap(pixmap)

        # ********* Add gif picture in label *********
        movie = QMovie('py.gif')  
        label.setMovie(movie)
        movie.start()


        # ********* QLineEdit *********
        line = QLineEdit(self)  # self or Window
        self.line.setFixedWidth(300)
        line.setText('Hi 2')
        line.setPlaceholderText("Hi")
        line.setEnabled(True)
        line.setEchoMode(QLineEdit.EchoMode.Password)
        

        # ********* Spin Box and QHBoxLayout *********
        HBox = QHBoxLayout(self)
        self.label = QLabel('Price : ')
        self.spinbox = QSpinBox(self)
        # ***************** Event ******************************
        self.spinbox.valueChanged.connect(self.price_change)  # When User will scroll up price will change for price_change function
        self.line = QLineEdit(self)
        HBox.addWidget(self.label)
        HBox.addWidget(self.spinbox)
        HBox.addWidget(self.line)
        VBox.addStretch(5)
        self.setLayout(HBox)

        # ********* VBoxLayout *********
        VBox = QVBoxLayout(self)
        self.label = QLabel('V Box Test')
        self.line = QLineEdit(self)
        VBox.addWidget(self.label)
        VBox.addWidget(self.line)
        VBox.addStretch(5)
        self.setLayout(VBox)


        # ********* Grid Layout, it like tkinter *********
        grid = QGridLayout(self)
        self.label = QLabel('V Box Test')
        self.line = QLineEdit(self)
        self.line.setFixedWidth(300)
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(self.line, 0, 1)
        self.setLayout(grid)
    
        # ********* Q Push Button with event  *********         
        vbox = QVBoxLayout(self)             
        self.btn = QPushButton('My Data', self)
        self.btn.clicked.connect(self.create_message)
        vbox.addStretch(5)                   
        vbox.addWidget(self.btn)             

        # ********* listWidget For add_item(self) *********
        VBox = QVBoxLayout(self)
        self.listWidget = QListWidget()
        self.additem = QPushButton(VBox)
        self.additem.clicked.connect(self.add_item)
        VBox.addWidget(self.listWidget)



app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())



