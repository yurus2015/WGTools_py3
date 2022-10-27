import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import os
import re
import math

description = "Open Texture Editor"
buttonType = "opt"
beautyName = "Texture Editor"
iconName = "Texture Editor"


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
        <p style="color: #aaa;">Opens Maya native Texture Editor</p>
        '''

        self.label = QLabel(html)

        self.mainLayout.addWidget(self.label)

        return self.mainLayout

    def main(self):
        # path = str(os.path.dirname(__file__)) + "\\wg_textureEditor.mel"
        # fix =  path.replace("\\", "/")
        # mel.eval('source "'+fix+'"')

        mel.eval("TextureViewWindow;")
