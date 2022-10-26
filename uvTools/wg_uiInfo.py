try:
	from PySide import QtGui, QtCore
	from PySide.QtGui import *
	from PySide.QtCore import *
except ImportError:
	from PySide2 import QtGui, QtCore, QtWidgets
	from PySide2.QtGui import *
	from PySide2.QtCore import *
	from PySide2.QtWidgets import *
try:
	from shiboken import wrapInstance
except:
	from shiboken2 import wrapInstance

import maya.OpenMayaUI as omu


import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import os, datetime

dir = str(os.path.dirname(__file__))

def mainWindowPointer():
	ptr = omu.MQtUtil.mainWindow() #pointer for the main window
	return wrapInstance(int(ptr), QWidget)

class UI_Info(QDialog):
	def __init__(self, size, parent = mainWindowPointer()):
	#def __init__(self, parent = None,  *args, **kwargs):
		QDialog.__init__(self,parent)
		self.setWindowTitle("UI Info")

		width_ui = 300
		height_ui = 170
		if size > 100: width_ui = 200 + size
		if size > 100: height_ui = 70 + size

		self.setFixedSize(width_ui, height_ui);
		self.setObjectName("id_UI_Info")

		self.pixmap = QPixmap(QtCore.QSize(size,size))
		self.painter = QPainter()
		self.colorWhite = QColor()
		self.colorBlack = QColor()
		self.colorRed = QColor()

		self.setLayout(self.create_layout(size))
		self.connections(size)
		#self.checkSelected(size)
		self.updateInfo(size)


	def create_layout(self, size):
		self.label1_0 = QLabel("Region:")
		self.label1_0.setFixedWidth(100)
		self.label1_1 = QLabel("[0:1]")
		self.label2_0 = QLabel("Current UV Set:")
		self.label2_0.setFixedWidth(100)
		self.label2_1 = QLabel("map1")
		self.label3_0 = QLabel("UV Area:")
		self.label3_0.setFixedWidth(100)
		self.label3_1 = QLabel("0%")
		self.label4_0 = QLabel("Number of UV Shells:")
		self.label4_1 = QLabel("0")
		self.label5_0 = QLabel("Out of region shells:")
		self.label5_1 = QLabel("0")

		self.btnOK =   QPushButton("Close");
		self.btnUpdate = QPushButton("Update")

		self.layoutMain = QVBoxLayout()
		self.layoutBtn = QHBoxLayout()
		self.layoutContent = QHBoxLayout()
		self.layoutText = QVBoxLayout()
		self.layoutText.setContentsMargins(0, 10, 0, 0)
		#self.layoutFixedText = QVBoxLayout()
		#self.layoutChangedText = QVBoxLayout()


		self.layoutInfo_01 = QHBoxLayout()
		self.layoutInfo_02 = QHBoxLayout()
		self.layoutInfo_03 = QHBoxLayout()
		self.layoutInfo_04 = QHBoxLayout()
		self.layoutInfo_05 = QHBoxLayout()

		#______________________________________________________________________
		self.imgLabel = QLabel()
		self.imgLabel.setFixedSize(size+20, size+10)

		#setup drawing colors
		self.colorWhite.setRgb(255,255,255,255)
		self.colorBlack.setRgb(0,0,0,255)
		self.colorRed.setRgb(255,0,0,255)
		self.pixmap.fill(self.colorBlack)

		self.imgLabel.setPixmap(self.pixmap)
		#_______________________________________________________________________

		#settings
		self.layoutContent.setAlignment(QtCore.Qt.AlignTop)
		#self.label1_0.setStyleSheet("padding-top: 20px;")
		#self.label1_1.setStyleSheet("padding-top: 20px; padding-left: 20px;")
		#self.label2_1.setStyleSheet("padding-left: 20px;")
		#self.label3_1.setStyleSheet("padding-left: 20px;")
		#self.label4_1.setStyleSheet("padding-left: 7px;")
		#self.label5_1.setStyleSheet("padding-left: 9px;")


		#connecting
		self.layoutInfo_01.addWidget(self.label1_0)
		self.layoutInfo_01.addWidget(self.label1_1)

		self.layoutInfo_02.addWidget(self.label2_0)
		self.layoutInfo_02.addWidget(self.label2_1)

		self.layoutInfo_03.addWidget(self.label3_0)
		self.layoutInfo_03.addWidget(self.label3_1)

		self.layoutInfo_04.addWidget(self.label4_0)
		self.layoutInfo_04.addWidget(self.label4_1)

		self.layoutInfo_05.addWidget(self.label5_0)
		self.layoutInfo_05.addWidget(self.label5_1)

		self.layoutContent.addWidget(self.imgLabel)
		self.layoutContent.addLayout(self.layoutText)

	   # self.layoutText.addLayout(self.layoutFixedText)




		self.layoutText.addLayout(self.layoutInfo_01)
		self.layoutText.addLayout(self.layoutInfo_02)
		self.layoutText.addLayout(self.layoutInfo_03)
		# self.layoutContent.addLayout(self.layoutInfo_04)
		# self.layoutContent.addLayout(self.layoutInfo_05)

		self.layoutBtn.addWidget(self.btnOK)
		self.layoutBtn.addWidget(self.btnUpdate)

		self.layoutMain.addLayout(self.layoutContent)
		self.layoutMain.addLayout(self.layoutBtn)

		self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.layoutText.addItem(self.verticalSpacer)

		return self.layoutMain

	def connections(self, size):
		#print 'SZ', size
		self.connect(self.btnOK, QtCore.SIGNAL("clicked()"), self.tempProc)
		#self.connect(self.btnUpdate, QtCore.SIGNAL("clicked()"), self.updateInfo)
		self.connect(self.btnUpdate, QtCore.SIGNAL("clicked()"), lambda: self.updateInfo(size))

	def tempProc(self):
		self.close()

	def checkSelected(self, size):
		selected = cmds.ls(sl=1, l=1)
		objectToProcess = None
		if selected:
			for i in selected:
				if cmds.ls(cmds.listRelatives(i, c=1, type="mesh", f=1)):
					objectToProcess = i
					break
			if objectToProcess:
				self.updateInfo(size)

	def updateInfo(self, size):

		#print 'SIZE', size
		self.pixmap.fill(self.colorBlack)

		obj = cmds.filterExpand(sm=12)
		if obj:


			for o in obj:
				#start processing object
				# 1 - get current uv set
				currentUVSet = cmds.polyUVSet(o, q=1, cuv=1)
				if currentUVSet:
					self.label2_1.setText(currentUVSet[0])

				#check if the object has some uvs
				numUVs = cmds.polyEvaluate(o, uv=1)

				if numUVs > 0:
					# 2 - drawing uv shells

					selectionList = OpenMaya.MSelectionList()

					selectionList.add(o)
					dagPath = OpenMaya.MDagPath()
					mObject = OpenMaya.MObject()

					selectionList.getDagPath(0,dagPath, mObject)

					iter = OpenMaya.MItMeshPolygon(dagPath)
					while not iter.isDone():
						uCoord = OpenMaya.MFloatArray()
						vCoord = OpenMaya.MFloatArray()
						iter.getUVs(uCoord, vCoord, currentUVSet[0])
						uvCount = uCoord.length()
						# print "face: ", uCoord, vCoord

						QArray = QPolygonF()
						for i in range(len(uCoord)):
							curU = int(uCoord[i] * size)
							curV = size - int(vCoord[i] * size)
							point = QtCore.QPointF(curU, curV)
							# print point
							QArray.append(point)
						# print "formated: ", QArray #QArray wrong

						self.painter.begin(self.pixmap)
						self.painter.setBrush(QBrush(self.colorWhite))
						self.painter.setPen(self.colorWhite)
						self.painter.drawConvexPolygon(QArray)
						self.painter.end()
						self.imgLabel.setPixmap(self.pixmap)
						iter.next()


			#3 - get black pixels and get area = 10000 - len(blackPixels)
			blackPixelCount = 0
			img = self.pixmap.toImage()
			for i in range(0,size):
				for j in range(0,size):
					color = QColor()
					color =QColor.fromRgb(img.pixel(i,j))
					if color == QtCore.Qt.black:
						blackPixelCount += 1

			precentage = 100 - float(blackPixelCount)/(size*size)*100
			self.label3_1.setText(str(precentage) + "%")

			# self.pixmap.save('D:/pixmap.jpg')








def main(size):
	if cmds.window("id_UI_Info",q=True,exists=True):
		cmds.deleteUI("id_UI_Info")

	try:
		dialog.close()
	except:
		pass

	dialog = UI_Info(size)
	dialog.show()



