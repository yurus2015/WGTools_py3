from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from .headerWidget import HeaderWidget
import maya.cmds as cmds


class ToolsWidget(QWidget):
    def __init__(self, label=None, action=None, parent=None):
        super(ToolsWidget, self).__init__(parent)
        self.mainWindow = parent
        self.isExpanded = True
        self.label = label
        self.action = action

        self.centralLayout = QVBoxLayout(self)
        self.centralLayout.setContentsMargins(0, 1, 0, 0)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setAlignment(QtCore.Qt.AlignTop)

        # create header widget- wrapper for check button
        self.headerWidget = HeaderWidget(self)
        self.headerWidget.setFixedHeight(20)
        self.headerWidget.setLabel(self.label)
        self.headerWidget.mousePressEvent = self.hideDataLayout

        # add layouts
        self.setLayout(self.centralLayout)
        self.centralLayout.addWidget(self.headerWidget)

    def hideDataLayout(self, *args):
        if self.dataWidget.isVisible():
            self.dataWidget.setVisible(False)
            self.headerWidget.setArrow(False)
            cmds.optionVar(sv=(self.label, '0'))
        else:
            self.dataWidget.setVisible(True)
            cmds.optionVar(sv=(self.label, '1'))
            self.headerWidget.setArrow(True)

    # QMessageBox.information(self, 'New document',
    #    "New document is being created...", QMessageBox.Ok)

    def dataLayout(self, widget):
        self.dataWidget = widget
        if not cmds.optionVar(ex=self.label):
            cmds.optionVar(sv=(self.label, '1'))

        value = cmds.optionVar(q=self.label)
        if value == '1':
            self.dataWidget.setVisible(True)
            self.headerWidget.setArrow(True)
        else:
            self.dataWidget.setVisible(False)
            self.headerWidget.setArrow(False)
