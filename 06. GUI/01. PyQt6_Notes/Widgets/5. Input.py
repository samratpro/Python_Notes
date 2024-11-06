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


        # *********** Combo Box ******************
        layout = QVBoxLayout()
        self.combo_box = QComboBox()
        self.combo_box.addItem('Option 1')
        self.combo_box.addItem('Option 2')
        self.combo_box.activated.connect(self.on_activated)   # *** Event
        self.combo_box.currentIndexChanged.connect(self.on_current_index_changed)   # *** Event
        layout.addWidget(self.combo_box)
        self.setLayout(layout)
        
    def on_activated(self, index):
        selected_item = self.combo_box.itemText(index)
        print(f"Activated: {selected_item}")
        
    def on_current_index_changed(self, index):
        selected_item = self.combo_box.itemText(index)
        print(f"Current Index Changed: {selected_item}") 
      
        # *********** Font Combo Box ******************

        # ***************** QLineEdit has with QSlider  **********************
        # ***************** QLine has with SpinBox  **********************

        # *************** QTextEdit ********************
        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.textChanged.connect(self.on_text_changed)   # *** Event
        self.text_edit.cursorPositionChanged.connect(self.on_cursor_position_changed)   # *** Event
        self.text_edit.copyAvailable.connect(self.on_copy_available)   # *** Event
        self.text_edit.redoAvailable.connect(self.on_redo_available)   # *** Event
        self.text_edit.undoAvailable.connect(self.on_undo_available)   # *** Event
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def on_text_changed(self):
        print("Text changed:", self.text_edit.toPlainText())
        
    def on_cursor_position_changed(self):
        cursor_position = self.text_edit.textCursor().position()
        print("Cursor position:", cursor_position)
        
    def on_copy_available(self, enable):
        if enable:
            print("Text can be copied to clipboard")
        else:
            print("No text available to copy")
            
    def on_redo_available(self, enable):
        if enable:
            print("Redo actions are available")
        else:
            print("No redo actions available")
            
    def on_undo_available(self, enable):
        if enable:
            print("Undo actions are available")
        else:
            print("No undo actions available")

        # *************** QPlainTextEdit ******************** Text without CSS

      
        # ********************** Spin Box *With Qline  **********************
        layout = QVBoxLayout()
        self.spinbox = QSpinBox(self)
        self.spinbox.valueChanged.connect(self.price_change)  # When User will scroll up price will change for price_change function
        self.line = QLine()
        layout.addWidget(self.spinbox)
        layout.addWidget(self.line)
        self.setLayout(layout)
        
    def price_change(self):
        spin_data = self.spinbox.value()
        self.line.setText(str(spin_data * 500))

        # **************** Double Spin Box ********************** Float Value

        # **************** Time Edit **********************  Gap

        # **************** Date Edit **********************  Gap
       
        # **************** Date / Time Edit **********************  Gap

        # **************** Dial **********************  Gap

        # **************** Scroll Bar **********************  Gap

       
        # ***************** Q Slider and Q Line Edit ***********
        layout = QHBoxLayout()
        self.label = QLabel()
        self.line = QLineEdit()
        self.line.returnPressed.connect(self.set_slider_value)  # ********** If Pressed Enter then this event will hapen
        self.line.textChanged.connect(self.set_slider_value)

        self.slider = QSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(200)
        self.slider.valueChanged.connect(self.set_lable_value)   # *** Event
        self.slider.setOrientation(Qt.Orientation.Horizontal)    # ** Horizontal & Vertical
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.sliderMoved.connect(self.on_slider_moved)   # *** Event
        self.slider.sliderPressed.connect(self.on_slider_pressed)   # *** Event
        self.slider.sliderReleased.connect(self.on_slider_released)   # *** Event
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        layout.addWidget(self.line)
        self.setLayout(layout)

   def set_lable_value(self):
        value = self.slider.value()
        self.label.setText(str(value))
        self.line.setText(str(value))
       
   def set_slider_value(self):
        try:
            value = int(self.line.text())
            self.slider.setValue(value)
        except:
            pass
          

   def on_slider_moved(self, value):
        print(f"Slider moved to {value}")
       
   def on_slider_pressed(self):
        print("Slider pressed")
       
   def on_slider_released(self):
        print("Slider released")


        # **************** key Sequence Edit **********************  Gap


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
