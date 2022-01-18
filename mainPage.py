from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def __init__(self, app):
        self.app = app
        self.current_selected_tab_1 = None
        self.total_submission = None
        self.next_due_date = None
        self.total_review = None
        self.total_rating = None
        self.total_students = None
        
        self.server_email_address = None
        self.connection_status = None

        

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_1.setText(_translate("MainWindow", f"Current Status: {self.connection_status}"))
        self.label_2.setText(_translate("MainWindow", f"Students submission submitted for current deadline: {self.total_submission}"))
        self.label_3.setText(_translate("MainWindow", f"Next Due Date: {self.next_due_date}"))
        self.label_4.setText(_translate("MainWindow", f"Total Students: {self.total_students}"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Submission"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Review"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Rating"))
        self.label_5.setText(_translate("MainWindow", "Deadline:"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_main), _translate("MainWindow", "Main"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_students_details), _translate("MainWindow", "Students Details"))
    
    def on_changed_combobox_tab_1(self, selected_value):
        print("Combbox changed", selected_value)
        if selected_value == "Submission":
            self.label_2.setText(f"Students submissions submitted for current deadline: {self.total_submission}")
        elif selected_value == "Review":
            self.label_2.setText(f"Students reviews submitted for current deadline: {self.total_review}")
        elif selected_value == "Rating":
            self.label_2.setText(f"Students ratings submitted for current deadline: {self.total_rating}")

    def on_clicked_button_tab_1(self):
        if not self.app.token:
            self.connection_status = "Disconnected"

            # If disconnected. Token exist
            self.label_1.setText(f"Current Status: {self.connection_status}")
            self.pushButton.setText("Connect")
            self.label_1.setStyleSheet("color: rgb(255, 43, 32);font: 18pt \".AppleSystemUIFont\";")
            self.pushButton.setStyleSheet("color: rgb(74, 255, 14);")
        elif self.app.token:
            # If connected
            self.label_1.setText(f"Current Status: {self.connection_status}")
            self.label_1.setGeometry(QtCore.QRect(540, 10, 200, 21))
            self.label_1.setStyleSheet("color: rgb(255, 43, 32);font: 18pt \".AppleSystemUIFont\";")
            self.pushButton.setStyleSheet("color: rgb(255, 43, 32);")
        print("button cliecked")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
