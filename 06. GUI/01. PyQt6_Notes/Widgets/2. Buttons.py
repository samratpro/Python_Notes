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
from PyQt6.QtCore import Qt


class Window(QWidget):  # QWidget....................
    def __init__(self):
        super().__init__()
        self.setGeometry(220, 220, 700, 400)
        self.setWindowTitle('Hello App')
        self.setWindowIcon(QIcon("py.png"))

      
        
        # **************** Q Push Button with event  ****************                 
        self.btn = QPushButton('My Data', self)
        self.btn.clicked.connect(self.create_message)      # *** Event
                              
    def create_message(self):                
        new_label = QLabel('New Label')      
        self.layout().addWidget(new_label)   


         # **************** Tool Button ******************      

        

      
        # **************** Radio Button ******************             
        self.radio_button = QRadioButton('Option 1')
        self.radio_button.toggled.connect(self.on_radio_toggled)   # *** Event
        
    def radio_operation(self):
        if self.radio_button.isChecked() == True:
            print("Radio Button has been checked")
          

        # ******************** QCheckBox ********************
        layout = QVBoxLayout()
        self.checkbox = QCheckBox('Check me')
        self.checkbox.stateChanged.connect(self.on_checkbox_state_changed)   # *** Event
        layout.addWidget(self.checkbox)
        self.setLayout(layout)
        
    def on_checkbox_state_changed(self, state):
        if state == 2:  # Checked state
            print("Check box checked")
        else:
            print("Check box unchecked")
    
    def check_box(self):
        if self.checkbox.isChecked():
            print("Checked")


        # **************** CommandLinkButton ******************    


        # **************** Dialog Button Box ******************    
      
       

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
