# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/discon_confirmation.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(408, 194)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.prompt_lb = QtWidgets.QLabel(Dialog)
        self.prompt_lb.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.prompt_lb.setObjectName("prompt_lb")
        self.gridLayout.addWidget(self.prompt_lb, 1, 0, 1, 1)
        self.disconnect_btn = QtWidgets.QPushButton(Dialog)
        self.disconnect_btn.setAutoFillBackground(True)
        self.disconnect_btn.setIconSize(QtCore.QSize(40, 40))
        self.disconnect_btn.setObjectName("disconnect_btn")
        self.gridLayout.addWidget(self.disconnect_btn, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)
        self.back_btn = QtWidgets.QPushButton(Dialog)
        self.back_btn.setIconSize(QtCore.QSize(35, 30))
        self.back_btn.setObjectName("back_btn")
        self.gridLayout.addWidget(self.back_btn, 3, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.prompt_lb.setText(_translate("Dialog", "Are you sure you want to disconnect?"))
        self.disconnect_btn.setText(_translate("Dialog", "Yes,  I am sure"))
        self.back_btn.setText(_translate("Dialog", "Oops,  I was wrong"))
