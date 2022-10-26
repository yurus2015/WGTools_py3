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


description = "Set all meshes uv_sets to map1"
buttonType = "opt"
#beautyName = "Hard/Soft Edges Fix"
#iconName = "Hard/Soft Edges Fix"

class ToolOptions(QWidget):

	def __init__(self, parent = None):

		super(ToolOptions, self).__init__(parent)


		self.setLayout(self.createUI())

	def createUI(self):

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setContentsMargins(5,5,5,5)
		self.mainLayout.setSpacing(5) #layout
		self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

		self.label  = QLabel("<b>Set all meshes uv_sets to map1</p>")

		self.mainLayout.addWidget(self.label)

		return self.mainLayout


	def main(self):

		meshes = cmds.ls(type = 'mesh')
		for i in meshes:
			try:
				cmds.polyUVSet(i, currentUVSet=True,  uvSet='map1')
			except:
				print((i + ' doesn`t have map1'))

