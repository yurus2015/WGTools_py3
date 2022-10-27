import maya.cmds as cmds
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

description = "Select one or more polygonal objects to apply XRay. Press the button again to exit XRay mode"
buttonType = "opt"
beautyName = "XRay"
iconName = "XRay"


class ToolOptions(QWidget):

    def __init__(self, parent=None):

        super(ToolOptions, self).__init__(parent)

        self.setLayout(self.createUI())

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(5)  # layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.label = QLabel(
            "<b>Description:</b><p>Select one or more polygonal objects to apply XRay. <br>Press the button again to exit XRay mode</p>")

        self.mainLayout.addWidget(self.label)

        return self.mainLayout

    # @classmethod
    def main(self):
        cmds.undoInfo(ock=1)
        selection = cmds.ls(sl=1, dag=1, ap=1, typ="surfaceShape")

        if not selection:
            cmds.inViewMessage(amg='<hl>Please select one or more polygonal objects</hl>', pos='topLeft', fade=True,
                               fot=1000)
            return

        for i in selection:
            temp = cmds.displaySurface(i, q=1, xRay=1)
            value = temp[0]
            if value == 1:
                cmds.displaySurface(i, xRay=0)
            else:
                cmds.displaySurface(i, xRay=1)

        cmds.undoInfo(cck=1)
