# outlook.py
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog
from input_form import Ui_Dialog
from PyQt6.QtWidgets import *


class Ui_outlookobject(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Create an instance from Ui_Dialog class  ** From input_form.py file
        self.dialog = Ui_Dialog()  
        # Initialize the dialog's UI Method
        self.dialog.setupUi(self.dialog)  
        # Connect the signal, to get data in Different Class or Different file's Class
        self.dialog.browser_created.connect(self.browser_created)  

    def setupUi(self, outlookobject):
        outlookobject.setObjectName("outlookobject")
        outlookobject.resize(698, 661)
        outlookobject.setAutoFillBackground(False)
        outlookobject.setWindowTitle("Outlook Verification")
        self.widget = QtWidgets.QWidget(parent=outlookobject)
        self.widget.setGeometry(QtCore.QRect(20, 10, 661, 461))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.addbrowser = QtWidgets.QPushButton(parent=self.widget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("add.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.addbrowser.setIcon(icon)
        self.addbrowser.setObjectName("addbrowser")
        self.addbrowser.setText("Add Browser")
        self.addbrowser.clicked.connect(self.open_browser_config_dialog)
        self.verticalLayout.addWidget(self.addbrowser)
        self.deletebrowser = QtWidgets.QPushButton(parent=self.widget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("stop.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.deletebrowser.setIcon(icon1)
        self.deletebrowser.setObjectName("deletebrowser")
        self.deletebrowser.setText("Stop Browser")
        self.deletebrowser.clicked.connect(self.stop_browser)
        self.verticalLayout.addWidget(self.deletebrowser)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.browserlistlabel = QtWidgets.QLabel(parent=self.widget)
        self.browserlistlabel.setStyleSheet("background-color:#F07427")
        self.browserlistlabel.setObjectName("browserlistlabel")
        self.browserlistlabel.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:700;\">Browser List</span></p></body></html>")
        self.verticalLayout_2.addWidget(self.browserlistlabel)
        self.browserlist = QtWidgets.QListWidget(parent=self.widget)
        self.browserlist.setObjectName("browserlist")
        self.verticalLayout_2.addWidget(self.browserlist)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.logs = QtWidgets.QTextEdit(parent=outlookobject)
        self.logs.setEnabled(True)
        self.logs.setReadOnly(True)
        self.logs.setGeometry(QtCore.QRect(20, 490, 661, 161))
        self.logs.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.logs.setStyleSheet("color: white;background-color: #100000;")
        self.logs.setObjectName("logs")
        self.horizontalLayout.addLayout(self.verticalLayout_2)

    # This method will execute when ** new_browser_data() will execute from ** input_form.py ** for signal passing
    def browser_created(self, browser_name):  
        print('Browser Created:', browser_name)
        self.browserlist.addItem(browser_name['browser_name'])
        
        # Threading will start from here .....................


    def stop_browser(self):
        row = self.browserlist.currentRow()
        item = self.browserlist.item(row)
        # Optional
        if item is None:
            return
        replay = QMessageBox.question(self, 'Remove Browser', 'Do you want to remove Browser?',
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                      )
        if replay == QMessageBox.StandardButton.Yes:
            # Optional
            self.browserlist.takeItem(row)

    def open_browser_config_dialog(self):
        self.dialog.exec()  # Show the dialog when the button is clicked


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    outlookobject = QtWidgets.QWidget()
    ui = Ui_outlookobject()
    ui.setupUi(outlookobject)
    outlookobject.show()
    sys.exit(app.exec())
