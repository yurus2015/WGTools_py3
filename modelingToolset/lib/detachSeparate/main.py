import maya.cmds as cmds
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

description = "Select object faces and click the tool"


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
		<p style="color: #aaa;">Detaches and separates object faces.</p>
		'''
        self.label = QLabel(html)

        self.mainLayout.addWidget(self.label)

        return self.mainLayout

    def polyDetach(self):
        bsp_face = cmds.filterExpand(ex=False, sm=34)
        if bsp_face:
            newObj = []
            objShape = cmds.ls(sl=True, fl=True, o=True, l=True)
            objShape = cmds.ls(objShape, s=1)
            for shape in objShape:
                objTr = cmds.listRelatives(shape, p=True, f=True)
                objName = cmds.listRelatives(shape, p=True, f=False)
                dupObj = cmds.duplicate(objTr, n=(objName[0] + '_1'))
                dupTr = cmds.listRelatives(dupObj, c=True, typ="transform", f=True)
                if dupTr:
                    cmds.delete(dupTr)
                extention = []
                for face in bsp_face:
                    if objName[0] in face:
                        f = face.split('.', 1)
                    extention.append(dupObj[0] + '.' + f[1])
                faceObj = cmds.ls(dupObj[0] + '.f[*]', fl=True)
                extention = cmds.ls(extention, fl=True)
                faceObj = list(set(faceObj) - set(extention))
                cmds.delete(faceObj)
                newObj.append(dupObj[0])
            cmds.delete(bsp_face)
            cmds.selectMode(object=True)
            cmds.select(newObj)
        else:
            cmds.inViewMessage(amg='<hl>Please select faces that should be detached and separated</hl>',
                               pos='midCenter', fade=True, fot=1000)
            return

    # @classmethod
    def main(self):
        self.polyDetach()
