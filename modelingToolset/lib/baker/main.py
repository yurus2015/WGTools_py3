import maya.cmds as cmds
import maya.mel as mel
import os

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

description = "Bake normal"
buttonType = "opt"
beautyName = "Baker"
iconName = "Baker"


class ToolOptions(QWidget):

    def __init__(self, parent=None):
        super(ToolOptions, self).__init__(parent)

        self.setLayout(self.createUI())

    def createUI(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(5)  # layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.label = QLabel("<b>Description:</b><p>Bake normal textures. <br></p>")

        self.mainLayout.addWidget(self.label)

        return self.mainLayout

    def main(self):
        baker_mel = str(os.path.dirname(__file__)) + "\\bake_texture_ui.mel"
        fix = baker_mel.replace("\\", "/")
        mel.eval('source "' + fix + '"')
        mel.eval('bake_texture_ui')
