from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
from PySide2.QtWebKitWidgets import QWebView, QWebFrame, QWebPage, QWebElement

import maya.OpenMayaUI as OpenMayaUI
import os
from .constants import VERSION

dir = os.path.dirname(__file__)

def getMayaWindow():
    main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)


class aboutWindow(QMainWindow):
    def __init__(self, parent = getMayaWindow()):
        super(aboutWindow, self).__init__(parent)

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.setWindowTitle('About')
        self.setFixedSize(280, 250)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.versionInfo = QLabel()
        self.versionInfo.setText(VERSION)
        self.versionInfo.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.icon = QLabel()
        self.icon.setPixmap(QPixmap(os.path.join(dir,'img', 'Wargaming.net_logo.png')))
        self.icon.setObjectName("icon")
        self.icon.setAlignment(QtCore.Qt.AlignHCenter)

        self.contacts = QLabel()
        self.contacts.setText(" Feel free to contac with developer for any questions\n or support")
        self.contacts.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.versionInfo)
        self.layout.addWidget(self.contacts)
        self.centralwidget.setLayout(self.layout)

