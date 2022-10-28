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

import modelingToolset.utils.scene as scene_u

description = "Select faces to map them into separated UV Shells"
buttonType = "opt"
beautyName = "Best-plane UV Mapping"
iconName = "UV Utils"


class ToolOptions(QWidget):

    def __init__(self, parent=None):

        super(ToolOptions, self).__init__(parent)

        self.setLayout(self.createUI())

        # source mel command
        realPath = str(os.path.dirname(__file__)) + "\\fixUV.mel"
        fix = realPath.replace("\\", "/")
        mel.eval('source "' + fix + '"')

    # self.loadUnfoldPlugin()

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(10)  # layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        html = '''
		<b>Description:</b>
		<p style="color: #aaa;">UV Utilities</p>
		'''
        self.label = QLabel(html)

        self.buttons_layout = QVBoxLayout()
        self.layout_A = QHBoxLayout()
        self.layout_B = QHBoxLayout()
        self.layout_C = QHBoxLayout()
        self.layout_D = QHBoxLayout()

        self.btn_FixBorder = QPushButton("Fix UV Border")
        self.btn_FixBorder.clicked.connect(self.bntA)
        self.btn_FixInternalUVs = QPushButton("Fix Internal UVs")
        self.btn_FixInternalUVs.clicked.connect(self.bntB)
        self.btn_QuickFixU = QPushButton("Quick Fix U")
        self.btn_QuickFixU.clicked.connect(self.bntC)
        self.btn_QuickFixV = QPushButton("Quick Fix V")
        self.btn_QuickFixV.clicked.connect(self.bntD)

        self.btn_moveLeft = QPushButton("<-- Move Left")
        self.btn_moveLeft.clicked.connect(lambda x="mleft": self.transformUVs(x))
        self.btn_moveRight = QPushButton("--> Move Right")
        self.btn_moveRight.clicked.connect(lambda x="mright": self.transformUVs(x))
        self.btn_squeeze = QPushButton("x.5 Squeeze")
        self.btn_squeeze.clicked.connect(lambda x="squeeze": self.transformUVs(x))
        self.btn_stretch = QPushButton("x2 Stretch")
        self.btn_stretch.clicked.connect(lambda x="stretch": self.transformUVs(x))

        self.buttons_layout.addLayout(self.layout_A)
        self.buttons_layout.addLayout(self.layout_B)
        self.buttons_layout.addLayout(self.layout_C)
        self.buttons_layout.addLayout(self.layout_D)

        self.layout_A.addWidget(self.btn_FixBorder)
        self.layout_A.addWidget(self.btn_FixInternalUVs)
        self.layout_B.addWidget(self.btn_QuickFixU)
        self.layout_B.addWidget(self.btn_QuickFixV)
        self.layout_C.addWidget(self.btn_moveLeft)
        self.layout_C.addWidget(self.btn_moveRight)
        self.layout_D.addWidget(self.btn_squeeze)
        self.layout_D.addWidget(self.btn_stretch)

        self.mainLayout.addWidget(self.label)
        self.mainLayout.addLayout(self.buttons_layout)

        return self.mainLayout

    def UnfoldSelected(self, UV=None):
        mel.eval("PolySelectConvert 4;")
        unfoldIterations = 1000
        if UV == "U":
            cmds.unfold(i=unfoldIterations, ss=1, gb=0, gmb=0, pub=0, ps=0, oa=2, us=0)
        elif UV == "V":
            cmds.unfold(i=unfoldIterations, ss=1, gb=0, gmb=0, pub=0, ps=0, oa=1, us=0)

    def SelectInteriorUVs(self):
        mel.eval("PolySelectConvert 4;")
        mel.eval("polySelectBorderShell 0;")
        selUV = cmds.ls(sl=1, fl=1, l=1)
        mel.eval("SelectUVBorder;")
        borderUV = cmds.ls(sl=1, fl=1, l=1)
        cmds.select(selUV)
        cmds.select(borderUV, d=1)

    def QuickFix(self):

        unfoldAccuracy = 1000
        selected = cmds.ls(sl=1, l=1, fl=1)
        meshName = selected[0].split(".")[0]

        totalUVs = cmds.polyEvaluate(meshName, uv=1)
        selection = cmds.ls(sl=1, l=1, fl=1)
        mel.eval("PolySelectConvert 4;")

        selUVs = cmds.ls(sl=1, l=1, fl=1)
        if len(selUVs) == totalUVs:
            cmds.select(selUVs[0], d=1)

        cmds.unfold(i=unfoldAccuracy, ss=0.001, gb=0, gmb=0, pub=0, ps=0, oa=0, us=0)
        cmds.select(selection)

    def QuickFixBorder(self):
        mel.eval("PolySelectConvert 4;")
        mel.eval("polySelectBorderShell 1;")
        self.QuickFix()

    def QuickFixInterior(self):
        self.SelectInteriorUVs()
        self.QuickFix()

    def selectShells(self):
        selection = cmds.ls(sl=1, l=1, fl=1)
        if not ".map[" in selection[0]:
            selection = cmds.ls(cmds.polyListComponentConversion(selection, tuv=1), l=1, fl=1)
        uvShells = scene_u.getUVShells(selection)
        uvShellsAll = []
        for i in uvShells:
            uvShellsAll.extend(i)
        cmds.select(uvShellsAll)

    def transformUVs(self, action=None):
        if not action: return
        scene_u.cleanup()
        self.selectShells()

        if action == "mleft":
            cmds.polyEditUV(u=-1, v=0)
        elif action == "mright":
            cmds.polyEditUV(u=1, v=0)
        elif action == "stretch":
            cmds.polyEditUV(pu=1, pv=1, su=1, sv=2)
        elif action == "squeeze":
            cmds.polyEditUV(pu=1, pv=1, su=1, sv=0.5)

        self.selectShells()

    def bntA(self):
        selection = cmds.ls(sl=1, l=1, fl=1)
        scene_u.cleanup()
        self.selectShells()
        try:
            # mel.eval('QuickFixBorder();')
            self.QuickFixBorder()
        except:
            cmds.inViewMessage(
                amg='<hl style="color: #fff">Something wrong happened. Try selecting the object other way.</hl>',
                pos='midCenter', fade=True, fot=1000)
        cmds.selectMode(co=1)
        cmds.selectType(puv=1, alc=0)
        cmds.select(selection)
        self.selectShells()

    def bntB(self):
        selection = cmds.ls(sl=1, l=1, fl=1)
        scene_u.cleanup()
        self.selectShells()
        try:
            # mel.eval('QuickFixInterior();')
            self.QuickFixInterior()
        except:
            cmds.inViewMessage(
                amg='<hl style="color: #fff">Something wrong happened. Try selecting the object other way.</hl>',
                pos='midCenter', fade=True, fot=1000)
        cmds.selectMode(co=1)
        cmds.selectType(puv=1, alc=0)
        cmds.select(selection)
        self.selectShells()

    def bntC(self):
        selection = cmds.ls(sl=1, l=1, fl=1)
        scene_u.cleanup()
        self.selectShells()
        try:
            # mel.eval('UnfoldSelected U;')
            self.UnfoldSelected("U")
        except:
            cmds.inViewMessage(
                amg='<hl style="color: #fff">Something wrong happened. Try selecting the object other way.</hl>',
                pos='midCenter', fade=True, fot=1000)
        cmds.selectMode(co=1)
        cmds.selectType(puv=1, alc=0)
        cmds.select(selection)
        self.selectShells()

    def bntD(self):
        selection = cmds.ls(sl=1, l=1, fl=1)
        scene_u.cleanup()
        self.selectShells()
        try:
            # mel.eval('UnfoldSelected V;')
            self.UnfoldSelected("V")
        except:
            cmds.inViewMessage(
                amg='<hl style="color: #fff">Something wrong happened. Try selecting the object other way.</hl>',
                pos='midCenter', fade=True, fot=1000)
        cmds.selectMode(co=1)
        cmds.selectType(puv=1, alc=0)
        cmds.select(selection)
        self.selectShells()

    def main(self):

        cmds.inViewMessage(amg='<hl>Please click right mouse button to choose an option</hl>', pos='midCenter',
                           fade=True, fot=1000)
