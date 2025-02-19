from PyQt6 import QtWidgets
from ui.printmemo_ui import Ui_Form
from PyQt6.QtGui import QFont, QFontDatabase

class Print_Form(QtWidgets.QWidget):  # ✅ Inherit QWidget
    def __init__(self):
        super().__init__()  # ✅ Properly initialize QWidget
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # ✅ Set up UI on self (which is now a QWidget)
        self.setup_ui()

    def setup_ui(self):
        self.apply_bangla_font()

    def apply_bangla_font(self):
        bangla_font_path = "font/nato.ttf"
        font_id = QFontDatabase.addApplicationFont(bangla_font_path)
        custom_font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font_low = QFont(custom_font_family, 11)  # Font size 14
        custom_font_high = QFont(custom_font_family, 22)  # Font size 14
        custom_font = QFont(custom_font_family, 12)  # Font size 14
        self.ui.tableWidget.horizontalHeader().setFont(custom_font)
        self.ui.tableWidget.verticalHeader().setFont(custom_font)
        self.ui.label.setFont(custom_font_low)
        self.ui.memoLabel.setFont(custom_font)
        self.ui.label_9.setFont(custom_font_high)
        self.ui.label_10.setFont(custom_font_low)
        self.ui.label_11.setFont(custom_font)
        self.ui.label_13.setFont(custom_font)
        self.ui.label_12.setFont(custom_font)
        self.ui.label_14.setFont(custom_font)
        self.ui.label_2.setFont(custom_font_low)
        self.ui.label_3.setFont(custom_font_low)
        self.ui.label_4.setFont(custom_font_low)
        self.ui.label_5.setFont(custom_font_low)
        self.ui.label_6.setFont(custom_font_low)
        self.ui.label_7.setFont(custom_font_low)
        self.ui.label_19.setFont(custom_font)
        self.ui.label_20.setFont(custom_font)
        self.ui.label_21.setFont(custom_font)
        self.ui.label_22.setFont(custom_font)
        self.ui.label_23.setFont(custom_font)
        self.ui.label_24.setFont(custom_font)
        self.ui.label_25.setFont(custom_font)
        self.ui.label_26.setFont(custom_font)
        self.ui.label_16.setFont(custom_font)
        self.ui.label_15.setFont(custom_font)
        self.ui.label_17.setFont(custom_font_low)
        self.ui.label_18.setFont(custom_font)
        self.ui.date.setFont(custom_font)
