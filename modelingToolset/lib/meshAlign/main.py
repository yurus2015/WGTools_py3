import maya.cmds as cmds
import maya.mel as mel

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import os


description = "Select faces or edges on meshes"
buttonType = "opt"
beautyName = "Mesh Align"
iconName = "Mesh Align"

class ToolOptions(QWidget):

    def __init__(self, parent = None):

        super(ToolOptions, self).__init__(parent)


        self.setLayout(self.createUI())

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5,5,5,5)
        self.mainLayout.setSpacing(10) #layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        html = '''
        <b>Description:</b>
        <p style="color: #aaa;">Align meshes by vertices and edges</p>
        '''
        self.label  = QLabel(html)
        self.mainLayout.addWidget(self.label)

        '''ui content'''
        self.layout_tolerance = QHBoxLayout()
        self.layout_buttons = QHBoxLayout()

        self.tol_label = QLabel("Distance Tolerance: ")
        self.tol_edit = QLineEdit("0.1000")
        self.tol_edit.setInputMask("9.9999")

        if cmds.optionVar(exists = 'wg_mdltls_meshAlign_distTol'):
            self.tol_edit.setText(str(float(cmds.optionVar(q = 'wg_mdltls_meshAlign_distTol'))))

        self.but_vertAlign = QPushButton("Match Selected Verts")
        self.but_vertAlign.clicked.connect(self.alignVerts)
        self.but_edgeAlign = QPushButton("Match Border Edge")
        self.but_edgeAlign.clicked.connect(self.alignEdges)


        self.layout_tolerance.addWidget(self.tol_label)
        self.layout_tolerance.addWidget(self.tol_edit)
        self.layout_buttons.addWidget(self.but_vertAlign)
        self.layout_buttons.addWidget(self.but_edgeAlign)

        self.mainLayout.addLayout(self.layout_tolerance)
        self.mainLayout.addLayout(self.layout_buttons)


        return self.mainLayout

    def alignVerts(self):
        distTol = 0.0
        try:
            distTol = float(self.tol_edit.text())
        except:
            cmds.inViewMessage(amg= '<hl>Make sure you use correct Distance Tolerance number type</hl>' , pos = 'midCenter', fade = True, fot = 1000)
            return

        cmds.optionVar(sv=("wg_mdltls_meshAlign_distTol", self.tol_edit.text()))
        cmds.optionVar(sv=("wg_mdltls_meshAlign_lastTool", "Vertex"))


        dir = str(os.path.dirname(__file__))

        cmds.undoInfo(ock=1)

        scriptPath = str(os.path.dirname(__file__)) + "\\meshAlign.mel"
        scriptPathFix =  scriptPath.replace("\\", "/")
        mel.eval('source "'+scriptPathFix+'"')
        mel.eval('NinjaMesh_MatchVertex('+str(distTol)+')')

        cmds.undoInfo(cck=1)

    def alignEdges(self):
        distTol = 0.0
        try:
            distTol = float(self.tol_edit.text())
        except:
            cmds.inViewMessage(amg= '<hl>Make sure you use correct Distance Tolerance number type</hl>' , pos = 'midCenter', fade = True, fot = 1000)
            return

        cmds.optionVar(sv=("wg_mdltls_meshAlign_distTol", self.tol_edit.text()))
        cmds.optionVar(sv=("wg_mdltls_meshAlign_lastTool", "Edges"))

        dir = str(os.path.dirname(__file__))

        cmds.undoInfo(ock=1)

        scriptPath = str(os.path.dirname(__file__)) + "\\meshAlign.mel"
        scriptPathFix =  scriptPath.replace("\\", "/")
        mel.eval('source "'+scriptPathFix+'"')
        mel.eval('NinjaMesh_FixSeams('+str(distTol)+')')

        cmds.undoInfo(cck=1)



    # @classmethod
    def main(self):

        selection = cmds.ls(sl=1, l=1, fl=1)

        if not selection:
            cmds.inViewMessage(amg= '<hl>Please select components on two meshes (vertices or edges)</hl>' , pos = 'midCenter', fade = True, fot = 1000)
            return

        dist = 0.1
        lastTool = "Vertex"
        if cmds.optionVar(exists = 'wg_mdltls_meshAlign_distTol'):
            dist = float(cmds.optionVar(q = 'wg_mdltls_meshAlign_distTol'))

        if cmds.optionVar(exists = 'wg_mdltls_meshAlign_lastTool'):
            lastTool = str(cmds.optionVar(q = 'wg_mdltls_meshAlign_lastTool'))


        dir = str(os.path.dirname(__file__))

        cmds.undoInfo(ock=1)

        scriptPath = str(os.path.dirname(__file__)) + "\\meshAlign.mel"
        scriptPathFix =  scriptPath.replace("\\", "/")
        mel.eval('source "'+scriptPathFix+'"')

        if lastTool == "Vertex":
            print("Match Selected Verts")
            mel.eval('NinjaMesh_MatchVertex('+str(dist)+')')

        elif lastTool == "Edges":
            print("Match Border Edges")
            mel.eval('NinjaMesh_FixSeams('+str(dist)+')')

        cmds.undoInfo(cck=1)
