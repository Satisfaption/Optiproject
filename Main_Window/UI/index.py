# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'index.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHeaderView,
    QLabel, QLayout, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QTableView,
    QVBoxLayout, QWidget, QStackedWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1440, 750)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget_icons = QWidget(self.centralwidget)
        self.widget_icons.setObjectName(u"widget_icons")
        self.widget_icons.setGeometry(QRect(0, 0, 60, 750))
        self.widget_icons.setMinimumSize(QSize(60, 750))
        self.widget_icons.setMaximumSize(QSize(60, 750))
        self.widget_icons.setStyleSheet(u"QWidget{\n"
"background-color: rgb(0, 0, 0);\n"
"}")
        self.layoutWidget = QWidget(self.widget_icons)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 61, 751))
        self.vL_MenuIcon = QVBoxLayout(self.layoutWidget)
        self.vL_MenuIcon.setSpacing(0)
        self.vL_MenuIcon.setObjectName(u"vL_MenuIcon")
        self.vL_MenuIcon.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.vL_MenuIcon.setContentsMargins(0, 20, 0, 5)
        self.vL_topMenuIcon = QVBoxLayout()
        self.vL_topMenuIcon.setObjectName(u"vL_topMenuIcon")
        self.pB_MenuIcon = QPushButton(self.layoutWidget)
        self.pB_MenuIcon.setObjectName(u"pB_MenuIcon")
        self.pB_MenuIcon.setMinimumSize(QSize(0, 40))
        self.pB_MenuIcon.setMaximumSize(QSize(16777215, 40))
        icon = QIcon()
        icon.addFile(u":/Icons/menu_white.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pB_MenuIcon.setIcon(icon)
        self.pB_MenuIcon.setIconSize(QSize(100, 13))
        self.pB_MenuIcon.setCheckable(True)
        self.pB_MenuIcon.setAutoExclusive(True)

        self.vL_topMenuIcon.addWidget(self.pB_MenuIcon)

        self.pB_SearchIcon = QPushButton(self.layoutWidget)
        self.pB_SearchIcon.setObjectName(u"pB_SearchIcon")
        self.pB_SearchIcon.setMinimumSize(QSize(0, 40))
        self.pB_SearchIcon.setMaximumSize(QSize(16777215, 40))
        icon1 = QIcon()
        icon1.addFile(u":/Icons/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pB_SearchIcon.setIcon(icon1)
        self.pB_SearchIcon.setIconSize(QSize(100, 20))
        self.pB_SearchIcon.setCheckable(True)
        self.pB_SearchIcon.setAutoExclusive(True)

        self.vL_topMenuIcon.addWidget(self.pB_SearchIcon)

        self.pB_PartnerIcon = QPushButton(self.layoutWidget)
        self.pB_PartnerIcon.setObjectName(u"pB_PartnerIcon")
        self.pB_PartnerIcon.setMinimumSize(QSize(0, 40))
        self.pB_PartnerIcon.setMaximumSize(QSize(16777215, 40))
        self.pB_PartnerIcon.setStyleSheet(u"QPushButton:checked {\n"
"	background-color: red;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/Icons/studentssmall1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pB_PartnerIcon.setIcon(icon2)
        self.pB_PartnerIcon.setIconSize(QSize(100, 17))
        self.pB_PartnerIcon.setCheckable(True)
        self.pB_PartnerIcon.setChecked(False)
        self.pB_PartnerIcon.setAutoExclusive(True)

        self.vL_topMenuIcon.addWidget(self.pB_PartnerIcon)


        self.vL_MenuIcon.addLayout(self.vL_topMenuIcon)

        self.vSpacer_MenuIcon = QSpacerItem(20, 450, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.vL_MenuIcon.addItem(self.vSpacer_MenuIcon)

        self.vL_botMenuIcon = QVBoxLayout()
        self.vL_botMenuIcon.setSpacing(0)
        self.vL_botMenuIcon.setObjectName(u"vL_botMenuIcon")
        self.pB_SettingsIcon = QPushButton(self.layoutWidget)
        self.pB_SettingsIcon.setObjectName(u"pB_SettingsIcon")
        self.pB_SettingsIcon.setMinimumSize(QSize(0, 40))
        self.pB_SettingsIcon.setMaximumSize(QSize(16777215, 40))
        icon3 = QIcon()
        icon3.addFile(u":/Icons/settingssmall1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pB_SettingsIcon.setIcon(icon3)
        self.pB_SettingsIcon.setIconSize(QSize(100, 20))
        self.pB_SettingsIcon.setCheckable(True)
        self.pB_SettingsIcon.setAutoExclusive(True)

        self.vL_botMenuIcon.addWidget(self.pB_SettingsIcon)

        self.pB_LogoutIcon = QPushButton(self.layoutWidget)
        self.pB_LogoutIcon.setObjectName(u"pB_LogoutIcon")
        self.pB_LogoutIcon.setMinimumSize(QSize(0, 40))
        self.pB_LogoutIcon.setMaximumSize(QSize(16777215, 40))
        icon4 = QIcon()
        icon4.addFile(u":/Icons/signoutsmall1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pB_LogoutIcon.setIcon(icon4)
        self.pB_LogoutIcon.setIconSize(QSize(90, 16))
        self.pB_LogoutIcon.setCheckable(True)
        self.pB_LogoutIcon.setAutoExclusive(True)

        self.vL_botMenuIcon.addWidget(self.pB_LogoutIcon)


        self.vL_MenuIcon.addLayout(self.vL_botMenuIcon)

        self.widget_main = QStackedWidget(self.centralwidget)
        self.widget_main.setObjectName(u"widget_main")
        self.widget_main.setGeometry(QRect(60, 0, 1440, 750))
        self.widget_main.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.widget_main.setStyleSheet(u"QWidget{\n"
"background-color: rgb(184, 255, 192);\n"
"}")
        self.frame_Filter = QFrame(self.widget_main)
        self.frame_Filter.setObjectName(u"frame_Filter")
        self.frame_Filter.setGeometry(QRect(0, 150, 140, 600))
        self.frame_Filter.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_Filter.setFrameShadow(QFrame.Shadow.Raised)
        self.widget = QWidget(self.frame_Filter)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(4, 20, 140, 600))
        self.vL_Filter = QVBoxLayout(self.widget)
        self.vL_Filter.setSpacing(50)
        self.vL_Filter.setObjectName(u"vL_Filter")
        self.vL_Filter.setContentsMargins(0, 0, 0, 0)
        self.vL_PLZ = QVBoxLayout()
        self.vL_PLZ.setSpacing(0)
        self.vL_PLZ.setObjectName(u"vL_PLZ")
        self.lineEdit_PLZ = QLineEdit(self.widget)
        self.lineEdit_PLZ.setObjectName(u"lineEdit_PLZ")
        font = QFont()
        font.setPointSize(10)
        self.lineEdit_PLZ.setFont(font)

        self.vL_PLZ.addWidget(self.lineEdit_PLZ)

        self.label_PLZ = QLabel(self.widget)
        self.label_PLZ.setObjectName(u"label_PLZ")
        self.label_PLZ.setFont(font)

        self.vL_PLZ.addWidget(self.label_PLZ)


        self.vL_Filter.addLayout(self.vL_PLZ)

        self.vL_Flaeche = QVBoxLayout()
        self.vL_Flaeche.setSpacing(0)
        self.vL_Flaeche.setObjectName(u"vL_Flaeche")
        self.lineEdit_Flaeche = QLineEdit(self.widget)
        self.lineEdit_Flaeche.setObjectName(u"lineEdit_Flaeche")
        self.lineEdit_Flaeche.setFont(font)

        self.vL_Flaeche.addWidget(self.lineEdit_Flaeche)

        self.label_Flaeche = QLabel(self.widget)
        self.label_Flaeche.setObjectName(u"label_Flaeche")
        self.label_Flaeche.setFont(font)

        self.vL_Flaeche.addWidget(self.label_Flaeche)


        self.vL_Filter.addLayout(self.vL_Flaeche)

        self.vL_Strasse = QVBoxLayout()
        self.vL_Strasse.setSpacing(0)
        self.vL_Strasse.setObjectName(u"vL_Strasse")
        self.lineEdit_Strasse = QLineEdit(self.widget)
        self.lineEdit_Strasse.setObjectName(u"lineEdit_Strasse")
        self.lineEdit_Strasse.setFont(font)

        self.vL_Strasse.addWidget(self.lineEdit_Strasse)

        self.label_Strasse = QLabel(self.widget)
        self.label_Strasse.setObjectName(u"label_Strasse")
        self.label_Strasse.setFont(font)

        self.vL_Strasse.addWidget(self.label_Strasse)


        self.vL_Filter.addLayout(self.vL_Strasse)

        self.vL_Ort = QVBoxLayout()
        self.vL_Ort.setSpacing(0)
        self.vL_Ort.setObjectName(u"vL_Ort")
        self.lineEdit_Ort = QLineEdit(self.widget)
        self.lineEdit_Ort.setObjectName(u"lineEdit_Ort")
        self.lineEdit_Ort.setFont(font)

        self.vL_Ort.addWidget(self.lineEdit_Ort)

        self.label_Ort = QLabel(self.widget)
        self.label_Ort.setObjectName(u"label_Ort")
        self.label_Ort.setFont(font)

        self.vL_Ort.addWidget(self.label_Ort)


        self.vL_Filter.addLayout(self.vL_Ort)

        self.vL_Choice = QVBoxLayout()
        self.vL_Choice.setSpacing(0)
        self.vL_Choice.setObjectName(u"vL_Choice")
        self.comboBox_Partner = QComboBox(self.widget)
        self.comboBox_Partner.addItem("")
        self.comboBox_Partner.addItem("")
        self.comboBox_Partner.addItem("")
        self.comboBox_Partner.setObjectName(u"comboBox_Partner")
        self.comboBox_Partner.setFont(font)

        self.vL_Choice.addWidget(self.comboBox_Partner)

        self.comboBox_Begruenungsart = QComboBox(self.widget)
        self.comboBox_Begruenungsart.addItem("")
        self.comboBox_Begruenungsart.addItem("")
        self.comboBox_Begruenungsart.addItem("")
        self.comboBox_Begruenungsart.setObjectName(u"comboBox_Begruenungsart")
        self.comboBox_Begruenungsart.setFont(font)

        self.vL_Choice.addWidget(self.comboBox_Begruenungsart)


        self.vL_Filter.addLayout(self.vL_Choice)

        self.vSpacer_Filter = QSpacerItem(20, 80, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.vL_Filter.addItem(self.vSpacer_Filter)

        self.pB_Suche = QPushButton(self.widget)
        self.pB_Suche.setObjectName(u"pB_Suche")
        self.pB_Suche.setFont(font)

        self.vL_Filter.addWidget(self.pB_Suche)

        self.tableView = QTableView(self.widget_main)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(140, 150, 1051, 601))
        self.widget_menu = QWidget(self.centralwidget)
        self.widget_menu.setObjectName(u"widget_menu")
        self.widget_menu.setEnabled(True)
        self.widget_menu.setGeometry(QRect(1260, 0, 180, 750))
        self.widget_menu.setMinimumSize(QSize(180, 750))
        self.widget_menu.setMaximumSize(QSize(180, 750))
        self.widget_menu.setStyleSheet(u"QWidget{\n"
"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButtons {\n"
"	height: 40px;\n"
"	border: none;\n"
"}")
        self.layoutWidget1 = QWidget(self.widget_menu)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(2, 0, 223, 751))
        self.vL_Menu = QVBoxLayout(self.layoutWidget1)
        self.vL_Menu.setSpacing(0)
        self.vL_Menu.setObjectName(u"vL_Menu")
        self.vL_Menu.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.vL_Menu.setContentsMargins(0, 20, 0, 5)
        self.vL_topMenu = QVBoxLayout()
        self.vL_topMenu.setObjectName(u"vL_topMenu")
        self.pB_Menu = QPushButton(self.layoutWidget1)
        self.pB_Menu.setObjectName(u"pB_Menu")
        self.pB_Menu.setMinimumSize(QSize(0, 40))
        self.pB_Menu.setMaximumSize(QSize(16777215, 40))
        font1 = QFont()
        font1.setPointSize(12)
        self.pB_Menu.setFont(font1)
        self.pB_Menu.setStyleSheet(u"QPushButton {\n"
"	text-align: left;\n"
"	padding-left: 10px;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	background-color: white;\n"
"}")
        self.pB_Menu.setIcon(icon)
        self.pB_Menu.setIconSize(QSize(100, 13))
        self.pB_Menu.setCheckable(True)
        self.pB_Menu.setAutoExclusive(True)

        self.vL_topMenu.addWidget(self.pB_Menu)

        self.pB_Search = QPushButton(self.layoutWidget1)
        self.pB_Search.setObjectName(u"pB_Search")
        self.pB_Search.setMinimumSize(QSize(0, 40))
        self.pB_Search.setMaximumSize(QSize(16777215, 40))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(False)
        font2.setKerning(False)
        self.pB_Search.setFont(font2)
        self.pB_Search.setAutoFillBackground(False)
        self.pB_Search.setStyleSheet(u"QPushButton {\n"
"	text-align: left;\n"
"	padding-left: 10px;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	background-color: white;\n"
"}")
        self.pB_Search.setIcon(icon1)
        self.pB_Search.setIconSize(QSize(100, 20))
        self.pB_Search.setCheckable(True)
        self.pB_Search.setChecked(False)
        self.pB_Search.setAutoExclusive(True)

        self.vL_topMenu.addWidget(self.pB_Search)

        self.pB_Partner = QPushButton(self.layoutWidget1)
        self.pB_Partner.setObjectName(u"pB_Partner")
        self.pB_Partner.setMinimumSize(QSize(0, 40))
        self.pB_Partner.setMaximumSize(QSize(16777215, 40))
        self.pB_Partner.setFont(font2)
        self.pB_Partner.setStyleSheet(u"QPushButton {\n"
"	text-align: left;\n"
"	padding-left: 10px;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.pB_Partner.setIcon(icon2)
        self.pB_Partner.setIconSize(QSize(100, 17))
        self.pB_Partner.setCheckable(True)
        self.pB_Partner.setChecked(False)
        self.pB_Partner.setAutoExclusive(True)
        self.pB_Partner.setAutoDefault(False)
        self.pB_Partner.setFlat(False)

        self.vL_topMenu.addWidget(self.pB_Partner)


        self.vL_Menu.addLayout(self.vL_topMenu)

        self.vSpacer_Menu = QSpacerItem(20, 450, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.vL_Menu.addItem(self.vSpacer_Menu)

        self.vL_botMenu = QVBoxLayout()
        self.vL_botMenu.setSpacing(0)
        self.vL_botMenu.setObjectName(u"vL_botMenu")
        self.vL_botMenu.setContentsMargins(-1, 0, -1, 0)
        self.pB_Settings = QPushButton(self.layoutWidget1)
        self.pB_Settings.setObjectName(u"pB_Settings")
        self.pB_Settings.setMinimumSize(QSize(0, 40))
        self.pB_Settings.setMaximumSize(QSize(16777215, 40))
        self.pB_Settings.setFont(font2)
        self.pB_Settings.setStyleSheet(u"QPushButton {\n"
"	text-align: left;\n"
"	padding-left: 10px;\n"
"}")
        self.pB_Settings.setIcon(icon3)
        self.pB_Settings.setIconSize(QSize(100, 20))
        self.pB_Settings.setCheckable(True)
        self.pB_Settings.setAutoExclusive(True)

        self.vL_botMenu.addWidget(self.pB_Settings)

        self.pB_Logout = QPushButton(self.layoutWidget1)
        self.pB_Logout.setObjectName(u"pB_Logout")
        self.pB_Logout.setMinimumSize(QSize(0, 40))
        self.pB_Logout.setMaximumSize(QSize(16777215, 40))
        self.pB_Logout.setFont(font1)
        self.pB_Logout.setStyleSheet(u"QPushButton {\n"
"	text-align: left;\n"
"	padding-left: 10px;\n"
"}")
        self.pB_Logout.setIcon(icon4)
        self.pB_Logout.setIconSize(QSize(40, 16))
        self.pB_Logout.setCheckable(True)
        self.pB_Logout.setAutoExclusive(True)

        self.vL_botMenu.addWidget(self.pB_Logout)


        self.vL_Menu.addLayout(self.vL_botMenu)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.pB_Partner.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pB_MenuIcon.setText("")
        self.pB_SearchIcon.setText("")
        self.pB_PartnerIcon.setText("")
        self.pB_SettingsIcon.setText("")
        self.pB_LogoutIcon.setText("")
        self.label_PLZ.setText(QCoreApplication.translate("MainWindow", u"Postleitzahl", None))
        self.label_Flaeche.setText(QCoreApplication.translate("MainWindow", u"Fl\u00e4che", None))
        self.label_Strasse.setText(QCoreApplication.translate("MainWindow", u"Stra\u00dfe", None))
        self.label_Ort.setText(QCoreApplication.translate("MainWindow", u"Ort", None))
        self.comboBox_Partner.setItemText(0, QCoreApplication.translate("MainWindow", u"Partner", None))
        self.comboBox_Partner.setItemText(1, QCoreApplication.translate("MainWindow", u"Dachdecker", None))
        self.comboBox_Partner.setItemText(2, QCoreApplication.translate("MainWindow", u"Handel", None))

        self.comboBox_Begruenungsart.setItemText(0, QCoreApplication.translate("MainWindow", u"Extensiv", None))
        self.comboBox_Begruenungsart.setItemText(1, QCoreApplication.translate("MainWindow", u"Intensiv", None))
        self.comboBox_Begruenungsart.setItemText(2, QCoreApplication.translate("MainWindow", u"Verkehrsdach", None))

        self.pB_Suche.setText(QCoreApplication.translate("MainWindow", u"Suchen", None))
        self.pB_Menu.setText(QCoreApplication.translate("MainWindow", u"  Men\u00fc", None))
        self.pB_Search.setText(QCoreApplication.translate("MainWindow", u"  Suche", None))
        self.pB_Partner.setText(QCoreApplication.translate("MainWindow", u"  Partner", None))
        self.pB_Settings.setText(QCoreApplication.translate("MainWindow", u"  Einstellungen", None))
        self.pB_Logout.setText(QCoreApplication.translate("MainWindow", u"  Logout", None))
    # retranslateUi

