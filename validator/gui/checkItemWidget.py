from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView
import maya.OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
import maya.cmds as cmds
import os, posixpath
from .constants import *

current_directory = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_directory, os.pardir))


def main_window_pointer():
    ptr = OpenMayaUI.MQtUtil.mainWindow()  # pointer for the main window
    return wrapInstance(int(ptr), QtWidgets.QWidget)


class CheckWidget(QWidget):
    def __init__(self, error=None, label=None, action=None, fixed=None, parent=None):
        super(CheckWidget, self).__init__(parent)
        self.mainWindow = parent
        self.isExpanded = False
        self.label = label
        self.action = action
        self.error = error
        self.fixed = fixed

        self.centralLayout = QVBoxLayout(self)
        self.centralLayout.setContentsMargins(0, 1, 0, 0)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setAlignment(QtCore.Qt.AlignTop)

        # create header widget- wrapper for check button
        self.headerWidget = HeaderWidget(self, self.action)
        self.headerWidget.setFixedHeight(30)
        self.headerWidget.setLabel(self.label)
        self.headerWidget.mousePressEvent = self.hide_data_layout

        self.dataWidget = DataWidget(self)
        self.dataWidget.setVisible(False)

        # add layouts
        self.setLayout(self.centralLayout)
        self.centralLayout.addWidget(self.headerWidget)
        self.centralLayout.addWidget(self.dataWidget)

    def hide_data_layout(self, *args):
        if self.dataWidget.isVisible():
            self.dataWidget.setVisible(False)
            self.headerWidget.setArrow()
        else:
            self.dataWidget.setVisible(True)
            self.headerWidget.setArrow()

    def run_check(self, *args):
        isolate = cmds.optionVar(q=ISOLATEOPTION)
        exec('import ' + CHECKS_PATH + self.action + '.check')
        print(self.label.upper())
        self.returnList = None
        try:
            self.returnList = eval(CHECKS_PATH + self.action + '.check.main()')
        except ValueError:
            self.headerWidget.setLabel('Error in script!: ' + self.label)
            return self.error, self.fixed
        if self.returnList:
            self.dataWidget.addItem(self.returnList)
            self.headerWidget.set_color_error(self.error)
            self.headerWidget.set_fix_icon(self.fixed)
            return self.error, self.fixed
        else:
            self.dataWidget.addItem(self.returnList)
            self.headerWidget.set_color_error()
            if isolate:
                self.setVisible(False)

            return None, None

    def run_fix(self, *args):
        isolate = cmds.optionVar(q=ISOLATEOPTION)
        exec('import ' + CHECKS_PATH + self.action + '.fix')
        tmp = []

        for x in self.returnList:
            if not isinstance(x[1], (list, tuple)):
                tmp.append(x[1])
            else:
                tmp.extend(x[1])

        # in case these are compoments
        if len(tmp) > 255:
            print('MORE 255')
            newTmp = []
            for i in tmp:
                newTmp.append(i.split(".")[0])

            tmp = list(set(newTmp))

        try:
            self.returnList = eval(CHECKS_PATH + self.action + '.fix.main(' + str(tmp).strip("[]") + ')')
        except:
            self.returnList = eval(CHECKS_PATH + self.action + '.fix.main(' + str(tmp) + ')')

        if self.returnList:
            self.dataWidget.addItem(self.returnList)
        else:
            self.dataWidget.addItem(self.returnList)
            self.headerWidget.set_color_error()
            self.run_check()


class HeaderWidget(QWidget):
    def __init__(self, parent=None, action=None):
        super(HeaderWidget, self).__init__(parent)
        self.action = action
        self.headerLayout = QHBoxLayout(self)
        self.headerLayout.setContentsMargins(5, 1, 0, 1)

        self.setLayout(self.headerLayout)
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.inActiveColor = QColor(INACTIVE_COLOR[0], INACTIVE_COLOR[1], INACTIVE_COLOR[2])
        self.hoverColor = QColor(HOVER_COLOR[0], HOVER_COLOR[1], HOVER_COLOR[2], HOVER_COLOR[3])
        self.p.setColor(self.backgroundRole(), self.inActiveColor)
        self.setPalette(self.p)
        self.active = False

        # red button
        self.resultButton = QPushButton(self)
        self.resultButton.setFixedSize(13, 25)
        self.resultButton.setStyleSheet("border:0px;background: rgb(150, 150, 150);")

        # arrow button
        self.arrowButton = QLabel("", self)
        self.arrowButton.setFixedSize(13, 25)
        self.arrowButton.setStyleSheet("background:transparent;")
        self.arrowButton.setEnabled(False)

        # label
        self.checkLabel = QLabel(self)
        #
        # fix button
        self.fixButton = QPushButton(self)
        self.fixButton.setFixedSize(25, 25)
        self.fixButton.setVisible(True)
        self.fixButton.setIcon(QIcon(os.path.join(current_directory, CHECK_ICON)))
        self.fixButton.setIconSize(QSize(25, 25));
        self.fixButton.setStyleSheet("QPushButton {border:0px; background: rgb(0, 0, 0, 0);}")
        self.fixButton.clicked.connect(lambda: self.runCheck())

        # help button
        self.helpButton = HelpButton(self.action)

        # fix and help layout
        self.fix_widget = QWidget()
        self.fix_help_Layout = QHBoxLayout(self)
        self.fix_help_Layout.setContentsMargins(0, 0, 5, 0)
        self.fix_help_Layout.setAlignment(Qt.AlignRight)
        self.fix_help_Layout.addWidget(self.fixButton)
        self.fix_help_Layout.addWidget(self.helpButton)
        self.fix_help_Layout.addStretch(1)
        self.fix_widget.setLayout(self.fix_help_Layout)
        self.fix_widget.setFixedWidth(48)

        # #manage layout
        self.manage_widget = QWidget()
        self.result_label_Layout = QHBoxLayout(self)
        self.result_label_Layout.setContentsMargins(1, 1, 1, 0)
        self.result_label_Layout.setAlignment(Qt.AlignLeft)
        self.result_label_Layout.addWidget(self.resultButton)
        self.result_label_Layout.addWidget(self.arrowButton)
        self.result_label_Layout.addWidget(self.checkLabel)
        self.manage_widget.setLayout(self.result_label_Layout)

        self.headerLayout.addWidget(self.manage_widget)
        self.headerLayout.addWidget(self.fix_widget)

        self.isExpanded = False

        self.arrow_down = QPixmap(os.path.join(current_directory, ARROWDOWN_ICON))
        self.arrow_right = QPixmap(os.path.join(current_directory, ARROWRIGHT_ICON))
        self.arrowButton.setPixmap(self.arrow_right)

        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def resizeEvent(self, event):
        s = self.size()
        self.checkLabel.setMaximumWidth(int(s.width() - 104))

    def runCheck(self, *args):
        err, fix = self.parent().run_check()

    def set_color_error(self, err=None):
        if err == 'Warning':
            self.resultButton.setStyleSheet("border:0px;background: yellow;")
        elif err == 'Error':
            self.resultButton.setStyleSheet("border:0px;background: red;")
        else:
            self.resultButton.setStyleSheet("border:0px;background: green;")

    def setLabel(self, label):
        self.checkLabel.setText(label)

    def set_fix_icon(self, fix=None):
        if fix:
            self.fixButton.setIcon(QIcon(os.path.join(current_directory, FIX_ICON)))
            self.fixButton.clicked.disconnect()
            self.fixButton.clicked.connect(lambda: self.run_fix())

    def run_fix(self):
        fix = self.parent().run_fix()

    def setArrow(self):
        if self.isExpanded:
            self.isExpanded = False
            self.arrowButton.setPixmap(self.arrow_right)

        else:
            self.isExpanded = True
            self.arrowButton.setPixmap(self.arrow_down)

    def event(self, event):
        if event.type() == 10:
            if not self.active:
                self.p.setColor(self.backgroundRole(), self.hoverColor)
                self.setPalette(self.p)

        if event.type() == 11:
            if not self.active:
                self.p.setColor(self.backgroundRole(), self.inActiveColor)
                self.setPalette(self.p)

        return QWidget.event(self, event)


class DataWidget(QWidget):
    def __init__(self, parent=None):
        super(DataWidget, self).__init__(parent)
        self.dataMainLayout = QVBoxLayout()
        self.dataMainLayout.setAlignment(Qt.AlignTop)
        self.dataLayout = QHBoxLayout()
        self.dataLayout.setContentsMargins(0, 0, 0, 4)
        self.dataLayout.setSpacing(0)

        self.spacer = QSpacerItem(25, 0)

        # scroll Areya
        self.scrollArea = ExtendedQListWidget()
        defaultColor = self.scrollArea.palette().color(self.backgroundRole()).getRgb()
        self.scrollArea.setStyleSheet(
            "background-color: rgb(" + str(SCROLLAREA_COLOR[0]) + "," + str(SCROLLAREA_COLOR[1]) + "," + str(
                SCROLLAREA_COLOR[2]) + ");border: 0px solid")
        self.scrollArea.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.scrollArea.setFixedHeight(self.scrollArea.count() * 13 + 20)

        self.dataLayout.addItem(self.spacer)
        self.dataLayout.addWidget(self.scrollArea)

        self.dataMainLayout.addLayout(self.dataLayout)
        self.setLayout(self.dataMainLayout)

    def addItem(self, returnList):
        self.scrollArea.clear()
        for x in returnList:
            item = ExtendedQListWidgetItem(x[0], self.scrollArea)
            item.setSelection(x[1])
            self.scrollArea.addItem(item)
        self.scrollArea.setFixedHeight(self.scrollArea.count() * 13 + 20)

    def change_size_scroll(self):
        self.scrollArea.setFixedHeight(self.scrollArea.count() * 13 + 20)


class ExtendedQListWidget(QListWidget):
    def __init__(self, *args):
        super(ExtendedQListWidget, self).__init__(*args)

        self.itemSelectionChanged.connect(self.selectMayaObject)

    def selectMayaObject(self):
        if len(self.selectedItems()) != 0:
            cmds.select(cl=True)
            for x in self.selectedItems():
                try:
                    cmds.select(x.selection(), tgl=True)
                except:
                    find = str(x.text()).find(" -")
                    if find != -1:
                        try:
                            for z in str(x.text())[:find].split(","):
                                cmds.select(z, tgl=True)
                        except:
                            pass


class ExtendedQListWidgetItem(QListWidgetItem):
    def __init__(self, *args):
        super(ExtendedQListWidgetItem, self).__init__(*args)
        self.__selection = None

    def setSelection(self, selection):
        self.__selection = selection

    def selection(self):
        return self.__selection


class HelpButton(QWidget):
    def __init__(self, action=None, *args):
        super(HelpButton, self).__init__(*args)
        self.action = action
        self.__helpFile = None
        self.__helpText = None
        self.help_button_layout = QHBoxLayout(self)
        self.help_button_layout.setContentsMargins(5, 1, 1, 1)
        self.setLayout(self.help_button_layout)

        self.help_button = QPushButton(self)
        self.help_button.setFixedSize(12, 25)
        self.help_button.setVisible(True)
        self.help_button.setEnabled(self.exist_help())
        self.help_button.setIcon(QIcon(os.path.join(current_directory, QUESTION_ICON)))
        self.help_button.setStyleSheet("QPushButton {border:0px; \
													background: rgb(0, 0, 0, 0);\
													height: 80px;\
													}")

        self.help_button.clicked.connect(lambda: self.open_help())

        self.help_button_layout.addWidget(self.help_button)

    # class HelpButton (QPushButton):
    # 	def __init__(self, action = None, *args):
    # 		super(HelpButton, self).__init__(*args)
    # 		self.action = action
    # 		self.__helpFile = None
    # 		self.__helpText = None
    # 		self.setFixedSize(25, 25)
    # 		self.setVisible(True)
    # 		#self.setEnabled(True)
    # 		self.setEnabled(self.exist_help())
    # 		self.setIcon(QIcon(os.path.join(dir, QUESTION_ICON)))
    # 		self.setStyleSheet("QPushButton {border:0px; \
    # 													background: rgb(0, 0, 0, 0);\
    # 													height: 80px;\
    # 													}")

    # 		self.clicked.connect(lambda:self.open_help())

    def exist_help(self):
        self.help_htm = os.path.join(parent_dir, 'utils', 'checks', self.action, self.action + 'Help.htm')
        if os.path.exists(self.help_htm):
            return True
        else:
            return False

    def open_help(self):
        self.help = Browser(url=self.help_htm, title=self.action)
        self.help.show()


class Browser(QWidget):
    def __init__(self, parent=main_window_pointer(), url=None, title=None):
        super(Browser, self).__init__(parent)
        self.url = url
        self.title = title
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(self.title)
        cursorPosition = QCursor.pos()
        # self.setGeometry(cursorPosition.x(), cursorPosition.y(), 605, 800)
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout(self)  # main layout
        self.topLayout = QFrame()  # close layout
        self.topLayout.setMinimumHeight(8)
        self.topLayout.setMaximumHeight(8)

        vebWiew = QWebEngineView()
        url = QUrl.fromLocalFile(self.url)
        vebWiew.setUrl(url)

        self.mainLayout.addWidget(self.topLayout)
        self.mainLayout.addWidget(vebWiew)
