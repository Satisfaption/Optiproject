# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Login_window.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_w_LoginForm(object):
    def setupUi(self, w_LoginForm):
        if not w_LoginForm.objectName():
            w_LoginForm.setObjectName(u"w_LoginForm")
        w_LoginForm.resize(279, 477)
        font = QFont()
        font.setPointSize(12)
        w_LoginForm.setFont(font)
        self.gridLayout = QGridLayout(w_LoginForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_gast = QPushButton(w_LoginForm)
        self.pushButton_gast.setObjectName(u"pushButton_gast")
        self.pushButton_gast.setMinimumSize(QSize(150, 0))

        self.gridLayout.addWidget(self.pushButton_gast, 8, 1, 1, 2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 8, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 8, 3, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_3, 6, 0, 1, 4)

        self.lineEdit_Password = QLineEdit(w_LoginForm)
        self.lineEdit_Password.setObjectName(u"lineEdit_Password")

        self.gridLayout.addWidget(self.lineEdit_Password, 5, 0, 1, 4)

        self.lineEdit_Username = QLineEdit(w_LoginForm)
        self.lineEdit_Username.setObjectName(u"lineEdit_Username")

        self.gridLayout.addWidget(self.lineEdit_Username, 3, 0, 1, 4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 4)

        self.label_Login = QLabel(w_LoginForm)
        self.label_Login.setObjectName(u"label_Login")
        self.label_Login.setMinimumSize(QSize(0, 50))
        self.label_Login.setMaximumSize(QSize(16777215, 50))
        font1 = QFont()
        font1.setPointSize(16)
        font1.setBold(True)
        self.label_Login.setFont(font1)
        self.label_Login.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_Login, 0, 0, 1, 4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 7, 3, 1, 1)

        self.pushButton_login = QPushButton(w_LoginForm)
        self.pushButton_login.setObjectName(u"pushButton_login")
        self.pushButton_login.setMinimumSize(QSize(150, 0))
        self.pushButton_login.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_login.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton_login.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_login, 7, 1, 1, 2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 7, 0, 1, 1)

        self.label_Password = QLabel(w_LoginForm)
        self.label_Password.setObjectName(u"label_Password")
        self.label_Password.setMinimumSize(QSize(0, 30))
        self.label_Password.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.label_Password, 4, 0, 1, 4)

        self.label_Username = QLabel(w_LoginForm)
        self.label_Username.setObjectName(u"label_Username")
        self.label_Username.setMinimumSize(QSize(0, 30))
        self.label_Username.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.label_Username, 2, 0, 1, 4)


        self.retranslateUi(w_LoginForm)

        self.pushButton_login.setDefault(False)


        QMetaObject.connectSlotsByName(w_LoginForm)
    # setupUi

    def retranslateUi(self, w_LoginForm):
        w_LoginForm.setWindowTitle(QCoreApplication.translate("w_LoginForm", u"Login", None))
        self.pushButton_gast.setText(QCoreApplication.translate("w_LoginForm", u"Gastzugang", None))
        self.label_Login.setText(QCoreApplication.translate("w_LoginForm", u"Login", None))
        self.pushButton_login.setText(QCoreApplication.translate("w_LoginForm", u"Login", None))
        self.label_Password.setText(QCoreApplication.translate("w_LoginForm", u"Passwort", None))
        self.label_Username.setText(QCoreApplication.translate("w_LoginForm", u"Benutzername", None))
    # retranslateUi

