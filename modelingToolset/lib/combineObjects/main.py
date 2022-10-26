import maya.cmds as cmds
from maya.mel import eval as meval
from PySide2 import QtGui, QtCore, QtWidgets
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
        self.mainLayout.setSpacing(10)  # layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        html = '''
        <b>Description:</b>
        <p style="color: #aaa;">Combines objects preserving a pivot,\n
        transforms and hierarchy of the selected object</p>
        '''

        self.number_group = QButtonGroup(self.mainLayout)  # Number group
        self.first = QRadioButton("to first")
        self.last = QRadioButton("to last")
        self.number_group.addButton(self.first)
        self.number_group.addButton(self.last)
        self.first.setChecked(True)

        self.label = QLabel(html)
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.first)
        self.mainLayout.addWidget(self.last)
        # self.mainLayout.addWidget(self.number_group)

        return self.mainLayout

    def confirm_dialog(self, title=None, message=None):
        cmds.confirmDialog(title=title, message=message, button=['   OK   '], defaultButton='   OK   ')

    def combine_objects(self, first=True):
        selected = cmds.ls(sl=True, fl=True, l=True, o=True)
        selected = cmds.filterExpand(sm=[12])
        if not selected:
            self.confirm_dialog('Error', 'Select two or more meshes')
            return
        if len(selected) < 2:
            self.confirm_dialog('Error', 'Select two or more meshes')
            return

        master = selected[0]
        masterShapes = cmds.listRelatives(master, s=True, path=True)
        combine = cmds.polyUnite(selected, ch=True)
        childShapes = cmds.listRelatives(combine[0], s=True, path=True)
        finalShape = cmds.rename(childShapes[0], masterShapes[0])
        finalShape = cmds.parent(finalShape, master, s=True)
        cmds.delete(master, ch=True)
        cmds.delete(combine[0])

        parentTransform = cmds.listRelatives(finalShape[0], f=True, p=True)
        cmds.makeIdentity(parentTransform, apply=True, t=1, r=1, s=1, n=0)
        cmds.parent(finalShape[0], master, s=True, addObject=True)
        cmds.delete(parentTransform)
        selected.remove(master)
        for unit in selected:
            if cmds.objExists(unit):
                cmds.delete(unit)

        shortName = master.split('|')[-1]
        masterShapes = cmds.listRelatives(master, s=True, path=True)
        cmds.select(masterShapes)
        evalCMD = 'renameSelectionList("' + shortName + 'Shape")'
        meval(evalCMD)
        cmds.select(master)

    def main(self):
        self.combine_objects()
