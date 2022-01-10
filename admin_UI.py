from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


class Admin_UI:
    def __init__(self, has_account):
        Form, Window = uic.loadUiType("V1.ui") #your ui file
        app = QApplication([])
        window = Window()
        form = Form()
        form.setupUi(window)
        window.show()
        app.exec()