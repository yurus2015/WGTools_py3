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

import modelingToolset2019.utils.scene as scene_u
import modelingToolset2019.utils.std as std_u

description = "Select faces to map them into separated UV Shells"
buttonType = "opt"
beautyName = "Best-plane UV Mapping"
iconName = "Map Selected"


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
        <p style="color: #aaa;">Creates a UV map based on selection</p>
        '''
        self.label = QLabel(html)

        '''texel value'''
        self.texel_layout = QHBoxLayout()
        self.texel_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.texel_layout.setSpacing(10)
        self.texel_layout.setContentsMargins(0, 0, 0, 0)

        self.texelValue = QLineEdit()
        self.texelValue.setStyleSheet("background-color: #111;")
        self.texelValue.setText("500")
        if cmds.optionVar(exists='wg_mdltls_uvautmp_pixelratio'):
            self.texelValue.setText(str(int(cmds.optionVar(q='wg_mdltls_uvautmp_pixelratio'))))

        self.texelvalueLabel = QLabel("Pixel Ratio")
        self.texelvalueLabel.setMinimumWidth(100)
        self.texelvalueLabel.setMaximumWidth(100)

        self.texel_layout.addWidget(self.texelvalueLabel)
        self.texel_layout.addWidget(self.texelValue)

        '''texture width'''
        self.texture_layout = QVBoxLayout()
        self.texture_layout.setAlignment(QtCore.Qt.AlignTop)
        self.texture_layout.setSpacing(2)
        self.texture_layout.setContentsMargins(0, 0, 0, 0)

        self.texture_layout_A = QHBoxLayout()
        self.texture_layout_A.setAlignment(QtCore.Qt.AlignLeft)
        self.texture_layout_A.setSpacing(10)
        self.texture_layout_A.setContentsMargins(0, 0, 0, 0)
        self.texture_layout_B = QHBoxLayout()
        self.texture_layout_B.setAlignment(QtCore.Qt.AlignLeft)
        self.texture_layout_B.setSpacing(1)
        self.texture_layout_B.setContentsMargins(0, 0, 0, 0)

        self.A_label = QLabel("Texture Size: ")
        self.A_label.setMinimumWidth(100)
        self.A_label.setMaximumWidth(100)
        self.A_edit = QLineEdit()
        self.A_edit.setStyleSheet("background-color: #111;")
        self.A_edit.setText("2048")
        if cmds.optionVar(exists='wg_mdltls_uvautmp_textrwidth'):
            self.A_edit.setText(str(int(cmds.optionVar(q='wg_mdltls_uvautmp_textrwidth'))))

        self.pres_label = QLabel("Presets")
        self.pres_label.setMinimumWidth(110)
        self.pres_label.setMaximumWidth(110)
        self.pres_512 = QPushButton("512")
        self.pres_512.clicked.connect(lambda x=512: self.setTextureSize(x))
        self.pres_1024 = QPushButton("1024")
        self.pres_1024.clicked.connect(lambda x=1024: self.setTextureSize(x))
        self.pres_2048 = QPushButton("2048")
        self.pres_2048.clicked.connect(lambda x=2048: self.setTextureSize(x))
        self.pres_4096 = QPushButton("4096")
        self.pres_4096.clicked.connect(lambda x=4096: self.setTextureSize(x))
        self.pres_8192 = QPushButton("8192")
        self.pres_8192.clicked.connect(lambda x=8192: self.setTextureSize(x))

        self.texture_layout_A.addWidget(self.A_label)
        self.texture_layout_A.addWidget(self.A_edit)
        self.texture_layout_B.addWidget(self.pres_label)
        self.texture_layout_B.addWidget(self.pres_512)
        self.texture_layout_B.addWidget(self.pres_1024)
        self.texture_layout_B.addWidget(self.pres_2048)
        self.texture_layout_B.addWidget(self.pres_4096)
        self.texture_layout_B.addWidget(self.pres_8192)
        self.texture_layout.addLayout(self.texture_layout_A)
        self.texture_layout.addLayout(self.texture_layout_B)

        '''buttons'''
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(2)
        self.buttons_layout.setContentsMargins(0, 30, 0, 0)
        self.btn_run = QPushButton("Save and Run")
        self.btn_run.clicked.connect(self.runAction)
        self.btn_saveandrun = QPushButton("Save and Run")
        self.btn_saveandrun.clicked.connect(self.saveRunAction)
        self.btn_save = QPushButton("Save without Running")
        self.btn_save.clicked.connect(self.save)
        self.buttons_layout.addWidget(self.btn_run)
        self.buttons_layout.addWidget(self.btn_save)

        self.mainLayout.addWidget(self.label)
        self.mainLayout.addLayout(self.texel_layout)
        self.mainLayout.addLayout(self.texture_layout)
        self.mainLayout.addLayout(self.buttons_layout)

        return self.mainLayout

    def setTextureSize(self, size=None):
        if not size: return

        try:
            size = int(size)
        except:
            cmds.inViewMessage(amg='<hl>Please use correct size value</hl>', pos='midCenter', fade=True, fot=1000)
            return

        self.A_edit.setText(str(size))

        self.save()

    def saveRunAction(self):
        cmds.optionVar(sv=("wg_mdltls_uvautmp_pixelratio", self.texelValue.text()))
        cmds.optionVar(sv=("wg_mdltls_uvautmp_textrwidth", self.A_edit.text()))
        self.runAction()

    def save(self):
        cmds.optionVar(sv=("wg_mdltls_uvautmp_pixelratio", self.texelValue.text()))
        cmds.optionVar(sv=("wg_mdltls_uvautmp_textrwidth", self.A_edit.text()))

    def runExternalMel(self, selection):

        if not selection: return

        pixelRatio = 500
        try:
            pixelRatio = int(self.texelValue.text())
        except:
            cmds.inViewMessage(amg='<hl>Can`t read Pixel Ratio value</hl>', pos='midCenter', fade=True, fot=1000)
            return

        textureWidth = 2048
        try:
            textureWidth = int(self.A_edit.text())
        except:
            cmds.inViewMessage(amg='<hl>Can`t read Texture Size value</hl>', pos='midCenter', fade=True, fot=1000)
            return

        print("Pixel ratio: " + str(float(pixelRatio)) + ", Texture Size: " + str(float(textureWidth)))

        realPath = str(os.path.dirname(__file__)) + "\\map.mel"
        fix = realPath.replace("\\", "/")
        mel.eval('source "' + fix + '"')
        mel.eval('Map(' + str(float(pixelRatio)) + ',' + str(float(textureWidth)) + ')')

    def applyAutoRotate(self):
        selection = cmds.ls(sl=1, l=1, fl=1)
        if not selection: return

        denisevichPath = str(os.path.dirname(__file__)) + "\\autoRotate.mel"
        fix = denisevichPath.replace("\\", "/")
        mel.eval('source "' + fix + '"')
        mel.eval('rotateUvShells()')

    def findLongestEdgeUVsInShell(self, uvShell):
        # conver it to edges
        selectedEdgeList = cmds.ls(cmds.polyListComponentConversion(uvShell, fuv=1, te=1), l=1, fl=1)
        cmds.select(selectedEdgeList)

        highestLength = 0
        uvCouple = []

        for i in selectedEdgeList:

            edgeUVs = cmds.ls(cmds.polyListComponentConversion(i, fe=1, tuv=1), l=1, fl=1)
            ourTwoUVs = std_u.matchLists(edgeUVs, uvShell)

            if len(ourTwoUVs) == 2:
                uvA = cmds.polyEditUV(ourTwoUVs[0], q=1, u=1, v=1)
                uvA[0] = float(round(uvA[0], 3))
                uvA[1] = float(round(uvA[1], 3))
                uvB = cmds.polyEditUV(ourTwoUVs[1], q=1, u=1, v=1)
                uvB[0] = float(round(uvB[0], 3))
                uvB[1] = float(round(uvB[1], 3))

                length = math.sqrt((uvB[0] - uvA[0]) * (uvB[0] - uvA[0]) + (uvB[1] - uvA[1]) * (uvB[1] - uvA[1]))
                if length > highestLength:
                    highestLength = length
                    uvCouple = ourTwoUVs

        if len(uvCouple) == 2:
            return [uvCouple[0], uvCouple[1]]
        else:
            return [uvShell[0], uvShell[1]]

    def main(self):
        scene_u.cleanup()

        if cmds.optionVar(exists='wg_mdltls_uvautmp_textrwidth'):
            self.A_edit.setText(str(int(cmds.optionVar(q='wg_mdltls_uvautmp_textrwidth'))))

        if cmds.optionVar(exists='wg_mdltls_uvautmp_pixelratio'):
            self.texelValue.setText(str(int(cmds.optionVar(q='wg_mdltls_uvautmp_pixelratio'))))

        # get the selection
        selection = cmds.ls(sl=1, l=1, fl=1)

        '''map and scale'''

        # nothing is selected - cancel operation
        if not selection:
            cmds.inViewMessage(amg='<hl>Please select some faces to make a map</hl>', pos='midCenter', fade=True,
                               fot=1000)
            return

        self.runExternalMel(selection)

        cmds.select(selection)
        uvs = cmds.ls(cmds.polyListComponentConversion(selection, tuv=1), fl=1, l=1)

        cmds.select(uvs)

        '''auto rotate'''
        uvShells = scene_u.getUVShells(uvs)

        for i in uvShells:
            twoUVs = self.findLongestEdgeUVsInShell(i)
            if twoUVs:
                cmds.select(twoUVs)
                self.applyAutoRotate()

        cmds.select(uvs)
