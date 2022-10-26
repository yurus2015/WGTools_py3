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


description = "Select faces to map them into separated UV Shells"
buttonType = "opt"
beautyName = "UV Straightening"
iconName = "Straighten UV"


class ToolOptions(QWidget):

    def __init__(self, parent = None):

        super(ToolOptions, self).__init__(parent)

        self.setLayout(self.createUI())

        #source mel command
        realPath = str(os.path.dirname(__file__)) + "\\fixUV.mel"
        fix =  realPath.replace("\\", "/")
        mel.eval('source "'+fix+'"')

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5,5,5,5)
        self.mainLayout.setSpacing(10) #layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        html = '''
        <b>Description:</b>
        <p style="color: #aaa;">Straightening out a UV shell</p>
        '''
        self.label  = QLabel(html)

        self.h_layout_options = QHBoxLayout()
        self.h_layout_buttons_A = QHBoxLayout()
        self.h_layout_buttons_B = QHBoxLayout()

        '''angle tolerance'''
        self.slider_label = QLabel("Angle Tolerance")

        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 45)
        self.slider.setSingleStep(1)
        self.slider.setSliderPosition(30)
        self.slider.setStyleSheet("border: 0px solid rbg(10,10,10); background-color: #222;")
        self.slider.valueChanged.connect(self.test)

        self.slider_value = QLabel(str(self.slider.value()))

        self.h_layout_options.addWidget(self.slider_label)
        self.h_layout_options.addWidget(self.slider)
        self.h_layout_options.addWidget(self.slider_value)

        '''buttons'''
        self.button_A_01 = QPushButton("Straighten Horizontal/Vertical")
        self.button_A_01.clicked.connect(lambda x = "Both": self.runStraighten(x))
        self.button_B_01 = QPushButton("Straighten Horizontal")
        self.button_B_01.clicked.connect(lambda x = "Horizontal": self.runStraighten(x))
        self.button_B_02 = QPushButton("Straighten Vertical")
        self.button_B_02.clicked.connect(lambda x = "Vertical": self.runStraighten(x))
        self.h_layout_buttons_A.addWidget(self.button_A_01)
        self.h_layout_buttons_B.addWidget(self.button_B_01)
        self.h_layout_buttons_B.addWidget(self.button_B_02)


        self.mainLayout.addWidget(self.label)
        self.mainLayout.addLayout(self.h_layout_options)
        self.mainLayout.addLayout(self.h_layout_buttons_A)
        self.mainLayout.addLayout(self.h_layout_buttons_B)

        return self.mainLayout

    def test(self):
        # print self.slider.value()
        self.slider_value.setText(str(self.slider.value()))


    def runStraighten(self, x = None):
        scene_u.cleanup()

        cmds.undoInfo(ock=1)
        selection = cmds.ls(sl=1, l=1, fl=1)

        if not selection or ".map[" not in selection[0]:
            cmds.inViewMessage(amg= '<hl>Please select a UV point or an entire uv shell</hl>' , pos = 'midCenter', fade = True, fot = 1000)
            return

        UVs = cmds.ls(cmds.polyListComponentConversion(selection, tuv=1), l=1, fl=1)
        # uvShells = scene_u.getUVShells(UVs)

        # cmds.select(d=1)
        # for i in uvShells:
        #     cmds.select(i, add=1)

        path = str(os.path.dirname(__file__)) + "\\straightenUV.mel"
        fix =  path.replace("\\", "/")
        mel.eval('source "'+fix+'"')
        print(str(self.slider.value()))
        mel.eval('UV_StraightenUVSelection '+ x + ' '  + str(self.slider.value()))

        # cmds.select(d=1)
        # for i in uvShells:
        #     cmds.select(i, add=1)
        #
        cmds.select(selection)

        cmds.selectMode(co=1)
        cmds.selectType(puv=1, alc=0)

        cmds.undoInfo(cck=1)

    def main(self):

        cmds.inViewMessage(amg= '<hl>Please click right mouse button to choose an option</hl>' , pos = 'midCenter', fade = True, fot = 1000)

