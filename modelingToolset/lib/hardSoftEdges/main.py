import maya.cmds as cmds
import maya.mel as mel
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *


class ToolOptions(QWidget):

    def __init__(self, parent=None):

        super(ToolOptions, self).__init__(parent)

        self.setLayout(self.createUI())

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(5)  # layout
        self.mainLayout.setAlignment(Qt.AlignTop)

        self.label = QLabel("<b>Description:</b><p>Fixes hard/soft edges after exporting from OBJ</p>")

        self.btn_selected = QPushButton('On selected')
        self.btn_selected.clicked.connect(self.restore_selected)

        self.btn_all = QPushButton('On all')
        self.btn_all.clicked.connect(self.restore_all)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.btn_selected)
        self.button_layout.addWidget(self.btn_all)

        self.mainLayout.addWidget(self.label)
        self.mainLayout.addLayout(self.button_layout)

        return self.mainLayout

    def main2(self):

        selection = cmds.ls(sl=1, l=1)

        if not selection:
            cmds.inViewMessage(amg='<hl>Please select at least one polygonal mesh in the scene</hl>', pos='topLeft',
                               fade=True, fot=1000)
            return

        for i in selection:
            cmds.select(i)
            duplicate = cmds.ls(cmds.duplicate(rr=1), l=1)[0]
            cmds.select(i)
            cmds.polySoftEdge(a=180, ch=1)
            cmds.transferAttributes(duplicate, i, transferPositions=0, transferNormals=1, transferUVs=0,
                                    transferColors=0, sampleSpace=1, sourceUvSpace="map2", targetUvSpace="map1",
                                    searchMethod=3, flipUVs=0, colorBorders=1)
            cmds.delete(all=1, ch=1)
            cmds.delete(duplicate)
            cmds.selectMode(object=1)

        cmds.select(selection, r=1)
        cmds.polyNormalPerVertex(ufn=1)
        mel.eval('colorSetEditCmd delete none;')

        cmds.inViewMessage(amg='<hl style="color: #00FF00">Hard/soft edges were fixes successfully</hl>', pos='topLeft',
                           fade=True, fot=1000)

    @staticmethod
    def list_remove_duplicate(source_list):
        return list(set(source_list))

    @staticmethod
    def list_subtract(big_list, small_list):
        return list(set(big_list) - set(small_list))

    def soft_hard_display_restore(self, mesh):
        # long path mesh or needs mesh long path yet
        mesh_long_name = cmds.ls(mesh, l=True)[0]
        mesh_shape_list = cmds.filterExpand(mesh_long_name, sm=12, fp=True)
        smooth_node = cmds.polySoftEdge(mesh_shape_list[0], a=180, ch=True)[0]
        connected_nodes = cmds.listConnections(smooth_node, sh=1, s=1)
        connected_nodes = cmds.ls(connected_nodes, l=True)

        # remove duplicate
        connected_nodes = self.list_remove_duplicate(connected_nodes)

        # remove base shape - get original
        original_nodes = self.list_subtract(connected_nodes, mesh_shape_list)

        cmds.transferAttributes(original_nodes[0], mesh_shape_list[0], transferNormals=1)
        cmds.delete(mesh_long_name, ch=1)
        cmds.select(d=True)

    def restore_selected(self):
        selection = cmds.ls(sl=True)
        shapes = cmds.filterExpand(selection, sm=12, fp=True)
        for s in shapes:
            self.soft_hard_display_restore(s)
        cmds.select(selection)

    def restore_all(self):
        all_meshes = cmds.ls(typ='mesh')
        for m in all_meshes:
            self.soft_hard_display_restore(m)

    def main(self):
        self.restore_selected()
