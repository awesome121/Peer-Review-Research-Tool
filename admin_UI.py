# Created by: PyQt5 UI code generator 5.15.6
from tokenize import Triple
from PyQt5 import QtCore, QtGui, QtWidgets

import sys

class Controller:
    def __init__(self, app, has_account) -> None:
        self.app = app
        self.qt_app = QtWidgets.QApplication(sys.argv)
        # print(1, flush=True)
        if has_account:
            self.land_on_dashboard()
        else:
            self.land_on_login()
        sys.exit(self.qt_app.exec())

    def land_on_login(self):
        self.login_window = LoginWindow(self)
        
    def land_on_dashboard(self):
        self.dashboard = Dashboard(self)

    def has_valid_token(self):
        return True if hasattr(self.app, 'token') else False

    def has_auth_flow(self):
        return True if hasattr(self.app, 'flow') else False

    def get_auth_flow_msg(self):
        return self.app.flow['message']

    def set_auth_success(self):
        self.app.set_auth_success()

    def clear_auth_flow(self):
        self.app.clear_auth_flow()

    def interrupt_auth_flow(self):
        self.app.interrupt_auth_flow()

    def try_connect(self):
        self.app.try_connect()
        


class LoginWindow:
    def __init__(self, controller):
        self.controller = controller
        self.setupUi()
        self.widget.show()

    def setupUi(self):
        self.widget = QtWidgets.QMainWindow()
        self.widget.setObjectName("login_window")
        self.widget.resize(360, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(320, 200))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 140))
        self.centralwidget = QtWidgets.QWidget(self.widget)
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
        self.widget.setCentralWidget(self.centralwidget)

        self.retranslateUi(self.widget)
        QtCore.QMetaObject.connectSlotsByName(self.widget)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("login_window", "login_window"))
        self.connect_btn.setText(_translate("login_window", "Connect"))
        self.account_lb.setText(_translate("login_window", "Email account:"))

    def connect_btn_onclick(self):
        self.controller.clear_auth_flow()
        self.hide()
        self.child = LoginDialog(self.controller, self)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()
        

class LoginDialog:
    def __init__(self, controller, parent):
        self.controller = controller
        self.widget = QtWidgets.QDialog()
        self.parent = parent
        self.controller.try_connect()
        self.setupUi()
        self.widget.exec()

    def setupUi(self):
        self.widget.setObjectName("Dialog")
        self.widget.resize(360, 200)
        self.prompt_lb = QtWidgets.QLabel(self.widget)
        self.prompt_lb.setGeometry(QtCore.QRect(30, 40, 281, 101))
        self.prompt_lb.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.prompt_lb.setObjectName("prompt_lb")
        self.prompt_lb.setWordWrap(True)
        self.prompt_lb.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.back_btn = QtWidgets.QPushButton(self.widget)
        self.back_btn.setGeometry(QtCore.QRect(0, 0, 41, 41))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("left-arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back_btn.setIcon(icon1)
        self.back_btn.setIconSize(QtCore.QSize(35, 30))
        self.back_btn.setObjectName("back_btn")
        self.back_btn.clicked.connect(self.back_btn_onclick)

        self.retranslateUi(self.widget)
        QtCore.QMetaObject.connectSlotsByName(self.widget)
        self.set_prompt()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Please follow the instruction"))

    def set_prompt(self):
        if not self.controller.has_auth_flow():
            print('waiting for flow')
            self.prompt_lb.setText('Waiting for response...')
            self.con_timer = QtCore.QTimer()
            self.con_timer.timeout.connect(self.set_prompt)  # execute `set_prompt`
            self.con_timer.setSingleShot(True)
            self.con_timer.setInterval(1000)
            self.con_timer.start()
        else:
            print('detected flow')
            self.prompt_lb.setText(self.controller.get_auth_flow_msg())
            self.detect_auth()

    def detect_auth(self):
        if self.controller.has_valid_token():
            print('detected token')
            self.has_detected_token = True
            self.controller.set_auth_success()
            self.widget.done(self.widget.Accepted)
            self.controller.land_on_dashboard()
        else:
            print('waiting for token')
            self.auth_timer = QtCore.QTimer()
            self.auth_timer.timeout.connect(self.detect_auth)
            self.auth_timer.setSingleShot(True)
            self.auth_timer.setInterval(1000)
            self.auth_timer.start()

    def back_btn_onclick(self):
        if self.controller.has_auth_flow():
            self.controller.interrupt_auth_flow()
        self.widget.done(self.widget.Accepted) 
        self.parent.show()

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    
class Dashboard:
    def __init__(self, controller):
        print('create dashboard')
        self.controller = controller
        self.widget = QtWidgets.QMainWindow()
        self.current_selected_tab_1 = None
        self.total_submission = None
        self.next_due_date = None
        self.total_review = None
        self.total_rating = None
        self.total_students = None
        self.server_email_address = None
        self.connection_status = None
        self.setupUi()
        self.widget.show()

    def setupUi(self):
        self.widget.setObjectName("Dashboard")
        self.widget.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self.widget)
        self.centralwidget.setObjectName("centralwidget")
        # Create a tabwidget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 841, 611))
        self.tabWidget.setObjectName("tabWidget")
        # Create our first tab
        self.tab_main = QtWidgets.QWidget()
        self.tab_main.setObjectName("tab_main")
        # Create objects for tab_main
        # Label used to show the current server's connection status
        self.label_1 = QtWidgets.QLabel(self.tab_main)
        self.label_1.setGeometry(QtCore.QRect(540, 10, 260, 21))
        self.label_1.setStyleSheet("font: 18pt \".AppleSystemUIFont\";")
        self.label_1.setObjectName("label_1")
        # Label used to show the total submisstions/reviews/ratings for the current deadline
        self.label_2 = QtWidgets.QLabel(self.tab_main)
        self.label_2.setGeometry(QtCore.QRect(0, 60, 800, 21))
        self.label_2.setStyleSheet("font: 18pt \".AppleSystemUIFont\";")
        self.label_2.setObjectName("label_2")
        self.label_2.setAlignment(QtCore.Qt.AlignLeft)
        # Label used to show the next due date
        self.label_3 = QtWidgets.QLabel(self.tab_main)
        self.label_3.setGeometry(QtCore.QRect(0, 80, 800, 21))
        self.label_3.setStyleSheet("font: 18pt \".AppleSystemUIFont\";")
        self.label_3.setObjectName("label_3")
        # Label used to show the total students
        self.label_4 = QtWidgets.QLabel(self.tab_main)
        self.label_4.setGeometry(QtCore.QRect(0, 100, 800, 21))
        self.label_4.setStyleSheet("font: 18pt \".AppleSystemUIFont\";")
        self.label_4.setObjectName("label_4")
        # CombBox which contains "Sbumission/Review/Rating"
        self.comboBox = QtWidgets.QComboBox(self.tab_main)
        self.comboBox.setGeometry(QtCore.QRect(80, 0, 111, 51))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        # Label for the CombBox
        self.label_5 = QtWidgets.QLabel(self.tab_main)
        self.label_5.setGeometry(QtCore.QRect(0, 10, 81, 21))
        self.label_5.setStyleSheet("font: 18pt \".AppleSystemUIFont\";")
        self.label_5.setObjectName("label_5")
        # Binding events to the function
        self.comboBox.currentTextChanged.connect(self.on_changed_combobox_tab_1)
        # PushButton. User can click on it and change the server status. (Connected/Disconnected)
        self.pushButton = QtWidgets.QPushButton(self.tab_main)
        self.pushButton.setGeometry(QtCore.QRect(600, 471, 120, 51))
        self.pushButton.setStyleSheet("color: rgb(74, 255, 14);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.on_clicked_button_tab_1)
        # Add tab_main to the tabWidget
        self.tabWidget.addTab(self.tab_main, "")
        # Create tab_students_details
        self.tab_students_details = QtWidgets.QWidget()
        self.tab_students_details.setObjectName("tab_students_details")
        # Add tab_students_details to the tabWidget
        self.tabWidget.addTab(self.tab_students_details, "")
        self.widget.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.widget.setStatusBar(self.statusbar)

        self.retranslateUi(self.widget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self.widget)

    def retranslateUi(self, dashboard):
        _translate = QtCore.QCoreApplication.translate
        dashboard.setWindowTitle(_translate("Dashboard", "Dashboard"))
        self.label_1.setText(_translate("Dashboard", f"Current Status: {self.connection_status}"))
        self.label_2.setText(_translate("Dashboard", f"Students submission submitted for current deadline: {self.total_submission}"))
        self.label_3.setText(_translate("Dashboard", f"Next Due Date: {self.next_due_date}"))
        self.label_4.setText(_translate("Dashboard", f"Total Students: {self.total_students}"))
        self.comboBox.setItemText(0, _translate("Dashboard", "Submission"))
        self.comboBox.setItemText(1, _translate("Dashboard", "Review"))
        self.comboBox.setItemText(2, _translate("Dashboard", "Rating"))
        self.label_5.setText(_translate("Dashboard", "Deadline:"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_main), _translate("Dashboard", "Main"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_students_details), _translate("Dashboard", "Students Details"))
    
    def on_changed_combobox_tab_1(self, selected_value):
        print("Combbox changed", selected_value)
        if selected_value == "Submission":
            self.label_2.setText(f"Students submissions submitted for current deadline: {self.total_submission}")
        elif selected_value == "Review":
            self.label_2.setText(f"Students reviews submitted for current deadline: {self.total_review}")
        elif selected_value == "Rating":
            self.label_2.setText(f"Students ratings submitted for current deadline: {self.total_rating}")

    def on_clicked_button_tab_1(self):
        if not self.controller.has_valid_token():
            self.connection_status = "Disconnected"
            # If disconnected. Token exist
            self.label_1.setText(f"Current Status: {self.connection_status}")
            self.pushButton.setText("Connect")
            self.label_1.setStyleSheet("color: rgb(255, 43, 32);font: 18pt \".AppleSystemUIFont\";")
            self.pushButton.setStyleSheet("color: rgb(74, 255, 14);")
        elif self.controller.has_valid_token():
            # If connected
            self.label_1.setText(f"Current Status: {self.connection_status}")
            self.label_1.setGeometry(QtCore.QRect(540, 10, 200, 21))
            self.label_1.setStyleSheet("color: rgb(255, 43, 32);font: 18pt \".AppleSystemUIFont\";")
            self.pushButton.setStyleSheet("color: rgb(255, 43, 32);")
        print("button cliecked")

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()
        



