import maya.cmds as cmds
from maya.mel import eval as meval
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

description = "Select object faces and click the tool"


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
		<p style="color: #aaa;">Detaches object`s faces without separates .</p>
		'''
		self.label  = QLabel(html)


		self.mainLayout.addWidget(self.label)

		return self.mainLayout

	def polyDetach(self):
		bsp_face = cmds.filterExpand( ex=False, sm=34 )
		if bsp_face:
			meval('DetachComponent')
		else:
			cmds.inViewMessage(amg= '<hl>Please select faces that should be detached</hl>' , pos = 'midCenter', fade = True, fot = 1000)
			return

	# @classmethod
	def main(self):
		self.polyDetach()

