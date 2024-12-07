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

        # ****************** Label *********************
        label = QLabel('Hi 1', self)
        label.setText('Hi')
        label.setNum(15)
        label.move(100, 100)
        label.setStyleSheet('color:blue')
        label.clear()
        
        pixmap = QPixmap('py.png')   # ********* Add Picture in Label *********
        label.setPixmap(pixmap)

        movie = QMovie('py.gif')  # ********* Add gif picture in label *********
        label.setMovie(movie)
        movie.start()

      
        # ********************** Label  2 **********************
        self.label = QLabel()
        self.line = QLineEdit(self)
        self.line.textChanged.connect(self.label.setText)
        self.line.editingFinished.connect(self.on_editing_finished)
        
        layout = QVBoxLayout()
        self.label = QLabel('Label Text')
        self.label.setMouseTracking(True)  # Enable mouse tracking to detect mouse clicks
        self.label.mousePressEvent = self.on_label_click  # Override the mousePressEvent method
        layout.addWidget(self.label)
        self.setLayout(layout)
        
    def on_label_click(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print("Label clicked!")


        # ********************** Text Browser ********************** Gap -> It is like HTML & CSS

        # ********************** Graphics View ********************** Gap -> Need to Study

        # ********************** Calender Widget ********************** Gap 

        # ********************** LCD Number ********************** Gap 

        # ********************** Progress Bar ********************** Gap 

        # ********************** Horizontal Line ********************** Gap 

        # ********************** Vertical Line ********************** Gap 

        # ********************** OpenGL Widget ********************** Gap 



app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
