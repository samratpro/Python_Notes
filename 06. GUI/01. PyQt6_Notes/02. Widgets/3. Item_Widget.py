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


        # ***************** Q List *********************
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.addItem('Item 1')
        self.list_widget.addItem('Item 2')
        self.list_widget.insertItem(0, 'Item 0')
        self.list_widget.itemClicked.connect(self.on_item_clicked)   # *** Event
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)   # *** Event
        self.list_widget.itemSelectionChanged.connect(self.on_item_selection_changed)   # *** Event
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def on_item_clicked(self, item):
        print(f"Item clicked: {item.text()}")
        
    def on_item_double_clicked(self, item):
        print(f"Item double-clicked: {item.text()}")
        
    def on_item_selection_changed(self):
        selected_items = [item.text() for item in self.list_widget.selectedItems()]
        print(f"Selection changed: {selected_items}")

        # ******************  Q List 2  ******************
        VBox = QVBoxLayout(self)
        self.listWidget = QListWidget()
        self.additem = QPushButton(VBox)
        self.additem.clicked.connect(self.add_item)
        VBox.addWidget(self.listWidget)
        
    def add_item(self):
        row = self.listWidget.currentRow()
        title = 'Add Item'
        data, ok = QInputDialog.getText(self, title, title)
        if ok and len(data) > 0:
            self.listWidget.insertItem(row, data)

        
      
        # **************** Tree ****************** Gap


      

        # **************** Table ******************
        layout = QVBoxLayout()
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(1)
        self.table_widget.setColumnCount(1)
        self.table_widget.setItem(0, 0, QTableWidgetItem('Row 1, Col 1'))
        self.table_widget.cellClicked.connect(self.on_cell_clicked)   # *** Event
        self.table_widget.cellDoubleClicked.connect(self.on_cell_double_clicked)   # *** Event
        self.table_widget.itemSelectionChanged.connect(self.on_item_selection_changed)   # *** Event
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
        
   def on_cell_clicked(self, row, column):
      item_text = self.table_widget.item(row, column).text()
      print(f"Cell clicked: {item_text}")
       
   def on_cell_double_clicked(self, row, column):
      item_text = self.table_widget.item(row, column).text()
      print(f"Cell double-clicked: {item_text}")
       
   def on_item_selection_changed(self):
      selected_items = [item.text() for item in self.table_widget.selectedItems()]
      print(f"Selection changed: {selected_items}")



app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
