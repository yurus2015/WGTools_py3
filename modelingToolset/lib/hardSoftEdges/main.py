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


description = "Fixes hard/soft edges after exporting from OBJ"
buttonType = "opt"
beautyName = "Hard/Soft Edges Fix"
iconName = "Hard/Soft Edges Fix"

class ToolOptions(QWidget):

    def __init__(self, parent = None):

        super(ToolOptions, self).__init__(parent)


        self.setLayout(self.createUI())

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5,5,5,5)
        self.mainLayout.setSpacing(5) #layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.label  = QLabel("<b>Description:</b><p>Fixes hard/soft edges after exporting from OBJ</p>")

        self.mainLayout.addWidget(self.label)

        return self.mainLayout

    # @classmethod
    def main(self):


        selection = cmds.ls(sl=1,l=1)

        if not selection:
            cmds.inViewMessage(amg= '<hl>Please select at least one polygonal mesh in the scene</hl>' , pos = 'topLeft', fade = True, fot = 1000)
            return

        for i in selection:
            cmds.select(i)
            duplicate = cmds.ls(cmds.duplicate(rr=1), l=1)[0]
            cmds.select(i)
            cmds.polySoftEdge(a=180, ch=1)
            cmds.transferAttributes(duplicate, i, transferPositions=0, transferNormals=1, transferUVs=0, transferColors=0, sampleSpace=1, sourceUvSpace="map2", targetUvSpace="map1", searchMethod=3, flipUVs=0, colorBorders=1)
            cmds.delete(all=1, ch=1)
            cmds.delete(duplicate)
            cmds.selectMode(object=1)

        cmds.select(selection, r=1)
        cmds.polyNormalPerVertex(ufn=1)
        mel.eval('colorSetEditCmd delete none;')


        cmds.inViewMessage(amg= '<hl style="color: #00FF00">Hard/soft edges were fixes successfully</hl>' , pos = 'topLeft', fade = True, fot = 1000)


