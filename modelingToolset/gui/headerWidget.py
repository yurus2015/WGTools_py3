import os
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from .constants import *


class HeaderWidget(QWidget):
    def __init__(self, parent=None):
        super(HeaderWidget, self).__init__(parent)
        self.headerLayout = QHBoxLayout(self)
        self.headerLayout.setContentsMargins(5, 1, 1, 1)

        self.setLayout(self.headerLayout)
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.inActiveColor = QColor(INACTIVE_COLOR[0], INACTIVE_COLOR[1], INACTIVE_COLOR[2])
        self.hoverColor = QColor(HOVER_COLOR[0], HOVER_COLOR[1], HOVER_COLOR[2], HOVER_COLOR[3])
        self.p.setColor(self.backgroundRole(), self.inActiveColor)
        self.setPalette(self.p)
        self.active = False

        # arrow button
        self.arrowButton = QLabel("", self)
        self.arrowButton.setFixedSize(14, 14)
        self.arrowButton.setStyleSheet("background:transparent;")
        self.arrowButton.setEnabled(False)
        #
        # label
        self.checkLabel = QLabel(self)
        self.checkLabel.setStyleSheet("font-weight: bold;");
        #
        self.headerLayout.addWidget(self.arrowButton)
        self.headerLayout.addWidget(self.checkLabel)

        self.arrow_down = QPixmap(os.path.join(os.path.dirname(__file__), 'img', ARROWDOWN_ICON))
        self.arrow_right = QPixmap(os.path.join(os.path.dirname(__file__), 'img', ARROWRIGHT_ICON))

        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def setLabel(self, label):
        self.checkLabel.setText(label)

    # def set_fix_icon(self, fix = None):
    # 	if fix:
    # 		self.fixButton.setIcon(QIcon(os.path.join(dir, FIX_ICON)))
    # 		self.fixButton.clicked.disconnect()
    # 		self.fixButton.clicked.connect(lambda:self.run_fix())

    def run_fix(self):
        fix = self.parent().run_fix()

    def setArrow(self, expand):
        if expand:
            # self.isExpanded = False
            self.arrowButton.setPixmap(self.arrow_down)

        else:
            # self.isExpanded = True
            self.arrowButton.setPixmap(self.arrow_right)

    def event(self, event):
        if event.type() == 10:
            if not self.active:
                self.p.setColor(self.backgroundRole(), self.hoverColor)
                self.setPalette(self.p)
                return True

        if event.type() == 11:
            if not self.active:
                self.p.setColor(self.backgroundRole(), self.inActiveColor)
                self.setPalette(self.p)
                return True

        return QWidget.event(self, event)
    # return False
