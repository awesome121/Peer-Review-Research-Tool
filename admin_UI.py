# Created by: PyQt5 UI code generator 5.15.6

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import database, os, time

import sys

class Controller:
    def __init__(self, app, has_account) -> None:
        # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        # QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        self.app = app
        self.db = database.Database()
        self.qtapp = QtWidgets.QApplication(sys.argv)
        self.qtapp.setApplicationName("Peer Review Dashboard")
        self.dashboard = None
        if has_account:
            self.land_on_dashboard()
        else:
            self.land_on_login()
        self.set_qtapp_icon()
        sys.exit(self.qtapp.exec())

    def set_qtapp_icon(self):
        app_icon = QtGui.QIcon()
        app_icon.addFile('icons/app-icon.png', QtCore.QSize(256,256))
        self.qtapp.setWindowIcon(app_icon)

    def land_on_login(self):
        self.login_window = LoginWindow(self)
        
    def land_on_dashboard(self):
        self.dashboard = Dashboard(self)

    def has_valid_token(self):
        return True if hasattr(self.app, 'token') and self.app.token is not None else False

    def has_auth_flow(self):
        return True if hasattr(self.app, 'flow') and self.app.flow is not None else False

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

    def disconnect(self):
        self.app.disconnect()


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
        self.parent = parent
        self.widget = QtWidgets.QDialog()
        self.has_active_widget = True # used to break timer
        self.controller.try_connect()
        self.setupUi()

        dialog_code = self.widget.exec()
        self.has_active_widget = False

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
        icon1.addPixmap(QtGui.QPixmap("icons/left-arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        if self.has_active_widget:
            if self.controller.has_valid_token():
                print('detected token')
                self.has_detected_token = True
                self.controller.set_auth_success()
                self.widget.done(self.widget.Accepted)
                if not self.controller.dashboard:
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
        self.controller = controller
        self.widget = QtWidgets.QMainWindow()
        self.current_selected_tab_1 = None
        self.total_submission = None
        self.next_due_date = None
        self.total_review = None
        self.total_rating = None
        self.total_students = None
        self.server_email_address = None
        self.connection_status = False
        self.setupUi(self.widget)
        self.update_conn_status()
        self.widget.show()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(780, 737)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tab = QtWidgets.QTabWidget(self.centralwidget)
        self.tab.setObjectName("tab")
        self.summary_tab = QtWidgets.QWidget()
        self.summary_tab.setObjectName("summary_tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.summary_tab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.summary_tab)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.student_total_lb = QtWidgets.QLabel(self.summary_tab)
        self.student_total_lb.setObjectName("student_total_lb")
        self.horizontalLayout.addWidget(self.student_total_lb)
        self.gridLayout_4.addLayout(self.horizontalLayout, 2, 2, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.summary_tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.submitted_lb = QtWidgets.QLabel(self.summary_tab)
        self.submitted_lb.setObjectName("submitted_lb")
        self.gridLayout_2.addWidget(self.submitted_lb, 2, 1, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.summary_tab)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout_2.addWidget(self.comboBox_2, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.summary_tab)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.dl_due_lb = QtWidgets.QLabel(self.summary_tab)
        self.dl_due_lb.setObjectName("dl_due_lb")
        self.gridLayout_2.addWidget(self.dl_due_lb, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.summary_tab)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 1, 2, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.summary_tab)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_4.addWidget(self.line_2, 1, 1, 1, 1)
        self.line = QtWidgets.QFrame(self.summary_tab)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_4.addWidget(self.line, 2, 1, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_15 = QtWidgets.QLabel(self.summary_tab)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 3, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.summary_tab)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.summary_tab)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 4, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.summary_tab)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 2, 0, 1, 1)
        self.last_conn_from = QtWidgets.QLabel(self.summary_tab)
        self.last_conn_from.setText("")
        self.last_conn_from.setObjectName("last_conn_from")
        self.gridLayout_3.addWidget(self.last_conn_from, 3, 1, 1, 1)
        self.last_conn_to = QtWidgets.QLabel(self.summary_tab)
        self.last_conn_to.setText("")
        self.last_conn_to.setObjectName("last_conn_to")
        self.gridLayout_3.addWidget(self.last_conn_to, 4, 1, 1, 1)
        self.conn_status_lb = QtWidgets.QLabel(self.summary_tab)
        self.conn_status_lb.setObjectName("conn_status_lb")
        self.gridLayout_3.addWidget(self.conn_status_lb, 0, 1, 1, 1)
        self.conn_btn = QtWidgets.QPushButton(self.summary_tab)
        self.conn_btn.setObjectName("conn_btn")
        self.gridLayout_3.addWidget(self.conn_btn, 1, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.tab.addTab(self.summary_tab, "")
        self.students_tab = QtWidgets.QWidget()
        self.students_tab.setObjectName("students_tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.students_tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.search_lineedit = QtWidgets.QLineEdit(self.students_tab)
        self.search_lineedit.setPlaceholderText("Type student's email to search")
        self.search_lineedit.setObjectName("search_lineedit")
        self.gridLayout.addWidget(self.search_lineedit, 0, 2, 1, 1)
        self.remove_btn = QtWidgets.QPushButton(self.students_tab)
        self.remove_btn.setStyleSheet("color: rgb(102, 0, 0);") # disable color
        self.remove_btn.setObjectName("remove_btn")
        self.remove_btn.setDisabled(True)
        self.gridLayout.addWidget(self.remove_btn, 3, 2, 1, 1)
        self.student_detail_tb = QtWidgets.QTableWidget(1, 1, self.students_tab)
        self.student_detail_tb.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.student_detail_tb.setObjectName("student_detail_tb")
        self.student_detail_tb.setHorizontalHeaderLabels(('Student Email Address',))
        self.student_detail_tb.horizontalHeader().setSectionResizeMode(0, \
                                            QtWidgets.QHeaderView.Stretch)
        # self.student_detail_tb.setColumnWidth(300, 300)
        self.gridLayout.addWidget(self.student_detail_tb, 1, 1, 1, 2)
        self.import_btn = QtWidgets.QPushButton(self.students_tab)
        self.import_btn.setObjectName("import_btn")
        self.gridLayout.addWidget(self.import_btn, 0, 1, 1, 1)
        self.add_btn = QtWidgets.QPushButton(self.students_tab)
        self.add_btn.setObjectName("add_btn")
        self.gridLayout.addWidget(self.add_btn, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tab.addTab(self.students_tab, "")
        self.deadlines_tab = QtWidgets.QWidget()
        self.deadlines_tab.setObjectName("deadlines_tab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.deadlines_tab)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.deadline_tb = QtWidgets.QTableWidget(self.deadlines_tab)
        self.deadline_tb.setObjectName("deadline_tb")
        self.deadline_tb.setColumnCount(0)
        self.deadline_tb.setRowCount(0)
        self.gridLayout_5.addWidget(self.deadline_tb, 0, 0, 1, 1)
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.remove_selected_btn = QtWidgets.QPushButton(self.deadlines_tab)
        self.remove_selected_btn.setObjectName("remove_selected_btn")
        self.gridLayout_11.addWidget(self.remove_selected_btn, 1, 2, 1, 1)
        self.new_schedule_btn = QtWidgets.QPushButton(self.deadlines_tab)
        self.new_schedule_btn.setObjectName("new_schedule_btn")
        self.gridLayout_11.addWidget(self.new_schedule_btn, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem1, 1, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_11, 1, 0, 1, 1)
        self.tab.addTab(self.deadlines_tab, "")
        self.verticalLayout_2.addWidget(self.tab)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # add listener
        self.import_btn.clicked.connect(self.import_btn_onclick)
        self.conn_btn.clicked.connect(self.conn_btn_onclick)
        self.remove_btn.clicked.connect(self.remove_student_btn_onclick)
        self.add_btn.clicked.connect(self.add_btn_onclick)
        self.search_lineedit.textEdited.connect(self.search_lineedit_onedited)
        self.student_detail_tb.itemSelectionChanged.connect(self.student_detail_tb_onselect)
        self.new_schedule_btn.clicked.connect(self.new_schedule_btn_onclick)
        self.student_detail_tb.itemDoubleClicked.connect(self.student_doubleClick)
        # update tables
        self.update_student_detail_tb()



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dashboard"))
        self.label_4.setText(_translate("MainWindow", "Students Total"))
        self.student_total_lb.setText(_translate("MainWindow", "40"))
        self.label_2.setText(_translate("MainWindow", "Current Deadline:"))
        self.submitted_lb.setText(_translate("MainWindow", "0/40"))
        self.label_6.setText(_translate("MainWindow", "Submitted"))
        self.dl_due_lb.setText(_translate("MainWindow", "04/3/22"))
        self.label_5.setText(_translate("MainWindow", "Due Date:"))
        self.label_15.setText(_translate("MainWindow", "From:"))
        self.label_7.setText(_translate("MainWindow", "Current Status:"))
        self.label_13.setText(_translate("MainWindow", "To:"))
        self.label_16.setText(_translate("MainWindow", "Last Connection"))
        self.conn_status_lb.setText(_translate("MainWindow", "Connected"))
        self.conn_btn.setText(_translate("MainWindow", "Connect"))
        self.tab.setTabText(self.tab.indexOf(self.summary_tab), _translate("MainWindow", "Summary"))
        self.search_lineedit.setPlaceholderText(_translate("MainWindow", "Type email address to search"))
        self.remove_btn.setText(_translate("MainWindow", "Remove selected student(s)"))
        self.import_btn.setText(_translate("MainWindow", "Import Students From CSV"))
        self.add_btn.setText(_translate("MainWindow", "Add a student"))
        self.tab.setTabText(self.tab.indexOf(self.students_tab), _translate("MainWindow", "Students"))
        self.remove_selected_btn.setText(_translate("MainWindow", "Remove Selected"))
        self.new_schedule_btn.setText(_translate("MainWindow", "New Schedule"))
        self.tab.setTabText(self.tab.indexOf(self.deadlines_tab), _translate("MainWindow", "Deadlines"))
    
    def new_schedule_btn_onclick(self):
        self.child = ScheduleDialog(self.controller, self)

    def student_doubleClick(self, item):
        StudentDetailDialog(self.controller, self, item.text())


    def search_lineedit_onedited(self):
        results = self.controller.db.get_author_by_prefix(self.search_lineedit.text())
        self.update_student_detail_tb(results)

    def import_btn_onclick(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self.widget,"Open File", "",\
                                                    "CSV Files (*.csv)")
        if filename:
            buttonReply = QtWidgets.QMessageBox.question(self.widget, 'Message Box', \
                                    "Are you sure you want to insert students from this csv file?"\
                                    , QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
            if buttonReply == QtWidgets.QMessageBox.Yes:
                self.controller.db.update_email_list(filename)
                self.update_student_detail_tb()

    def add_btn_onclick(self):
        input_text, ok = QtWidgets.QInputDialog.getText(self.widget, "", "Please type student's email address")
        while ok:
            input_text = input_text.strip()
            addr = input_text.split('@')
            if len(addr) == 2 and addr[0] != '' and addr[1] != '':
                is_added = self.controller.db.add_addr(input_text)
                time.sleep(1)
                if is_added:
                    QtWidgets.QMessageBox.information(self.widget, '', \
                                    f"'{input_text}' is successfully added")
                    self.update_student_detail_tb()
                    self.student_detail_tb.scrollToBottom()
                    items = self.student_detail_tb.findItems(input_text, QtCore.Qt.MatchExactly)

                else:
                    QtWidgets.QMessageBox.information(self.widget, '', \
                                    f"'{input_text}' already exists")  
                    items = self.student_detail_tb.findItems(input_text, QtCore.Qt.MatchExactly)
                    self.student_detail_tb.scrollToItem(items[0], QtWidgets.QAbstractItemView.PositionAtCenter)
                self.student_detail_tb.clearSelection()
                items[0].setSelected(True)
                ok = False
            else:
                QtWidgets.QMessageBox.warning(self.widget, '', \
                                    "Not a valid email address")
                input_text, ok = QtWidgets.QInputDialog.getText(self.widget, \
                                "", "Please type student's email address", text=input_text)

    def remove_student_btn_onclick(self):
        idxs = self.student_detail_tb.selectedIndexes()
        if idxs:
            msg = f"Are you sure you want to remove {len(idxs)} selected student(s)?\n\n"
            for idx in idxs[:5]:
                msg += idx.data() + "\n"
            msg += "........." if len(idxs) > 5 else ''
            buttonReply = QtWidgets.QMessageBox.question(self.widget, 'Message Box', msg
                                    , QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
            if buttonReply == QtWidgets.QMessageBox.Yes:
                rows = [idx.data() for idx in idxs]
                self.controller.db.remove_email_addr(rows)
                self.update_student_detail_tb()

    def student_detail_tb_onselect(self):
        idxs = self.student_detail_tb.selectedIndexes()
        if len(idxs) == 0:
            self.remove_btn.setEnabled(False)
            self.remove_btn.setStyleSheet("color: rgb(102, 0, 0);") # enable color
            self.remove_btn.setText(f"Remove selected student(s)")
        else:
            self.remove_btn.setEnabled(True)
            self.remove_btn.setStyleSheet("color: rgb(255, 54, 53);") # enable color
            if len(idxs) == 1:
                self.remove_btn.setText(f"Remove 1 selected student")
            else:
                self.remove_btn.setText(f"Remove {len(idxs)} selected students")

    # def on_changed_combobox_tab_1(self, selected_value):
    #     print("Combbox changed", selected_value)
    #     if selected_value == "Submission":
    #         self.label_2.setText(f"Students submissions submitted for current deadline: {self.total_submission}")
    #     elif selected_value == "Review":
    #         self.label_2.setText(f"Students reviews submitted for current deadline: {self.total_review}")
    #     elif selected_value == "Rating":
    #         self.label_2.setText(f"Students ratings submitted for current deadline: {self.total_rating}")

    def conn_btn_onclick(self):
        print("click button, popping dialog")
        if not self.controller.has_valid_token():
            self.child = LoginDialog(self.controller, self)
        else:
            self.child = DisconnectDialog(self.controller, self)
        self.update_conn_status()

    def update_conn_status(self):
        if not self.controller.has_valid_token():
            self.connection_status = "Disconnected"
            # If disconnected. Token exist
            self.conn_status_lb.setText(f"{self.connection_status}")
            # self.conn_btn.setText("Connect")
            self.conn_status_lb.setStyleSheet("color: rgb(255, 43, 32);font: 18pt \".AppleSystemUIFont\";")
            # self.conn_btn.setStyleSheet("color: rgb(20, 102, 26);")
        elif self.controller.has_valid_token():
            # If connected
            self.connection_status = "Connected"
            self.conn_status_lb.setText(f"{self.connection_status}")
            self.conn_status_lb.setGeometry(QtCore.QRect(540, 10, 200, 21))
            self.conn_status_lb.setStyleSheet("color: rgb(20, 102, 26);font: 18pt \".AppleSystemUIFont\";")
            # self.conn_btn.setText("Disconnect")
            # self.conn_btn.setStyleSheet("color: rgb(255, 43, 32);") # red

    def update_student_detail_tb(self, addresses=None):
        if not addresses:
            addresses = self.controller.db.get_all_email_addr()
        self.student_detail_tb.clearContents()
        self.student_detail_tb.setRowCount(len(addresses))
        for i in range(len(addresses)):
            self.student_detail_tb.setItem(i-1, 1,  QtWidgets.QTableWidgetItem(addresses[i]))

    def update_students_total(self):
        student_total = self.db.get_subscriber_total()
        self.student_total_lb.setText(f'{student_total}')

    def update_ddl_panel(self, deadline_item):
        name, id = deadline_item.split()
        due_date = self.db.get_ddl_by_id(id, name)
        self.ddl_due_lb.setText(f'{due_date}')
        if name == 'submission':
            submitted_lb_text = f'{self.db.get_num_item_by_id(id, name)}/{self.db.get_subscriber_total()}'
        elif name == 'review':
            submitted_lb_text = f'{self.db.get_num_item_by_id(id, name)}/{self.db.get_subscriber_total() * 3}'
        elif name == 'evaluation':
            submitted_lb_text = f'{self.db.get_num_item_by_id(id, name)}/{self.db.get_subscriber_total() * 3}'
        self.submitted_lb.setText(submitted_lb_text)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

class StudentDetailDialog:
    def __init__(self, controller, parent, email_addr):
        self.controller = controller
        self.parent = parent
        self.email_addr = email_addr
        self.widget = QtWidgets.QDialog(parent=self.parent.widget)
        self.setupUi(self.widget)
        self.widget.setModal(QtCore.Qt.ApplicationModal)
        self.widget.show()
        self.update_subm_panel_as_author()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(831, 638)
        Dialog.setWindowTitle("")
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.addr_lb = QtWidgets.QLabel(Dialog)
        self.addr_lb.setObjectName("addr_lb")
        self.gridLayout.addWidget(self.addr_lb, 0, 0, 1, 1)
        self.bottom_left_tb = QtWidgets.QTableWidget(Dialog)
        self.bottom_left_tb.setObjectName("bottom_left_tb")
        self.bottom_left_tb.setColumnCount(0)
        self.bottom_left_tb.setRowCount(0)
        self.gridLayout.addWidget(self.bottom_left_tb, 6, 0, 1, 1)
        self.top_right_tb = QtWidgets.QTableWidget(Dialog)
        self.top_right_tb.setObjectName("top_right_tb")

        self.gridLayout.addWidget(self.top_right_tb, 3, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 1, 1, 1)
        self.bottom_right_tb = QtWidgets.QTableWidget(Dialog)
        self.bottom_right_tb.setObjectName("bottom_right_tb")
        self.bottom_right_tb.setColumnCount(0)
        self.bottom_right_tb.setRowCount(0)
        self.gridLayout.addWidget(self.bottom_right_tb, 6, 2, 1, 1)
        self.top_textedit = QtWidgets.QTextEdit(Dialog)
        self.top_textedit.setObjectName("top_textedit")
        self.gridLayout.addWidget(self.top_textedit, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.bottom_textedit = QtWidgets.QTextEdit(Dialog)
        self.bottom_textedit.setObjectName("bottom_textedit")
        self.gridLayout.addWidget(self.bottom_textedit, 5, 2, 1, 1)

        self.top_left_tb = QtWidgets.QTableWidget(1, 2, Dialog)
        self.top_left_tb.setObjectName("top_left_tb")
        self.top_left_tb.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.top_left_tb.setHorizontalHeaderLabels(('Submission ID','Date'))
        self.top_left_tb.horizontalHeader().setSectionResizeMode(\
                                            QtWidgets.QHeaderView.Stretch)
        self.top_left_tb.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.gridLayout.addWidget(self.top_left_tb, 3, 0, 1, 1)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 4, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # listener
        self.top_left_tb.itemDoubleClicked.connect(self.top_left_tb_doubleclicked)
        print('listener')

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.addr_lb.setText(_translate("Dialog", self.email_addr))
        self.label_4.setText(_translate("Dialog", "is reviewed by"))
        self.label_3.setText(_translate("Dialog", "also reviewed by"))
        self.label.setText(_translate("Dialog", "Student has submitted:"))
        self.label_2.setText(_translate("Dialog", "has reviewed:"))

    def top_left_tb_doubleclicked(self, item):
        self.addr_lb.setText('----')
        

    def update_subm_panel_as_author(self):
        subm_list_as_author = self.controller.db.get_subm_id_by_author(self.email_addr)
        self.top_left_tb.clearContents()
        self.top_left_tb.setRowCount(len(subm_list_as_author))
        for i in range(len(subm_list_as_author)):
            self.top_left_tb.setItem(i, 0,  QtWidgets.QTableWidgetItem(str(subm_list_as_author[i][0])))
            self.top_left_tb.setItem(i, 1,  QtWidgets.QTableWidgetItem(str(subm_list_as_author[i][1])))

        


class ScheduleDialog:
    def __init__(self, controller, parent):
        self.controller = controller
        self.parent = parent
        self.widget = QtWidgets.QDialog(parent=self.parent.widget)
        self.setupUi(self.widget)
        self.widget.setModal(QtCore.Qt.ApplicationModal)
        self.widget.show()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(662, 151)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.eval_dtedit = QtWidgets.QDateTimeEdit(Dialog, calendarPopup=True)
        self.eval_dtedit.setObjectName("eval_dtedit")
        self.gridLayout.addWidget(self.eval_dtedit, 3, 1, 1, 1)
        self.review_dtedit = QtWidgets.QDateTimeEdit(Dialog, calendarPopup=True)
        self.review_dtedit.setObjectName("review_dtedit")
        self.gridLayout.addWidget(self.review_dtedit, 2, 1, 1, 1)
        self.subm_id_lb = QtWidgets.QLabel(Dialog)
        self.subm_id_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.subm_id_lb.setObjectName("subm_id_lb")
        self.gridLayout.addWidget(self.subm_id_lb, 0, 1, 1, 1)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 2, 4, 1)
        self.confirm_btn = QtWidgets.QPushButton(Dialog)
        self.confirm_btn.setObjectName("confirm_btn")
        self.gridLayout.addWidget(self.confirm_btn, 3, 3, 1, 1)
        self.timezone_combobox = QtWidgets.QComboBox(Dialog)
        self.timezone_combobox.setObjectName("timezone_combobox")
        self.gridLayout.addWidget(self.timezone_combobox, 1, 3, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.subm_dtedit = QtWidgets.QDateTimeEdit(Dialog, calendarPopup=True)
        self.subm_dtedit.setObjectName("subm_dtedit")
        self.gridLayout.addWidget(self.subm_dtedit, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.cancel_btn = QtWidgets.QPushButton(Dialog)
        self.cancel_btn.setObjectName("cancel_btn")
        self.gridLayout.addWidget(self.cancel_btn, 3, 4, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        # # ==================================
        # self.dateeidt = QtWidgets.QDateTimeEdit(self.deadline_tb, calendarPopup=True)
        # self.gridLayout_5.addWidget(self.dateeidt, 0, 0, 1, 1)
        # # self.widget.menuBar().setCornerWidget(self.dateeidt, QtCore.Qt.Corner.TopLeftCorner)
        # self.dateeidt.setDateTime(QtCore.QDateTime.currentDateTime())
        # # ==================================
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        #listener
        self.cancel_btn.clicked.connect(self.cancel_btn_onclick)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Schedule"))
        self.subm_id_lb.setText(_translate("Dialog", "1"))
        self.confirm_btn.setText(_translate("Dialog", "Confirm"))
        self.label.setText(_translate("Dialog", "Submission ID"))
        self.label_4.setText(_translate("Dialog", "Evaluation Deadline"))
        self.label_6.setText(_translate("Dialog", "Time Zone"))
        self.label_3.setText(_translate("Dialog", "Review Deadline"))
        self.label_2.setText(_translate("Dialog", "Submission Deadline (Distribution Time)"))
        self.cancel_btn.setText(_translate("Dialog", "Cancel"))
  
    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def cancel_btn_onclick(self):
        self.widget.done(self.widget.Accepted)


class DisconnectDialog:
    def __init__(self, controller, parent) -> None:
        self.controller = controller
        self.parent = parent
        self.widget = QtWidgets.QDialog()
        self.setupUi(self.widget)
        self.widget.show()

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
        self.disconnect_btn.clicked.connect(self.disconnect_btn_onclick)
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
        self.back_btn.clicked.connect(self.back_btn_onclick)
        self.gridLayout.addWidget(self.back_btn, 3, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def back_btn_onclick(self):
        self.widget.done(self.widget.Accepted)

    def disconnect_btn_onclick(self):
        self.controller.disconnect()
        print('disconnect')
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.parent.update_conn_status)
        self.timer.setSingleShot(True)
        self.timer.setInterval(1000)
        self.timer.start()
        self.widget.done(self.widget.Accepted)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.prompt_lb.setText(_translate("Dialog", "Are you sure you want to disconnect?"))
        self.disconnect_btn.setText(_translate("Dialog", "Yes,  I am sure"))
        self.back_btn.setText(_translate("Dialog", "Oops,  I was wrong"))

