from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow:
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(969, 600)
        MainWindow.setStyleSheet("""*{background:none;border:none;margin:0;padding:0;}
                                 QDateEdit, QLineEdit{border-radius:10px;padding:2px;margin:1px 6px;}
                                 #IconMenu, #SideMenu{background-color:#221402;padding:0px;margin:0px;}
                                 #IconMenu QPushButton, #IconMenu QLabel, #SideMenu QPushButton, #SideMenu QLabel{
                                    background-color:#221402;
                                    color:#C6CDCA;
                                    text-align: left;
                                    padding:14px 12px;
                                    }
                                 #IconMenuItems QPushButton, #MenuItems QPushButton{border-radius:10px;}
                                 #IconMenuItems QPushButton:checked, #MenuItems QPushButton:checked,#IconMenuItems QPushButton:hover, #MenuItems QPushButton:hover {
                                    background-color: #010905;
                                    }
                                 #header{background-color:#2D221B}
                                 #header QLabel, #header QPushButton{color:#C6CDCA;font-size:16px;}
                                 #header #userBtn{margin-right:20px;}
                                 #body{background-color:#F0F0F0}
                                 """)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget_Layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.centralwidget_Layout.setContentsMargins(0, 0, 0, 0)
        self.centralwidget_Layout.setSpacing(0)
        self.centralwidget_Layout.setObjectName("centralwidget_Layout")

        # ***************** Icon Menu  ******************
        self.IconMenu = QtWidgets.QWidget(parent=self.centralwidget)
        self.IconMenu.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.IconMenu.setFont(font)
        self.IconMenu.setObjectName("IconMenu")
        self.IconMenu.setHidden(True)

        self.IconMenu_Layout = QtWidgets.QVBoxLayout(self.IconMenu)
        self.IconMenu_Layout.setContentsMargins(0, 0, 0, 0)
        self.IconMenu_Layout.setSpacing(0)
        self.IconMenu_Layout.setObjectName("IconMenu_Layout")
        self.IconMenuToggle = QtWidgets.QFrame(parent=self.IconMenu)
        self.IconMenuToggle.setMinimumSize(QtCore.QSize(0, 50))
        self.IconMenuToggle.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.IconMenuToggle.setFont(font)
        self.IconMenuToggle.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.IconMenuToggle.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.IconMenuToggle.setObjectName("IconMenuToggle")
        self.IconMenuToggle_Layout = QtWidgets.QVBoxLayout(self.IconMenuToggle)
        self.IconMenuToggle_Layout.setContentsMargins(9, -1, -1, -1)
        self.IconMenuToggle_Layout.setObjectName("IconMenuToggle_Layout")
        self.IconToggleBtn = QtWidgets.QPushButton(parent=self.IconMenuToggle)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.IconToggleBtn.setFont(font)
        self.IconToggleBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.IconToggleBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./icons/menu.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.IconToggleBtn.setIcon(icon)
        self.IconToggleBtn.setIconSize(QtCore.QSize(28, 28))
        self.IconToggleBtn.setCheckable(True)
        self.IconToggleBtn.setAutoRepeat(False)
        self.IconToggleBtn.setAutoExclusive(True)
        self.IconToggleBtn.setObjectName("IconToggleBtn")
        self.IconMenuToggle_Layout.addWidget(self.IconToggleBtn)
        self.IconMenu_Layout.addWidget(self.IconMenuToggle)
        self.IconMenuItems = QtWidgets.QFrame(parent=self.IconMenu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.IconMenuItems.setFont(font)
        self.IconMenuItems.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.IconMenuItems.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.IconMenuItems.setObjectName("IconMenuItems")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.IconMenuItems)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # ******** Home icon Menu *******************
        self.homeIconBtn = QtWidgets.QPushButton(parent=self.IconMenuItems)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.homeIconBtn.setFont(font)
        self.homeIconBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.homeIconBtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./icons/home.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.homeIconBtn.setIcon(icon1)
        self.homeIconBtn.setIconSize(QtCore.QSize(28, 28))
        self.homeIconBtn.setCheckable(True)
        self.homeIconBtn.setChecked(True)
        self.homeIconBtn.setAutoExclusive(True)
        self.homeIconBtn.setAutoRepeatDelay(100)
        self.homeIconBtn.setAutoDefault(False)
        self.homeIconBtn.setFlat(False)
        self.homeIconBtn.setObjectName("homeIconBtn")
        self.verticalLayout_2.addWidget(self.homeIconBtn)

        # ******** Memo icon Menu *******************
        self.memoIconBtn = QtWidgets.QPushButton(parent=self.IconMenuItems)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.memoIconBtn.setFont(font)
        self.memoIconBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.memoIconBtn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./icons/edit.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.memoIconBtn.setIcon(icon2)
        self.memoIconBtn.setIconSize(QtCore.QSize(28, 28))
        self.memoIconBtn.setCheckable(True)
        self.memoIconBtn.setAutoExclusive(True)
        self.memoIconBtn.setAutoRepeatDelay(100)
        self.memoIconBtn.setAutoDefault(False)
        self.memoIconBtn.setFlat(False)
        self.memoIconBtn.setObjectName("memoIconBtn")
        self.verticalLayout_2.addWidget(self.memoIconBtn)

        # ******** Cost Entry icon Menu *******************
        self.costEntryIconBtn = QtWidgets.QPushButton(parent=self.IconMenuItems)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.costEntryIconBtn.setFont(font)
        self.costEntryIconBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.costEntryIconBtn.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("./icons/file-text.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.costEntryIconBtn.setIcon(icon4)
        self.costEntryIconBtn.setIconSize(QtCore.QSize(28, 28))
        self.costEntryIconBtn.setCheckable(True)
        self.costEntryIconBtn.setAutoExclusive(True)
        self.costEntryIconBtn.setAutoRepeatDelay(100)
        self.costEntryIconBtn.setAutoDefault(False)
        self.costEntryIconBtn.setFlat(False)
        self.costEntryIconBtn.setObjectName("costEntryIconBtn")
        self.verticalLayout_2.addWidget(self.costEntryIconBtn)

        # ******** Buyer Profile icon Menu *******************
        self.buyerProfileIconBtn = QtWidgets.QPushButton(parent=self.IconMenuItems)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.buyerProfileIconBtn.setFont(font)
        self.buyerProfileIconBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buyerProfileIconBtn.setText("")
        iconusers = QtGui.QIcon()
        iconusers.addPixmap(QtGui.QPixmap("./icons/users.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buyerProfileIconBtn.setIcon(iconusers)
        self.buyerProfileIconBtn.setIconSize(QtCore.QSize(28, 28))
        self.buyerProfileIconBtn.setCheckable(True)
        self.buyerProfileIconBtn.setAutoExclusive(True)
        self.buyerProfileIconBtn.setAutoRepeatDelay(100)
        self.buyerProfileIconBtn.setAutoDefault(False)
        self.buyerProfileIconBtn.setFlat(False)
        self.buyerProfileIconBtn.setObjectName("buyerProfileIconBtn")
        self.verticalLayout_2.addWidget(self.buyerProfileIconBtn)

        # ******** Seller Profile icon Menu *******************
        self.sellerProfileIconBtn = QtWidgets.QPushButton(parent=self.IconMenuItems)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.sellerProfileIconBtn.setFont(font)
        self.sellerProfileIconBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.sellerProfileIconBtn.setText("")
        self.sellerProfileIconBtn.setIcon(iconusers)
        self.sellerProfileIconBtn.setIconSize(QtCore.QSize(28, 28))
        self.sellerProfileIconBtn.setCheckable(True)
        self.sellerProfileIconBtn.setAutoExclusive(True)
        self.sellerProfileIconBtn.setAutoRepeatDelay(100)
        self.sellerProfileIconBtn.setAutoDefault(False)
        self.sellerProfileIconBtn.setFlat(False)
        self.sellerProfileIconBtn.setObjectName("buyerProfileIconBtn")
        self.verticalLayout_2.addWidget(self.sellerProfileIconBtn)
        # ******** Top icon Menu end *******************

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                           QtWidgets.QSizePolicy.Policy.Expanding)

        # ************* Bottom icon menu  ************************
        # ******** Settings icon Menu *******************
        self.verticalLayout_2.addItem(spacerItem)
        self.settingsIconBtn = QtWidgets.QPushButton(parent=self.IconMenuItems)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.settingsIconBtn.setFont(font)
        self.settingsIconBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.settingsIconBtn.setText("")
        settingIcon = QtGui.QIcon()
        settingIcon.addPixmap(QtGui.QPixmap("./icons/settings.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.settingsIconBtn.setIcon(settingIcon)
        self.settingsIconBtn.setIconSize(QtCore.QSize(28, 28))
        self.settingsIconBtn.setCheckable(True)
        self.settingsIconBtn.setAutoExclusive(True)
        self.settingsIconBtn.setAutoRepeatDelay(100)
        self.settingsIconBtn.setAutoDefault(False)
        self.settingsIconBtn.setFlat(False)
        self.settingsIconBtn.setObjectName("settingsIconBtn")
        self.verticalLayout_2.addWidget(self.settingsIconBtn)

        # ******** Logout icon Menu *******************
        self.logoutIconBtn = QtWidgets.QPushButton(parent=self.IconMenuItems)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.logoutIconBtn.setFont(font)
        self.logoutIconBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.logoutIconBtn.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("./icons/log-out.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.logoutIconBtn.setIcon(icon6)
        self.logoutIconBtn.setIconSize(QtCore.QSize(28, 28))
        self.logoutIconBtn.setCheckable(True)
        self.logoutIconBtn.setAutoExclusive(True)
        self.logoutIconBtn.setAutoRepeatDelay(100)
        self.logoutIconBtn.setAutoDefault(False)
        self.logoutIconBtn.setFlat(False)
        self.logoutIconBtn.setObjectName("logoutIconBtn")
        self.verticalLayout_2.addWidget(self.logoutIconBtn)
        self.IconMenu_Layout.addWidget(self.IconMenuItems)
        self.centralwidget_Layout.addWidget(self.IconMenu)
        # ******** icon Menu end *******************

        # ******** Main Menu start *******************
        self.SideMenu = QtWidgets.QWidget(parent=self.centralwidget)
        self.SideMenu.setMinimumSize(QtCore.QSize(200, 0))
        self.SideMenu.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.SideMenu.setFont(font)
        self.SideMenu.setObjectName("SideMenu")
        self.SideMenu_Layout = QtWidgets.QVBoxLayout(self.SideMenu)
        self.SideMenu_Layout.setContentsMargins(0, 0, 0, 0)
        self.SideMenu_Layout.setSpacing(0)
        self.SideMenu_Layout.setObjectName("SideMenu_Layout")
        self.MenuToggle = QtWidgets.QFrame(parent=self.SideMenu)
        self.MenuToggle.setMinimumSize(QtCore.QSize(0, 50))
        self.MenuToggle.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.MenuToggle.setFont(font)
        self.MenuToggle.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.MenuToggle.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.MenuToggle.setObjectName("MenuToggle")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.MenuToggle)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ToggleBtn = QtWidgets.QPushButton(parent=self.MenuToggle)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.ToggleBtn.setFont(font)
        self.ToggleBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.ToggleBtn.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("./icons/chevrons-left.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ToggleBtn.setIcon(icon7)
        self.ToggleBtn.setIconSize(QtCore.QSize(28, 28))
        self.ToggleBtn.setCheckable(True)
        self.ToggleBtn.setAutoExclusive(True)
        self.ToggleBtn.setObjectName("ToggleBtn")
        self.verticalLayout.addWidget(self.ToggleBtn)
        self.SideMenu_Layout.addWidget(self.MenuToggle)
        self.MenuItems = QtWidgets.QFrame(parent=self.SideMenu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.MenuItems.setFont(font)
        self.MenuItems.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.MenuItems.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.MenuItems.setObjectName("MenuItems")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.MenuItems)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # ******** Home main Menu *******************
        self.homeBtn = QtWidgets.QPushButton(parent=self.MenuItems)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.homeBtn.setFont(font)
        self.homeBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.homeBtn.setIcon(icon1)
        self.homeBtn.setIconSize(QtCore.QSize(28, 28))
        self.homeBtn.setCheckable(True)
        self.homeBtn.setChecked(True)
        self.homeBtn.setAutoExclusive(True)
        self.homeBtn.setAutoRepeatDelay(100)
        self.homeBtn.setAutoDefault(False)
        self.homeBtn.setFlat(False)
        self.homeBtn.setObjectName("homeBtn")
        self.verticalLayout_3.addWidget(self.homeBtn)

        # ******** Memo main Menu *******************
        self.memoBtn = QtWidgets.QPushButton(parent=self.MenuItems)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.memoBtn.setFont(font)
        self.memoBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.memoBtn.setIcon(icon2)
        self.memoBtn.setIconSize(QtCore.QSize(28, 28))
        self.memoBtn.setCheckable(True)
        self.memoBtn.setAutoExclusive(True)
        self.memoBtn.setAutoRepeatDelay(100)
        self.memoBtn.setAutoDefault(False)
        self.memoBtn.setFlat(False)
        self.memoBtn.setObjectName("memoBtn")
        self.verticalLayout_3.addWidget(self.memoBtn)

        # ******** CostEntry main Menu *******************
        self.costEntryBtn = QtWidgets.QPushButton(parent=self.MenuItems)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.costEntryBtn.setFont(font)
        self.costEntryBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.costEntryBtn.setIcon(icon4)
        self.costEntryBtn.setIconSize(QtCore.QSize(28, 28))
        self.costEntryBtn.setCheckable(True)
        self.costEntryBtn.setAutoExclusive(True)
        self.costEntryBtn.setAutoRepeatDelay(100)
        self.costEntryBtn.setAutoDefault(False)
        self.costEntryBtn.setFlat(False)
        self.costEntryBtn.setObjectName("costEntryBtn")
        self.verticalLayout_3.addWidget(self.costEntryBtn)

        # ******** Buyer Profile main Menu *******************
        self.buyerProfileBtn = QtWidgets.QPushButton(parent=self.MenuItems)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.buyerProfileBtn.setFont(font)
        self.buyerProfileBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buyerProfileBtn.setIcon(iconusers)
        self.buyerProfileBtn.setIconSize(QtCore.QSize(28, 28))
        self.buyerProfileBtn.setCheckable(True)
        self.buyerProfileBtn.setAutoExclusive(True)
        self.buyerProfileBtn.setAutoRepeatDelay(100)
        self.buyerProfileBtn.setAutoDefault(False)
        self.buyerProfileBtn.setFlat(False)
        self.buyerProfileBtn.setObjectName("buyerProfileBtn")
        self.verticalLayout_3.addWidget(self.buyerProfileBtn)

        # ******** SellerProfile main Menu *******************
        self.sellerProfileBtn = QtWidgets.QPushButton(parent=self.MenuItems)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.sellerProfileBtn.setFont(font)
        self.sellerProfileBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.sellerProfileBtn.setIcon(iconusers)
        self.sellerProfileBtn.setIconSize(QtCore.QSize(28, 28))
        self.sellerProfileBtn.setCheckable(True)
        self.sellerProfileBtn.setAutoExclusive(True)
        self.sellerProfileBtn.setAutoRepeatDelay(100)
        self.sellerProfileBtn.setAutoDefault(False)
        self.sellerProfileBtn.setFlat(False)
        self.sellerProfileBtn.setObjectName("sellerProfileBtn")
        self.verticalLayout_3.addWidget(self.sellerProfileBtn)
        # ******** Top main Menu end *******************

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)

        # ******** Bottom main Menu *******************
        # ******** Settings main Menu *******************
        self.settingsBtn = QtWidgets.QPushButton(parent=self.MenuItems)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.settingsBtn.setFont(font)
        self.settingsBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.settingsBtn.setIcon(settingIcon)
        self.settingsBtn.setIconSize(QtCore.QSize(28, 28))
        self.settingsBtn.setCheckable(True)
        self.settingsBtn.setAutoExclusive(True)
        self.settingsBtn.setAutoRepeatDelay(100)
        self.settingsBtn.setAutoDefault(False)
        self.settingsBtn.setFlat(False)
        self.settingsBtn.setObjectName("settingsBtn")
        self.verticalLayout_3.addWidget(self.settingsBtn)

        # ******** Logout main Menu *******************
        self.logoutBtn = QtWidgets.QPushButton(parent=self.MenuItems)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.logoutBtn.setFont(font)
        self.logoutBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.logoutBtn.setIcon(icon6)
        self.logoutBtn.setIconSize(QtCore.QSize(28, 28))
        self.logoutBtn.setCheckable(True)
        self.logoutBtn.setAutoExclusive(True)
        self.logoutBtn.setAutoRepeatDelay(100)
        self.logoutBtn.setAutoDefault(False)
        self.logoutBtn.setFlat(False)
        self.logoutBtn.setObjectName("logoutBtn")
        self.verticalLayout_3.addWidget(self.logoutBtn)
        self.SideMenu_Layout.addWidget(self.MenuItems)
        self.centralwidget_Layout.addWidget(self.SideMenu)
        # ******** Menu End *******************

        self.MainBody = QtWidgets.QWidget(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.MainBody.setFont(font)
        self.MainBody.setObjectName("MainBody")
        self.MainBody_Layout = QtWidgets.QVBoxLayout(self.MainBody)
        self.MainBody_Layout.setContentsMargins(0, 0, 0, 0)
        self.MainBody_Layout.setSpacing(0)
        self.MainBody_Layout.setObjectName("MainBody_Layout")
        self.Header = QtWidgets.QWidget(parent=self.MainBody)
        self.Header.setMinimumSize(QtCore.QSize(0, 60))
        self.Header.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Header.setFont(font)
        self.Header.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Header.setObjectName("Header")
        self.Header_Layout = QtWidgets.QHBoxLayout(self.Header)
        self.Header_Layout.setObjectName("Header_Layout")

        # ******** Header Left *******************
        self.LeftHeader = QtWidgets.QWidget(parent=self.Header)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.LeftHeader.setFont(font)
        self.LeftHeader.setObjectName("LeftHeader")
        self.LeftHeader_Layout = QtWidgets.QHBoxLayout(self.LeftHeader)
        self.LeftHeader_Layout.setContentsMargins(-1, 0, -1, -1)
        self.LeftHeader_Layout.setObjectName("LeftHeader_Layout")
        self.logo = QtWidgets.QLabel(parent=self.LeftHeader)
        self.logo.setMinimumSize(QtCore.QSize(45, 35))
        self.logo.setMaximumSize(QtCore.QSize(40, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.logo.setFont(font)
        self.logo.setText("")
        # ******** Logo *******************
        self.logo.setPixmap(QtGui.QPixmap("./images/logo.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.LeftHeader_Layout.addWidget(self.logo)
        self.tag = QtWidgets.QLabel(parent=self.LeftHeader)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.tag.setFont(font)
        self.tag.setObjectName("tag")
        self.LeftHeader_Layout.addWidget(self.tag)
        self.Header_Layout.addWidget(self.LeftHeader, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header_Layout.addItem(spacerItem2)

        # ******** Right Left *******************
        self.RightHeader = QtWidgets.QWidget(parent=self.Header)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.RightHeader.setFont(font)
        self.RightHeader.setStyleSheet("*{background-color: rgb(0, 0, 0);\n"
                                       " border-radius:20px;\n"
                                       "margin-right:10px;\n"
                                       "}")
        self.RightHeader.setObjectName("RightHeader")
        self.RightHeader_Layout = QtWidgets.QHBoxLayout(self.RightHeader)
        self.RightHeader_Layout.setContentsMargins(-1, 9, -1, 9)
        self.RightHeader_Layout.setObjectName("RightHeader_Layout")

        # *********** User icon ***************
        self.userBtn = QtWidgets.QPushButton(parent=self.RightHeader)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.userBtn.setFont(font)
        self.userBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.userBtn.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("./icons/user.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.userBtn.setIcon(icon8)
        self.userBtn.setIconSize(QtCore.QSize(28, 28))
        self.userBtn.setCheckable(True)
        self.userBtn.setAutoExclusive(True)
        self.userBtn.setObjectName("userBtn")
        self.RightHeader_Layout.addWidget(self.userBtn)

        self.Header_Layout.addWidget(self.RightHeader)
        self.MainBody_Layout.addWidget(self.Header)
        self.Body = QtWidgets.QWidget(parent=self.MainBody)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Body.setFont(font)
        self.Body.setObjectName("Body")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Body)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # *********** StackWidget *******************
        print("debug 1")
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.Body)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.stackedWidget.setFont(font)
        self.stackedWidget.setObjectName("stackedWidget")


        ## ************* Pages will add here *****************



        self.horizontalLayout.addWidget(self.stackedWidget)
        self.MainBody_Layout.addWidget(self.Body)
        self.centralwidget_Layout.addWidget(self.MainBody)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.ToggleBtn.clicked.connect(self.IconMenu.show)  # type: ignore
        self.ToggleBtn.clicked.connect(self.SideMenu.hide)  # type: ignore
        self.IconToggleBtn.clicked.connect(self.SideMenu.show)  # type: ignore
        self.IconToggleBtn.clicked.connect(self.IconMenu.hide)  # type: ignore

        self.homeBtn.toggled['bool'].connect(self.homeIconBtn.setChecked)  # type: ignore
        self.homeIconBtn.toggled['bool'].connect(self.homeBtn.setChecked)  # type: ignore

        self.memoBtn.toggled['bool'].connect(self.memoIconBtn.setChecked)  # type: ignore
        self.memoIconBtn.toggled['bool'].connect(self.memoBtn.setChecked)  # type: ignore

        self.costEntryBtn.toggled['bool'].connect(self.costEntryIconBtn.setChecked)  # type: ignore
        self.costEntryIconBtn.toggled['bool'].connect(self.costEntryBtn.setChecked)  # type: ignore

        self.buyerProfileBtn.toggled['bool'].connect(self.buyerProfileIconBtn.setChecked)  # type: ignore
        self.buyerProfileIconBtn.toggled['bool'].connect(self.buyerProfileBtn.setChecked)  # type: ignore

        self.sellerProfileBtn.toggled['bool'].connect(self.sellerProfileIconBtn.setChecked)  # type: ignore
        self.sellerProfileIconBtn.toggled['bool'].connect(self.sellerProfileBtn.setChecked)  # type: ignore

        self.settingsBtn.toggled['bool'].connect(self.settingsBtn.setChecked)  # type: ignore
        self.settingsIconBtn.toggled['bool'].connect(self.settingsBtn.setChecked)  # type: ignore

        self.logoutBtn.toggled['bool'].connect(self.logoutIconBtn.setChecked)  # type: ignore
        self.logoutIconBtn.toggled['bool'].connect(self.logoutBtn.setChecked)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.IconToggleBtn.setToolTip(_translate("MainWindow", "Expand Menu"))
        self.homeIconBtn.setToolTip(_translate("MainWindow", "Home"))
        self.homeBtn.setToolTip(_translate("MainWindow", "Home"))
        self.homeBtn.setText(_translate("MainWindow", "Home"))

        self.memoIconBtn.setToolTip(_translate("MainWindow", "Transaction"))
        self.memoBtn.setToolTip(_translate("MainWindow", "Transaction"))
        self.memoBtn.setText(_translate("MainWindow", "Transaction"))

        self.costEntryIconBtn.setToolTip(_translate("MainWindow", "Entry"))
        self.costEntryBtn.setToolTip(_translate("MainWindow", "Entry"))
        self.costEntryBtn.setText(_translate("MainWindow", "Entry"))

        self.settingsIconBtn.setToolTip(_translate("MainWindow", "Settings"))
        self.logoutIconBtn.setToolTip(_translate("MainWindow", "Logout"))
        self.ToggleBtn.setToolTip(_translate("MainWindow", "Narrow"))

        self.buyerProfileBtn.setToolTip(_translate("MainWindow", "Buyers Profile"))
        self.buyerProfileBtn.setText(_translate("MainWindow", "Buyers Profile"))

        self.sellerProfileBtn.setToolTip(_translate("MainWindow", "sellers Profile"))
        self.sellerProfileBtn.setText(_translate("MainWindow", "sellers Profile"))

        self.settingsBtn.setToolTip(_translate("MainWindow", "Settings"))
        self.settingsBtn.setText(_translate("MainWindow", "Settings"))
        self.logoutBtn.setToolTip(_translate("MainWindow", "Logout"))
        self.logoutBtn.setText(_translate("MainWindow", "Logout"))
        self.tag.setText(_translate("MainWindow", "Company Name"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())