import maya.cmds as cmds
import maya.api.OpenMaya as om

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

description = "Two Edge Center Computing. Please use options to compute Distance"
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

    def count_edges(self):
        edges = cmds.filterExpand(sm=[32])
        if edges and len(edges) == 2:
            return True
        else:
            return False

    @classmethod
    def culculate_center(cls):
        if cls.count_edges():

            mesh_selected = om.MSelectionList()
            om.MGlobal.getActiveSelectionList(mesh_selected)
            mesh_iter = om.MItSelectionList(mesh_selected)
            while not mesh_iter.isDone():
                mesh_dag_path, mesh_component = mesh_iter.getComponent()
                mesh = om.MFnMesh(mesh_dag_path)
                if mesh_component is not None:
                    edge_iter = om.MItMeshEdge(mesh_dag_path, mesh_component)

                next(mesh_iter)


class ToolOptions(QWidget):
    def __init__(self, parent=None):
        super(ToolOptions, self).__init__(parent)

        self.setLayout(self.createUI())

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.labelDiameter = QLabel('Edge Distance: ')
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

        if cmds.headsUpDisplay('HUDdistance_e', q=1, ex=1):
            cmds.headsUpDisplay('HUDdistance_e', rem=True)

        else:
            nfb = cmds.headsUpDisplay(nfb=0);
            cmds.headsUpDisplay('HUDdistance_e', section=0,
                                block=nfb,
                                blockSize='small',
                                label='Edge Distance ',
                                labelFontSize='large',
                                dfs='large',
                                command=self.distance,
                                event='SelectionChanged')

        cmds.inViewMessage(amg='<hl>Please open options to compute edge distance</hl>', pos='topCenter', fade=True,
                           fot=1000)

    def count_edges(self):
        edges = cmds.filterExpand(sm=[32])
        if edges and len(edges) == 2:
            return True
        else:
            return False

    def distance(self):
        distance = ''
        if self.count_edges():
            print('edges')
            # distance = None
            selection = om.MGlobal.getActiveSelectionList()
            polygonComponentIter = om.MItSelectionList(selection, om.MFn.kMeshEdgeComponent)
            if not selection.isEmpty():
                dag, s_edge = polygonComponentIter.getComponent()
                mainList = []
                edge_itr = om.MItMeshEdge(dag, s_edge)
                # print edge_itr.length()
                while not edge_itr.isDone():
                    print('__')
                    mainList.append(edge_itr.center())
                    next(edge_itr)
                distance = (om.MVector(mainList[0]) - om.MVector(mainList[1])).length()
                if cmds.currentUnit(query=True, linear=True) == 'm':
                    distance = distance / 100.0
        return distance

    def run_distance(self):
        distance = self.distance()
        if distance:
            self.labelDiameter.setText('Edge Distance: ' + str(round(distance, 4)))
        else:
            self.labelDiameter.setText('Select only two edges')
