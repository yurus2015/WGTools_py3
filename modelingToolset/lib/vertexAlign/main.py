import maya.cmds as cmds
import maya.mel as mel

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import os

description = "Select vertices at the ends first. Then select other vertices. \nClick Command Button."


class ToolOptions(QWidget):
    def __init__(self, parent=None):
        super(ToolOptions, self).__init__(parent)
        self.setLayout(self.createUI())

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(5)  # layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)

        self.label = QLabel(description)
        self.mainLayout.addWidget(self.label)

        return self.mainLayout

    # @classmethod
    def main(self):

        selection = cmds.ls(sl=1, l=1, fl=1)

        if not selection:
            print('Please select vertices that should be aligned')
            cmds.inViewMessage(amg='<hl>Please select vertices that should be alighted</hl>', pos='topLeft', fade=True,
                               fot=1000)
            return

        if ".vtx[" not in selection[0]:
            cmds.inViewMessage(amg='<hl>Please select vertices that should be alighted</hl>', pos='topLeft', fade=True,
                               fot=1000)
            return

        dir = str(os.path.dirname(__file__))
        cmds.undoInfo(ock=1)
        scriptFile = open(dir + "/verticesInLine.mel", 'r')
        scriptIn = scriptFile.read()
        mel.eval(scriptIn)
        cmds.undoInfo(cck=1)
