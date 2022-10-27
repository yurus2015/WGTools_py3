import maya.cmds as cmds
import math

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

description = "Diameter Computing. Please use options to compute Diameter"
buttonType = "opt"
beautyName = "Diameter Computing"
iconName = "Calculate Diameter"

DOCEDGES = ['4', '4-8', '8-12', '12-16', '16-20', '20-24', '24-28', '28-32', '32+']
COLOR_RED = 'color:red'
COLOR_WHITE = 'color:white'


class Utils(object):
    @classmethod
    def loadPlugin(cls):
        if not cmds.pluginInfo('techartAPI', query=True, loaded=True):
            try:
                cmds.loadPlugin('techartAPI')
            except:
                print('Don`t load plugin')


class ToolOptions(QWidget):
    def __init__(self, parent=None):
        super(ToolOptions, self).__init__(parent)
        self.setLayout(self.createUI())

    def createUI(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.labelDiameter = QLabel('Diameter: ')
        self.labelDiameter.setMinimumHeight(25)
        self.labelDiameter.setStyleSheet("color:white")

        self.labelHaveEdges = QLabel('You have edges: ')
        self.labelHaveEdges.setMinimumHeight(25)
        self.labelHaveEdges.setStyleSheet("color:white")

        self.labelNeedEdges = QLabel('You need edges: ')
        self.labelNeedEdges.setMinimumHeight(25)
        self.labelNeedEdges.setStyleSheet("color:white")

        self.btnDist = QPushButton('Get Correct Value')
        self.btnDist.setMinimumHeight(30)
        self.btnReset = QPushButton('Reset')
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.labelDiameter)
        self.vbox.addWidget(self.labelHaveEdges)
        self.vbox.addWidget(self.labelNeedEdges)
        self.vbox.addWidget(self.btnDist)
        self.setLayout(self.vbox)
        self.btnDist.clicked.connect(self.calcDiameter)

        '''main layout'''
        self.mainLayout.addLayout(self.vbox)

        return self.mainLayout

    def setValueHUD(self, visible=True, diameter=None, segment=None, recommended=None):
        Utils.loadPlugin()
        border = ''
        result = []
        if cmds.filterExpand(sm=(32, 34)):
            border = cmds.polyListComponentConversion(ff=True, te=True, bo=True)
            if border:
                border = str(len(cmds.ls(border, fl=1)))
            else:
                border = str(len(cmds.ls(sl=1, fl=1)))
        value = cmds.roundSections()
        if not value:
            result = []
            return result
        else:
            values = value.split()
            result.append(str(border))
            result.extend(values)

            if diameter:
                return result[1]
            if segment:
                return result[0]
            if recommended:
                return result[2]

    def main(self):
        Utils.loadPlugin()
        if cmds.headsUpDisplay('HUDdiameter', q=1, ex=1):
            cmds.headsUpDisplay('HUDdiameter', rem=True)
        else:
            nfb = cmds.headsUpDisplay(nfb=0)
            cmds.headsUpDisplay('HUDdiameter', section=0,
                                block=nfb,
                                blockSize='small',
                                label='Diameter ',
                                labelFontSize='large',
                                dfs='large',
                                command=lambda: self.setValueHUD(diameter=True),
                                event='SelectionChanged')

        if cmds.headsUpDisplay('HUDsegments', q=1, ex=1):
            cmds.headsUpDisplay('HUDsegments', rem=True)
        else:
            nfb = cmds.headsUpDisplay(nfb=0)
            cmds.headsUpDisplay('HUDsegments', section=0,
                                block=nfb,
                                blockSize='small',
                                label='You have edges: ',
                                labelFontSize='large',
                                dfs='large',
                                command=lambda: self.setValueHUD(segment=True),
                                event='SelectionChanged')

        if cmds.headsUpDisplay('HUDrecommended', q=1, ex=1):
            cmds.headsUpDisplay('HUDrecommended', rem=True)
        else:
            nfb = cmds.headsUpDisplay(nfb=0)
            cmds.headsUpDisplay('HUDrecommended', section=0,
                                block=nfb,
                                blockSize='small',
                                label='You need edges: ',
                                labelFontSize='large',
                                dfs='large',
                                command=lambda: self.setValueHUD(recommended=True),
                                event='SelectionChanged')

        cmds.inViewMessage(amg='<hl>Please open options to compute circle diameter</hl>', pos='topCenter', fade=True,
                           fot=1000)

    @classmethod
    def dist(cls, sp, ep):
        rDist = math.sqrt((ep[0] - sp[0]) ** 2 + (ep[1] - sp[1]) ** 2 + (ep[2] - sp[2]) ** 2)
        return rDist

    def resultCompute(self):
        for doc in DOCEDGES:
            print('Need for')

    def calcDiameter(self):
        selection = cmds.ls(sl=1, l=1)
        self.finDist = 0.0
        pSelected = cmds.filterExpand(selectionMask=[34, 32])
        if pSelected:
            # pEdges = pSelected = cmds.polyListComponentConversion(pSelected, toEdge = True, border = True)
            # pEdges = cmds.ls(pEdges, fl=1)
            # pSelected = cmds.polyListComponentConversion(pSelected, toVertex=1)
            # pSelected = cmds.ls(pSelected, fl=1)
            # vPos = cmds.xform(pSelected[0], q=1, t=1, ws=1)

            # for vert in pSelected:
            # 	vPos2 = cmds.xform(vert, q=1, t=1, ws=1)
            # 	pDist = self.dist(vPos, vPos2)

            # 	if pDist > self.finDist:
            # 		self.finDist = pDist

            # self.finDist *= 100
            # self.finDist = round(self.finDist)
            # print 'Fin Distance ', self.finDist

            # docEdges = ""
            # if (self.finDist <= 2):
            # 	docEdges = "4"
            # 	docEdges_min = 0
            # 	docEdges_max = 4
            # elif(self.finDist <= 5):
            # 	docEdges = "4-8"
            # 	docEdges_min = 4
            # 	docEdges_max = 8
            # elif(self.finDist <= 10):
            # 	docEdges = "8-12"
            # 	docEdges_min = 8
            # 	docEdges_max = 12
            # elif(self.finDist <= 20):
            # 	docEdges = "12-16"
            # 	docEdges_min = 12
            # 	docEdges_max = 16
            # elif(self.finDist <= 40):
            # 	docEdges = "16-20"
            # 	docEdges_min = 16
            # 	docEdges_max = 20
            # elif(self.finDist <= 60):
            # 	docEdges = "20-24"
            # 	docEdges_min = 20
            # 	docEdges_max = 24
            # elif(self.finDist <= 80):
            # 	docEdges = "24-28"
            # 	docEdges_min = 24
            # 	docEdges_max = 28
            # elif(self.finDist <= 100):
            # 	docEdges = "28-32"
            # 	docEdges_min = 28
            # 	docEdges_max = 32
            # else:
            # 	docEdges = "32+"
            # 	docEdges_min = 32
            # 	docEdges_max = 1000

            diameter = self.setValueHUD(diameter=True)
            segment = self.setValueHUD(segment=True)
            recommended = self.setValueHUD(recommended=True)

            # self.labelDiameter.setText('Diameter: ' + str(self.finDist) + ' cm')
            # self.labelHaveEdges.setText('You have edges: ' + str(len(pEdges)))
            # self.labelNeedEdges.setText('You need edges: ' + docEdges)

            self.labelDiameter.setText('Diameter: ' + diameter)
            self.labelHaveEdges.setText('You have edges: ' + segment)
            self.labelNeedEdges.setText('You need edges: ' + recommended)

            try:
                min_value = recommended.split('-')[0]
                max_value = recommended.split('-')[1]
            except:
                min_value = max_value = recommended.split('+')[0]

            if '+' in recommended:
                max_value = 1000

            if int(segment) < int(min_value) or int(segment) > int(max_value):
                self.labelNeedEdges.setStyleSheet(COLOR_RED)
            else:
                self.labelNeedEdges.setStyleSheet(COLOR_WHITE)

        else:
            cmds.inViewMessage(amg='<hl>Please select edges or faces</hl>', pos='topCenter', fade=True, fot=3000)
