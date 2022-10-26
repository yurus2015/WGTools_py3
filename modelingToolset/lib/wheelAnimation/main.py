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


description = "Adds a rotation animation to all wheels found in the scene"
buttonType = "opt"
beautyName = "WheelAnimation"
# iconType = "toggle"
iconName = "Animate wheels"


class ToolOptions(QWidget):

    def __init__(self, parent = None):

        super(ToolOptions, self).__init__(parent)

        self.setLayout(self.createUI())

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5,5,5,5)
        self.mainLayout.setSpacing(5) #layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.label  = QLabel("<b>Description:</b><p>Adds rotation animation to all wheels found in the<br> current scene</p>")

        self.mnl_layout = QHBoxLayout()
        self.mnl_title = QLabel("Speed (1.0 - normal speed):")
        self.mnl_editline = QLineEdit()
        self.mnl_editline.setStyleSheet("background-color: RGB(10,10,10);")
        if cmds.optionVar(exists = 'wg_mdltls_wheelAnimSpeed'):
            self.mnl_editline.setText(cmds.optionVar(q = 'wg_mdltls_wheelAnimSpeed'))
        else:
            self.mnl_editline.setText("0.2")
        self.mnl_editline.setInputMask("9.9")
        self.mnl_editline.returnPressed.connect(self.applySpeed)
        self.mnl_layout.addWidget(self.mnl_title)
        self.mnl_layout.addWidget(self.mnl_editline)


        self.prs_layout = QHBoxLayout()
        self.prs_label = QLabel("Presets")
        self.prs_button_01 = QPushButton("0.1")
        self.prs_button_01.clicked.connect(lambda x = "0.1": self.applySpeed(x))
        self.prs_button_05 = QPushButton("0.5")
        self.prs_button_05.clicked.connect(lambda x = "0.5": self.applySpeed(x))
        self.prs_button_10 = QPushButton("1.0")
        self.prs_button_10.clicked.connect(lambda x = "1.0": self.applySpeed(x))
        self.prs_button_15 = QPushButton("1.5")
        self.prs_button_15.clicked.connect(lambda x = "1.5": self.applySpeed(x))
        self.prs_button_20 = QPushButton("2.0")
        self.prs_button_20.clicked.connect(lambda x = "2.0": self.applySpeed(x))
        self.prs_layout.addWidget(self.prs_label)
        self.prs_layout.addWidget(self.prs_button_01)
        self.prs_layout.addWidget(self.prs_button_05)
        self.prs_layout.addWidget(self.prs_button_10)
        self.prs_layout.addWidget(self.prs_button_15)
        self.prs_layout.addWidget(self.prs_button_20)



        self.extr_layout = QHBoxLayout()
        self.extr_buttonA = QPushButton("Play")
        self.extr_buttonB = QPushButton("Stop")
        self.extr_layout.addWidget(self.extr_buttonA)
        self.extr_layout.addWidget(self.extr_buttonB)

        self.mainLayout.addWidget(self.label)
        self.mainLayout.addLayout(self.mnl_layout)
        self.mainLayout.addLayout(self.prs_layout)
        # self.mainLayout.addLayout(self.extr_layout)


        return self.mainLayout

    def applySpeed(self, speed = None):
        if not speed:
            speed = self.mnl_editline.text()
        else:
            self.mnl_editline.setText(speed)
        cmds.optionVar(sv=("wg_mdltls_wheelAnimSpeed", str(self.mnl_editline.text())))

        if cmds.play(q=1, state=1) == 1:
            self.main(update = 1)




    def getWheelsList(self):
        wheels = cmds.ls('w_*', 'wd_*', l= 1, type = 'transform')
        return wheels

    def main(self, update = 0):

        cmds.playbackOptions(ps =1)

        selection = cmds.ls(sl=1,l=1)
        wheels = cmds.ls(sl=1,l=1)
        if not wheels:
            wheels = self.getWheelsList()

        if not wheels: #if still no wheels
            cmds.inViewMessage(amg= '<hl>Wheels were not found. Please select wheels manually.</hl>' , pos = 'midCenter', fade = True, fot = 1000)
            return


        '''
        If there is some animation on tracks - stop playing animation and delete keyframes and restore timeline
        '''
        place2dTextures = cmds.ls(type="place2dTexture")
        if place2dTextures:
            if cmds.keyframe(place2dTextures, q=1, keyframeCount =1):
                cmds.play(state = 0)
                cmds.cutKey(place2dTextures, s=True)

                for ii in place2dTextures:
                    cmds.setAttr(ii + ".offsetV", 0)

                cmds.playbackOptions(e=1, ast = 1)
                cmds.playbackOptions(e=1, aet = 48)
                cmds.playbackOptions(min = 1, max = 24)
                cmds.currentTime(1)



        '''
        wheels transform animation
        '''
        #get speed value
        speed = float(self.mnl_editline.text())
        #calculate timing
        #24f = 1.0x = default speed
        timeS = cmds.playbackOptions(q=1, min=1)
        timeE = round(1.0/speed, 2) * 24

        if cmds.play(q=1, state=1) == 0:
            cmds.inViewMessage(amg= '<hl>Wheels are animated</hl>' , pos = 'topLeft', fade = True, fot = 1000)
            cmds.undoInfo(ock=1)
            cmds.setKeyframe( wheels, time = timeS, value = 0, at = "rotateX" )
            cmds.setKeyframe( wheels, time = timeE, value = -360, at = "rotateX" )
            cmds.playbackOptions(e=1, ast = timeS)
            cmds.playbackOptions(e=1, aet = timeE)
            cmds.playbackOptions(min = timeS, max = timeE)
            cmds.keyTangent(wheels, itt="linear", ott="linear")
            cmds.undoInfo(cck=1)
            cmds.play(forward=1)
            self.animationStatus = True


        elif cmds.play(q=1, state=1) == 1:
            cmds.inViewMessage(amg= '<hl>Wheels animation has been stopped</hl>' , pos = 'topLeft', fade = True, fot = 1000)
            cmds.play(state = 0)
            cmds.cutKey(wheels, s=True)
            for i in wheels:
                cmds.setAttr(i + ".rotateX", 0)

            cmds.playbackOptions(e=1, ast = 1)
            cmds.playbackOptions(e=1, aet = 48)
            cmds.playbackOptions(min = 1, max = 24)
            cmds.currentTime(1)
            self.animationStatus = False


        if update == 1:
            # cmds.inViewMessage(amg= '<hl>Wheels animation was updated</hl>' , pos = 'topLeft', fade = True, fot = 1000)
            cmds.undoInfo(ock=1)
            cmds.setKeyframe( wheels, time = timeS, value = 0, at = "rotateX" )
            cmds.setKeyframe( wheels, time = timeE, value = -360, at = "rotateX" )
            cmds.playbackOptions(e=1, ast = timeS)
            cmds.playbackOptions(e=1, aet = timeE)
            cmds.playbackOptions(min = timeS, max = timeE)
            cmds.keyTangent(wheels, itt="linear", ott="linear")
            cmds.undoInfo(cck=1)
            cmds.play(forward=1)


        if selection:
            cmds.select(selection)






