import maya.cmds as cmds
import maya.api.OpenMaya as om

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

description = "Two Vertex Distance Computing. Please use options to compute Distance"
buttonType = "opt"
beautyName = "Distance Computing"


class Utils(object):

    @classmethod
    def calculate_distance(cls):
        distance = ''
        vertex = cmds.filterExpand(sm=[31])
        if vertex:
            if len(vertex) == 2:
                v_1 = cmds.pointPosition(vertex[0])
                v_2 = cmds.pointPosition(vertex[1])
                distance = (om.MVector(v_1) - om.MVector(v_2)).length()
        return distance


class ToolOptions(QWidget):
    def __init__(self, parent=None):
        super(ToolOptions, self).__init__(parent)

        self.setLayout(self.createUI())

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.labelDiameter = QLabel('Vertex Distance: ')
        self.labelDiameter.setMinimumHeight(25)
        self.labelDiameter.setStyleSheet("color:white")
        self.btnDist = QPushButton('Get Distance')
        self.btnDist.setMinimumHeight(30)
        self.btnReset = QPushButton('Reset')
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.labelDiameter)
        self.vbox.addWidget(self.btnDist)
        self.setLayout(self.vbox)
        self.btnDist.clicked.connect(self.run_distance)

        '''main layout'''
        self.mainLayout.addLayout(self.vbox)

        return self.mainLayout

    def main(self):

        if cmds.headsUpDisplay('HUDdistance', q=1, ex=1):
            cmds.headsUpDisplay('HUDdistance', rem=True)

        else:
            nfb = cmds.headsUpDisplay(nfb=0);
            cmds.headsUpDisplay('HUDdistance', section=0,
                                block=nfb,
                                blockSize='small',
                                label='Vert Distance ',
                                labelFontSize='large',
                                dfs='large',
                                command=Utils.calculate_distance,
                                event='SelectionChanged')

        cmds.inViewMessage(amg='<hl>Please open options to compute circle diameter</hl>', pos='topCenter', fade=True,
                           fot=1000)

    def run_distance(self):
        distance = Utils.calculate_distance()
        if distance:
            self.labelDiameter.setText('Vertex Distance: ' + str(round(distance, 4)))
        else:
            self.labelDiameter.setText('Select only two vertices')
