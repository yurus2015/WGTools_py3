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

import modelingToolset2019.utils.scene as scene_u

description = "Application options"
buttonType = "opt"
beautyName = "Application Options"
iconName = "App Options"


class ToolOptions(QWidget):

    def __init__(self, parent=None):

        super(ToolOptions, self).__init__(parent)

        self.setLayout(self.createUI())
        self.value = 0

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(5)  # layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.label = QLabel("""
                                    <b>Description:</b>
                                    <p>Here you can change application settings</p>
                                    """)

        self.checkbox_autorun = QCheckBox("Auto Run")
        self.checkbox_autorun.stateChanged.connect(self.saveState)

        if cmds.optionVar(exists='wg_mdltls_appOptions_autorun'):
            if cmds.optionVar(q='wg_mdltls_appOptions_autorun') == 1:
                self.checkbox_autorun.setChecked(1)
            else:
                self.checkbox_autorun.setChecked(0)

        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.checkbox_autorun)

        return self.mainLayout

    def saveState(self):
        if self.checkbox_autorun.isChecked():
            # print "check box checked"
            cmds.optionVar(iv=("wg_mdltls_appOptions_autorun", 1))
            print("autorun = On saved")
        else:
            # print "check box unchecked"
            cmds.optionVar(iv=("wg_mdltls_appOptions_autorun", 0))
            print("autorun = Off saved")

    # @classmethod
    def main(self):

        cmds.inViewMessage(
            amg='<hl>Please open the tool options to change application settings(Right Button Clik)</hl>',
            pos='midCenter', fade=True, fot=1000)
