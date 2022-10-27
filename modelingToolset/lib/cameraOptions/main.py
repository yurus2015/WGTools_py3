import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaRender as OpenMayaRender

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import os

description = "Setups default cameras parameters"
buttonType = "opt"
beautyName = "Default cameras parameters"


class ToolOptions(QWidget):

    def __init__(self, parent=None):
        super(ToolOptions, self).__init__(parent)

        self.setLayout(self.createUI())

    def createUI(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(5)  # layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.label = QLabel("<b>Description:</b><p>Setups default cameras parameters</p>")

        self.mainLayout.addWidget(self.label)

        return self.mainLayout

    # @classmethod
    def main(self):
        cmds.currentUnit(l="m")
        cmds.setAttr("persp.translateX", 24)
        cmds.setAttr("persp.translateY", 18)
        cmds.setAttr("persp.translateZ", 24)
        cmds.setAttr("persp.rotateX", -27.938)
        cmds.setAttr("persp.rotateY", 45)
        cmds.setAttr("persp.rotateZ", 0)
        cmds.setAttr("perspShape.tumblePivotX", 0)
        cmds.setAttr("perspShape.tumblePivotY", 0)
        cmds.setAttr("perspShape.tumblePivotZ", 0)
        cmds.grid(sp=10, d=10, s=10, da=1, dgl=1, ddl=1, dpl=0, dol=0, dab=1)
        cmds.setAttr("perspShape.nearClipPlane", 0.05)
        cmds.setAttr("perspShape.farClipPlane", 10000)
        cmds.setAttr("topShape.nearClipPlane", 0.05)
        cmds.setAttr("topShape.farClipPlane", 10000)
        cmds.setAttr("frontShape.nearClipPlane", 0.05)
        cmds.setAttr("frontShape.farClipPlane", 10000)
        cmds.setAttr("sideShape.nearClipPlane", 0.05)
        cmds.setAttr("sideShape.farClipPlane", 10000)
        cmds.select(cl=1)
        mel.eval('fitPanel -selected;')
        cmds.FrameAll()

        cmds.inViewMessage(amg='<hl style="color: #00FF00">All cameras has been set up successfully</hl>',
                           pos='topLeft', fade=True, fot=1000)
