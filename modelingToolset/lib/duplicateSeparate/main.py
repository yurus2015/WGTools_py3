import maya.cmds as cmds
import maya.mel as mel

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import os

description = "Select object faces and click the tool"
buttonType = "opt"
beautyName = "Duplicate / Separate"
iconName = "Duplicate Separate"


class ToolOptions(QWidget):

    def __init__(self, parent=None):

        super(ToolOptions, self).__init__(parent)

        self.setLayout(self.createUI())

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(10)  # layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        html = '''
        <b>Description:</b>
        <p style="color: #aaa;">Duplicates and separates object faces.</p>
        '''
        self.label = QLabel(html)

        self.mainLayout.addWidget(self.label)

        return self.mainLayout

    # @classmethod
    def main(self):

        selection = cmds.ls(sl=1, l=1, fl=1)

        if not selection:
            cmds.inViewMessage(amg='<hl>Please select faces that should be duplicated and separated</hl>',
                               pos='midCenter', fade=True, fot=1000)
            return

        if ".f[" not in selection[0]:
            cmds.inViewMessage(amg='<hl>Please select faces that should be duplicated and separated</hl>',
                               pos='midCenter', fade=True, fot=1000)
            return

        dir = str(os.path.dirname(__file__))
        cmds.undoInfo(ock=1)
        scriptFile = open(dir + "/duplicateSeparate.mel", 'r')
        scriptIn = scriptFile.read()
        mel.eval(scriptIn)
        cmds.undoInfo(cck=1)
