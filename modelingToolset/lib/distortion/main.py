import maya.cmds as cmds
import math

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

description = "Vertex color paint distortion uv faces"
buttonType = "opt"
beautyName = "Distortion Paint"
iconName = "Calculate Diameter"


# DOCEDGES = ['4', '4-8', '8-12', '12-16', '16-20', '20-24', '24-28', '28-32', '32+']
# COLOR_RED = 'color:red'
# COLOR_WHITE = 'color:white'

class ToolOptions(QWidget):
    def __init__(self, parent=None):
        super(ToolOptions, self).__init__(parent)

        self.setLayout(self.createUI())

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.btnDist = QPushButton('Clear color')
        self.btnDist.setMinimumHeight(30)
        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.btnDist)
        self.setLayout(self.vbox)
        self.btnDist.clicked.connect(self.reset_color)

        '''main layout'''
        self.mainLayout.addLayout(self.vbox)

        return self.mainLayout

    def loadPlugin(self):
        if not cmds.pluginInfo('techartAPI2018', query=True, loaded=True):
            try:
                cmds.loadPlugin('techartAPI2018')
            except:
                print('Don`t load plugin')

    def reset_color(self):
        for i in cmds.ls(type='mesh'):
            try:
                cmds.polyColorSet(i, delete=True)
            except:
                pass

    # @classmethod
    def main(self):
        self.loadPlugin()
        cmds.stretchUV(clr=1)
        selected = cmds.filterExpand(sm=12)
        if selected:
            for sel in selected:
                cmds.setAttr(sel + '.displayColors', 1)
                cmds.setAttr(sel + '.displayColorChannel', "None", type="string")
        # Utils.add_texel_attribute(vertex_color_combobox, sel)
        # cmds.setAttr(sel + '.displayColors', 1)
        # setAttr -type "string" lod0|gun_01|gun_01_Shape.displayColorChannel "Ambient";
        cmds.inViewMessage(amg='<hl>Please open options to reset vertex color</hl>', pos='topCenter', fade=True,
                           fot=1000)
