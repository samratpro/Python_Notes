"""
QSpinBox (Spin Box):
valueChanged

QDateEdit (Date Edit):
dateChanged

QTimeEdit (Time Edit):
timeChanged

QDateTimeEdit (Date and Time Edit):
dateTimeChanged

QSlider (Slider):
valueChanged

QScrollBar (Scroll Bar):
valueChanged

QFileDialog (File Dialog):
Signals like fileSelected and filesSelected are generated when files are selected in the file dialog.

QColorDialog (Color Dialog):
colorSelected

QFontDialog (Font Dialog):
fontSelected

QInputDialog (Input Dialog):
intValueChanged, doubleValueChanged, intValueSelected, doubleValueSelected

valueChanged: Generated when the value of the dial changes.
QTextEdit (Text Edit):

"""




from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import uic
import sys
from PyQt6.QtCore import Qt


class Window(QWidget):  # QWidget....................
    def __init__(self):
        super().__init__()
        self.setGeometry(220, 220, 700, 400)
        self.setWindowTitle('Hello App')
        self.setWindowIcon(QIcon("py.png"))


    # ******************  Messagebox  ******************
    '''
        QMessageBox.warning(self, 'Message')
        QMessageBox.information(self, 'Message')
        QMessageBox.question(self, 'Remove Item', 'Do you want to remove item?',
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                      )
    '''

     
    def mouseMoveEvent(self, e):
      if e.button == Qt.MouseButton.RightButton:
        self.label.setText("mouseMoveEvent  ###############")
    
    def mousePressEvent(self, e):
      if e.button() == Qt.MouseButton.LeftButton:
          self.label.setText("mousePressEvent LEFT ..............")
    
      elif e.button() == Qt.MouseButton.MiddleButton:
          self.label.setText("mousePressEvent MIDDLE .........")
    
      elif e.button() == Qt.MouseButton.RightButton:
          self.label.setText("mousePressEvent RIGHT ...............")
    
    
    def mouseReleaseEvent(self, e):
      if e.button() == Qt.MouseButton.LeftButton:
          self.label.setText("mouseReleaseEvent LEFT>>>>>>>>>>>>>>>>>>>")
    
      elif e.button() == Qt.MouseButton.MiddleButton:
          self.label.setText("mouseReleaseEvent MIDDLE>>>>>>>>>>>>>")
    
      elif e.button() == Qt.MouseButton.RightButton:
          self.label.setText("mouseReleaseEvent RIGHT>>>>>>>>>>>>>>")
    
    
    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("mouseDoubleClickEvent LEFT<<<<<<<<<<<<<<<<<<<<<<<<")
    
        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("mouseDoubleClickEvent MIDDLE<<<<<<<<<<<<<<<<<<<<<<")
    
        elif e.button() == Qt.MouseButton.RightButton:
            self.label.setText("mouseDoubleClickEvent RIGHT<<<<<<<<<<<<<<<<<")


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
