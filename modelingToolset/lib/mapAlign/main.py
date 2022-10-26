import maya.cmds as cmds
import maya.mel as mel
import  math, operator

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

description = "Select faces or edges on meshes"
buttonType = "opt"
beautyName = "Map Align"
iconName = "Map Align"


class ToolOptions(QWidget):

	def __init__(self, parent = None):

		super(ToolOptions, self).__init__(parent)

		self.matchUVTarget = []
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

		self.tol_label = QLabel("Tolerance: ")
		self.tol_edit = QLineEdit("0.0015")
		self.tol_edit.setInputMask("9.9999")

		if cmds.optionVar(exists = 'wg_mdltls_mapAlign_distTol'):
			self.tol_edit.setText(str(float(cmds.optionVar(q = 'wg_mdltls_mapAlign_distTol'))))

		self.but_storeTUV = QPushButton("Store Target UV")
		self.but_storeTUV.clicked.connect(self.storeTarget)
		self.but_clearTUV = QPushButton("Clear Target UV")
		self.but_clearTUV.clicked.connect(self.clearTarget)
		self.but_matchUV = QPushButton("Match UV")
		self.but_matchUV.clicked.connect(self.matchUV)


		self.layout_tolerance.addWidget(self.tol_label)
		self.layout_tolerance.addWidget(self.tol_edit)
		self.layout_buttons.addWidget(self.but_storeTUV)
		self.layout_buttons.addWidget(self.but_clearTUV)

		self.mainLayout.addLayout(self.layout_tolerance)
		self.mainLayout.addLayout(self.layout_buttons)
		self.mainLayout.addWidget(self.but_matchUV)


		return self.mainLayout

	def removeList(self, fromList, thisList):
		resultList = [ n for n in fromList if n not in thisList ]
		resultList = list(resultList)
		return resultList

	def distance(self, p0, p1):
		dist = math.hypot(p0[0] - p1[0], p0[1] - p1[1])
		return dist

	def storeTarget(self):
		cmds.undoInfo(ock=1)

		singleUVTarget = cmds.filterExpand(sm = 35, ex=1)
		if singleUVTarget:
			mel.eval('polySelectBorderShell 0')
			self.matchUVTarget = cmds.filterExpand(sm = 35, ex=1)
			cmds.select(singleUVTarget)
		else:
			cmds.inViewMessage(amg= '<hl>Select any UV of the target shell</hl>' , pos = 'midCenter', fade = True, fot = 1000)


		cmds.undoInfo(cck=1)

	def clearTarget(self):
		cmds.undoInfo(ock=1)

		self.matchUVTarget = []
		cmds.inViewMessage(amg= '<hl>Target UVs clear</hl>' , pos = 'midCenter', fade = True, fot = 1000)


		cmds.undoInfo(cck=1)

	def matchUV(self):
		distTol = 0.0
		try:
			distTol = float(self.tol_edit.text())
		except:
			cmds.inViewMessage(amg= '<hl>Make sure you use correct Tolerance number type</hl>' , pos = 'midCenter', fade = True, fot = 1000)
			return

		cmds.optionVar(sv=("wg_mdltls_mapAlign_distTol", self.tol_edit.text()))

		cmds.undoInfo(ock=1)

		if not self.matchUVTarget:
			cmds.inViewMessage(amg= '<hl>Set target UVs</hl>' , pos = 'midCenter', fade = True, fot = 1000)
			return

		sourceUV = cmds.filterExpand(sm=35, ex=1)
		if sourceUV:
			sourceUV = self.removeList(sourceUV, self.matchUVTarget)
			if sourceUV:
				for uvs in sourceUV:
					sourceCoord = cmds.polyEditUV( uvs, query=True )
					distansArray = []
					for uvt in self.matchUVTarget:
						targetCoord = cmds.polyEditUV( uvt, query=True )
						dist = self.distance(sourceCoord,targetCoord)
						distansArray.append(dist)
					min_index, min_value = min(enumerate(distansArray), key=operator.itemgetter(1))
					targetCoord = cmds.polyEditUV( self.matchUVTarget[min_index], query=True )
					cmds.polyEditUV(uvs, relative=False, uValue=targetCoord[0], vValue=targetCoord[1])
				cmds.select(sourceUV)

			else:
				cmds.inViewMessage(amg= '<hl>Source UVs coincide with target UVs</hl>' , pos = 'midCenter', fade = True, fot = 1000)
		else:
			cmds.inViewMessage(amg= '<hl>Select source UVs for compare</hl>' , pos = 'midCenter', fade = True, fot = 1000)


		cmds.undoInfo(cck=1)


	def main():
		pass

