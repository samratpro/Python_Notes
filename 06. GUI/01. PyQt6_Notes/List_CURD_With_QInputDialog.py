from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QInputDialog, QLineEdit, QMessageBox


class Ui_Dialog(QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(584, 519)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.additem = QtWidgets.QPushButton(parent=Dialog)
        self.additem.setObjectName("additem")
        self.additem.clicked.connect(self.add_item)
        self.verticalLayout.addWidget(self.additem)
        self.edititem = QtWidgets.QPushButton(parent=Dialog)
        self.edititem.setObjectName("edititem")
        self.edititem.clicked.connect(self.edit_item)
        self.verticalLayout.addWidget(self.edititem)
        self.deleteitem = QtWidgets.QPushButton(parent=Dialog)
        self.deleteitem.setObjectName("deleteitem")
        self.deleteitem.clicked.connect(self.delete_item)
        self.verticalLayout.addWidget(self.deleteitem)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.sort = QtWidgets.QPushButton(parent=Dialog)
        self.sort.setObjectName("sort")
        self.sort.clicked.connect(self.sort_item)
        self.verticalLayout.addWidget(self.sort)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def add_item(self):
        row = self.listWidget.currentRow()
        title = 'Add Item'
        data, ok = QInputDialog.getText(self, title, title)
        if ok and len(data) > 0:
            self.listWidget.insertItem(row, data)

    def edit_item(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.item(row)
        if item is not None:
            title = 'Edit Title'
            data, ok = QInputDialog.getText(self, title, title, QLineEdit.EchoMode.Normal, item.text())
            if ok and len(data) > 0:
                item.setText(data)

    def delete_item(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.item(row)
        # Optional
        if item is None:
            return
        replay = QMessageBox.question(self, 'Remove Item', 'Do you want to remove item?',
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                      )
        if replay == QMessageBox.StandardButton.Yes:
            # Optional
            self.listWidget.takeItem(row)

    def sort_item(self):
        self.listWidget.sortItems()
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.additem.setText(_translate("Dialog", "Add Item"))
        self.edititem.setText(_translate("Dialog", "Edit Item"))
        self.deleteitem.setText(_translate("Dialog", "Delete Item"))
        self.sort.setText(_translate("Dialog", "Sort Item"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
