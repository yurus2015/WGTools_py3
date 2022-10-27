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

description = "Create lod groups hierarchy"
buttonType = "opt"
beautyName = "Create lods"


class ToolOptions(QWidget):

    def __init__(self, parent=None):

        super(ToolOptions, self).__init__(parent)

        self.setLayout(self.createUI())

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(5)  # layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.label = QLabel("<b>Description:</b><p>Create lod groups hierarchy</p>")

        self.mainLayout.addWidget(self.label)

        return self.mainLayout

    # @classmethod
    def main(self):

        selection = cmds.ls(sl=1, l=1)

        if not cmds.objExists("lod0"):
            cmds.inViewMessage(amg='<hl>Lod0 does not exists</hl>', pos='topLeft', fade=True, fot=1000)
            return

        cmds.select("lod0")
        lodGroup = cmds.listRelatives(p=1, type="lodGroup")

        if lodGroup:
            cmds.select(lodGroup[0])

            mel.eval('  performDeleteLod;\
                        reorder -front lod4;\
                        reorder -front lod3;\
                        reorder -front lod2;\
                        reorder -front lod1;\
                        reorder -front lod0;\
                        reorder -front persp;\
                        reorder -front top;\
                        reorder -front front;\
                        reorder -front side;')

            if cmds.objExists(selection[0]):
                cmds.select(selection)
        else:

            unitCoof = None
            if cmds.currentUnit(fullName=1, q=1, linear=1) == "meter":
                unitCoof = 1
            else:
                unitCoof = 100

            cmds.select(cl=1)
            if cmds.objExists("lod0"):
                cmds.select("lod0")
            if cmds.objExists("lod1"):
                cmds.select("lod1", add=1)
            if cmds.objExists("lod2"):
                cmds.select("lod2", add=1)
            if cmds.objExists("lod3"):
                cmds.select("lod3", add=1)
            if cmds.objExists("lod4"):
                cmds.select("lod4", add=1)

            nameOfLodGroup = mel.eval('performSetupLod;')
            if cmds.objExists(nameOfLodGroup[0] + ".threshold[0]"):
                cmds.setAttr(nameOfLodGroup[0] + ".threshold[0]", 13 * unitCoof)
            if cmds.objExists(nameOfLodGroup[0] + ".threshold[1]"):
                cmds.setAttr(nameOfLodGroup[0] + ".threshold[1]", 26 * unitCoof)
            if cmds.objExists(nameOfLodGroup[0] + ".threshold[2]"):
                cmds.setAttr(nameOfLodGroup[0] + ".threshold[2]", 39 * unitCoof)
            if cmds.objExists(nameOfLodGroup[0] + ".threshold[3]"):
                cmds.setAttr(nameOfLodGroup[0] + ".threshold[3]", 77 * unitCoof)

        cmds.inViewMessage(amg='<hl style="color: #00FF00">Selected mesh properties has been set up successfully</hl>',
                           pos='topLeft', fade=True, fot=1000)
