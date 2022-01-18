# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_mfa.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import time
from PyQt5 import QtCore, QtGui, QtWidgets

import sys


class AdminUI:
    def __init__(self, app, has_account):
        self.app = app
        self.qtApp = QtWidgets.QApplication(sys.argv)

        self.login_window = QtWidgets.QMainWindow()
        self.setupUi(self.login_window)
        self.login_window.show()

        sys.exit(self.qtApp.exec())

    def setupUi(self, login_window):
        login_window.setObjectName("login_window")
        login_window.resize(360, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(login_window.sizePolicy().hasHeightForWidth())
        login_window.setSizePolicy(sizePolicy)
        login_window.setMinimumSize(QtCore.QSize(320, 200))
        login_window.setMaximumSize(QtCore.QSize(16777215, 140))
        self.centralwidget = QtWidgets.QWidget(login_window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.connect_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.connect_btn.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.connect_btn.setObjectName("connect_btn")
        self.connect_btn.clicked.connect(self.connect_btn_onclick)

        self.gridLayout.addWidget(self.connect_btn, 1, 0, 1, 3)
        self.account_lb = QtWidgets.QLabel(self.centralwidget)
        self.account_lb.setObjectName("account_lb")
        self.gridLayout.addWidget(self.account_lb, 0, 0, 1, 1)
        self.account_input = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.account_input.sizePolicy().hasHeightForWidth())
        self.account_input.setSizePolicy(sizePolicy)
        self.account_input.setMinimumSize(QtCore.QSize(0, 0))
        self.account_input.setObjectName("account_input")
        self.gridLayout.addWidget(self.account_input, 0, 1, 1, 2)
        login_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(login_window)
        QtCore.QMetaObject.connectSlotsByName(login_window)

    def retranslateUi(self, login_window):
        _translate = QtCore.QCoreApplication.translate
        login_window.setWindowTitle(_translate("login_window", "login_window"))
        self.connect_btn.setText(_translate("login_window", "Connect"))
        self.account_lb.setText(_translate("login_window", "Email account:"))

    

    def connect_btn_onclick(self):
        self.app.clear_auth()
        self.dialog = QtWidgets.QDialog()
        child = Ui_Dialog(self.app, self.login_window)
        child.setupUi(self.dialog)
        self.login_window.hide()
        # time.sleep(1)
        child.set_prompt()
        self.dialog.exec()
        
            


class Ui_Dialog(object):
    def __init__(self, app, parent):
        self.app = app
        self.parent = parent
        self.app.try_connect()

    def setupUi(self, dialog):
        self.window = dialog
        self.window.setObjectName("Dialog")
        self.window.resize(360, 200)
        self.prompt_lb = QtWidgets.QLabel(self.window)
        self.prompt_lb.setGeometry(QtCore.QRect(30, 40, 281, 101))
        self.prompt_lb.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.prompt_lb.setObjectName("prompt_lb")
        self.prompt_lb.setWordWrap(True)
        self.prompt_lb.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.back_btn = QtWidgets.QPushButton(self.window)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 41, 41))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("left-arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back_btn.setIcon(icon1)
        self.back_btn.setIconSize(QtCore.QSize(35, 30))
        self.back_btn.setObjectName("back_btn")
        self.back_btn.clicked.connect(self.back_btn_onclick)

        self.retranslateUi(self.window)
        QtCore.QMetaObject.connectSlotsByName(self.window)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Please follow the instruction"))

    def set_prompt(self):
        if not hasattr(self.app, 'flow'):
            self.prompt_lb.setText('Waiting for response...')
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.set_prompt)  # execute `display_time`
            self.timer.setInterval(5)
            self.timer.start()
        else:
            self.prompt_lb.setText(self.app.flow["message"])
        


    def back_btn_onclick(self):
            self.app.flow['expires_at'] = 0
