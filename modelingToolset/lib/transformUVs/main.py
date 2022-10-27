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

description = "Move or stretch UVs"
buttonType = "opt"
beautyName = "Transform UVs"
iconName = "Transform UVs"


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
        <p style="color: #aaa;">Transforms and deforms UV shells</p>
        '''

        self.label = QLabel(html)

        self.btn_moveLeft = QPushButton("<-- Move Left")
        self.btn_moveLeft.clicked.connect(lambda x="mleft": self.transformUVs(x))

        self.btn_moveRight = QPushButton("--> Move Right")
        self.btn_moveRight.clicked.connect(lambda x="mright": self.transformUVs(x))

        self.btn_squeeze = QPushButton("x.5 Squeeze")
        self.btn_squeeze.clicked.connect(lambda x="squeeze": self.transformUVs(x))

        self.btn_stretch = QPushButton("x2 Stretch")
        self.btn_stretch.clicked.connect(lambda x="stretch": self.transformUVs(x))

        self.move_layout = QHBoxLayout()
        self.move_layout.addWidget(self.btn_moveLeft)
        self.move_layout.addWidget(self.btn_moveRight)

        self.deform_layout = QHBoxLayout()
        self.deform_layout.addWidget(self.btn_squeeze)
        self.deform_layout.addWidget(self.btn_stretch)

        self.mainLayout.addWidget(self.label)
        self.mainLayout.addLayout(self.move_layout)
        self.mainLayout.addLayout(self.deform_layout)

        return self.mainLayout

    def transformUVs(self, action=None):
        scene_u.cleanup()

        if not action: return

        if action == "mleft":
            cmds.polyEditUV(u=-1, v=0)
        elif action == "mright":
            cmds.polyEditUV(u=1, v=0)
        elif action == "stretch":
            cmds.polyEditUV(pu=1, pv=1, su=1, sv=2)
        elif action == "squeeze":
            cmds.polyEditUV(pu=1, pv=1, su=1, sv=0.5)

    def main(self):

        cmds.inViewMessage(amg='<hl>Please open options to continue</hl>', pos='midCenter', fade=True, fot=1000)
