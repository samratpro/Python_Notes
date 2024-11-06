# This Is Different ** QDialog ** Form That dosen't need ** app.exec() **

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QFileDialog

class Ui_Dialog(QDialog):
    
    # Creating Signal or Event *** Must be include data Type ***
    browser_created = QtCore.pyqtSignal(dict)  
    
    def __init__(self):
        super().__init__()
        
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Browser Create Form")
        Dialog.resize(489, 383)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(60, 60, 381, 241))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.browsernamelabel = QtWidgets.QLabel(self.widget)
        self.browsernamelabel.setObjectName("browsernamelabel")
        self.browsernamelabel.setText("<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">Browser Name : </span></p></body></html>")
        self.gridLayout.addWidget(self.browsernamelabel, 0, 0, 1, 1)

        self.browsernamevalue = QtWidgets.QLineEdit(parent=self.widget)
        self.browsernamevalue.setObjectName("browsernamevalue")
        self.gridLayout.addWidget(self.browsernamevalue, 0, 1, 1, 2)

        self.smsapilabel = QtWidgets.QLabel(parent=self.widget)
        self.smsapilabel.setObjectName("smsapilabel")
        self.smsapilabel.setText("<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">SMS API : </span></p></body></html>")
        self.gridLayout.addWidget(self.smsapilabel, 1, 0, 1, 1)

        self.smsapivalue = QtWidgets.QLineEdit(parent=self.widget)
        self.smsapivalue.setObjectName("smsapivalue")
        self.gridLayout.addWidget(self.smsapivalue, 1, 1, 1, 2)

        self.hotmaillabel = QtWidgets.QLabel(parent=self.widget)
        self.hotmaillabel.setObjectName("hotmaillabel")
        self.hotmaillabel.setText("<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">Hotmail List : </span></p></body></html>")
        self.gridLayout.addWidget(self.hotmaillabel, 2, 0, 1, 1)

        self.choosefilehotmail = QtWidgets.QToolButton(parent=self.widget)
        self.choosefilehotmail.setObjectName("choosefilehotmail")
        self.choosefilehotmail.setText("Choose File..")
        self.choosefilehotmail.clicked.connect(self.get_mail_file)       # ---------- get_mail_file() method will execute when click 
        self.gridLayout.addWidget(self.choosefilehotmail, 2, 1, 1, 1)

        self.nofilechosenhotmail = QtWidgets.QLabel(parent=self.widget)
        self.nofilechosenhotmail.setObjectName("nofilechosenhotmail")
        self.nofilechosenhotmail.setText("No File Chosen")
        self.gridLayout.addWidget(self.nofilechosenhotmail, 2, 2, 1, 1)

        self.proxylistlabel = QtWidgets.QLabel(parent=self.widget)
        self.proxylistlabel.setObjectName("proxylistlabel")
        self.proxylistlabel.setText("<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">Proxy List : </span></p></body></html>")
        self.gridLayout.addWidget(self.proxylistlabel, 3, 0, 1, 1)

        self.choosefileproxy = QtWidgets.QToolButton(parent=self.widget)
        self.choosefileproxy.setObjectName("choosefileproxy")
        self.choosefileproxy.setText("Choose File..")
        self.choosefileproxy.clicked.connect(self.get_proxy_file)        # ----------  get_proxy_file() method will execute when click on this
        self.gridLayout.addWidget(self.choosefileproxy, 3, 1, 1, 1)

        self.nofilechosenproxy = QtWidgets.QLabel(parent=self.widget)
        self.nofilechosenproxy.setObjectName("nofilechosenproxy")
        self.nofilechosenproxy.setText("No File Chosen")
        self.gridLayout.addWidget(self.nofilechosenproxy, 3, 2, 1, 1)

        self.sucessdirlabel = QtWidgets.QLabel(self.widget)
        self.sucessdirlabel.setObjectName("Outputdirlabel")
        self.sucessdirlabel.setText("<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">Output Dir Name : </span></p></body></html>")
        self.gridLayout.addWidget(self.sucessdirlabel, 4, 0, 1, 1)

        self.sucessdirvalue = QtWidgets.QLineEdit(parent=self.widget)
        self.sucessdirvalue.setObjectName("Outputdirvalue")
        self.gridLayout.addWidget(self.sucessdirvalue, 4, 1, 1, 2)

        self.faildirlabel = QtWidgets.QLabel(self.widget)
        self.faildirlabel.setObjectName("faildirlabel")
        self.faildirlabel.setText("<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">Fail Dir Name : </span></p></body></html>")
        self.gridLayout.addWidget(self.faildirlabel, 5, 0, 1, 1)

        self.faildirvalue = QtWidgets.QLineEdit(parent=self.widget)
        self.faildirvalue.setObjectName("faildirvalue")
        self.gridLayout.addWidget(self.faildirvalue, 5, 1, 1, 2)

        self.threadinglabel = QtWidgets.QLabel(self.widget)
        self.threadinglabel.setObjectName("thredingspinlabel")
        self.threadinglabel.setText("<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">Threads : </span></p></body></html>")
        self.gridLayout.addWidget(self.threadinglabel, 6, 0, 1, 1)

        self.threds = QtWidgets.QSpinBox(parent=self.widget)
        self.gridLayout.addWidget(self.threds, 6, 1, 1, 2)

        self.countrylabel = QtWidgets.QLabel(self.widget)
        self.countrylabel.setObjectName("thredingspinlabel")
        self.countrylabel.setText("<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">Select Country : </span></p></body></html>")
        self.gridLayout.addWidget(self.countrylabel, 7, 0, 1, 1)

        self.country = QtWidgets.QComboBox(parent=self.widget)
        self.country.addItem('ESTONIA')
        self.country.addItem('BRAZIL')

        self.gridLayout.addWidget(self.country, 7, 1, 1, 2)


        self.createbrowseraction = QtWidgets.QPushButton(parent=self.widget)
        self.createbrowseraction.setStyleSheet("QPushButton:hover{border:1px solid #0096FF;background-color:#E5F1FB} QPushButton{border:1px solid #ADADAD;height:60px}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("tab.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.createbrowseraction.setIcon(icon)
        self.createbrowseraction.setObjectName("createbrowseraction")
        self.createbrowseraction.setText("Create Browser")
        self.createbrowseraction.clicked.connect(self.new_browser_data)     # -----  new_browser_data() & browser_created() two methods will execute 
        self.gridLayout.addWidget(self.createbrowseraction, 8, 0, 1, 3)

        
        # To store Text file data, *** Casue After uploading the file and reading data, this variable will store that data
        # File isn't a simple text line that stores data like ** QLineEdit **
        self.mail_data = None  

        # To store Text file data
        self.proxy_data = None  

    
    # Open and Read Text File Data and Store in ** self.mail_data = None
    def get_mail_file(self):  
        path = str(QFileDialog.getOpenFileName(self, "Select File"))
        print(path)
        if 'txt' in path:
            self.nofilechosenhotmail.setText(str(path.split("'")[1].split('/')[-1]))
            print(path)
            mail_path = str(path.split("'")[1])
            print(mail_path)
            with open(mail_path) as file:
                mail_raw = file.readlines()
                self.mail_data = [x.strip() for x in mail_raw]
                print(mail_raw)

    
    # Open and Read Text File Data and Store in ** self.proxy_data = None
    def get_proxy_file(self): 
        path = str(QFileDialog.getOpenFileName(self, 'Select File'))
        print(path)
        if 'txt' in path:
            print(path)
            self.nofilechosenproxy.setText(str(path.split("'")[1].split('/')[-1]))
            proxy_path = str(path.split("'")[1])
            print(proxy_path)
            with open(proxy_path) as file:
                proxy_raw = file.readlines()
                self.proxy_data = [x.strip() for x in proxy_raw]
                print(proxy_raw)

    
    # This method will Read All data after Completing input Form data from user ** self.accept() will close this form
    def new_browser_data(self):
        browser_name = self.browsernamevalue.text()
        smaapi = self.smsapivalue.text()
        mail_list = self.mail_data
        proxy_list = self.proxy_data
        output_dir = self.sucessdirvalue.text()
        fail_dir = self.faildirvalue.text()
        threds_count = self.threds.value()
        country = self.country.currentText()


        if browser_name and smaapi and mail_list and proxy_list and output_dir and fail_dir and int(threds_count) > 0:
            print(browser_name)
            print(smaapi)
            print(mail_list)
            print(proxy_list)
            print(output_dir)
            print(fail_dir)
            print(threds_count)
            print(country)
            data = {'browser_name': browser_name,
                    'smsapi': smaapi,
                    'mail_list': mail_list,
                    'proxy_list': proxy_list,
                    'output_dir': output_dir,
                    'fail_dir': fail_dir,
                    'threds_count': threds_count,
                    'country ': country
                    }

            # Emit the custom signal with the browser_name **********
            # This method witll execute also in Passing Class ** outlook.py **
            self.browser_created.emit(data)  # Creating This event *** this happening from **** first lien of class browser_created = QtCore.pyqtSignal(dict)
            
            print('Emitting browser_created signal with browser_name:', browser_name)

            # Clearing all records ***************
            self.browsernamevalue.clear()
            self.smsapivalue.clear()
            self.nofilechosenproxy.clear()
            self.nofilechosenhotmail.clear()
            self.mail_data = None
            self.proxy_data = None
            
            # Closing Form, when operation has been completed **********
            self.accept()  
