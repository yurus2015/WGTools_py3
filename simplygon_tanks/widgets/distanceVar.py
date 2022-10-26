#from PySide import QtCore, QtGui
import maya.cmds as cmds
from maya.mel import eval as meval

#maya2018 pyside2
try:
	from PySide import QtGui, QtCore
	from PySide.QtGui import *
	from PySide.QtCore import *
except ImportError:
	from PySide2 import QtGui, QtCore, QtWidgets
	from PySide2.QtGui import *
	from PySide2.QtCore import *
	from PySide2.QtWidgets import *



class SG_lodDistance(QWidget):
	def __init__(self, parent = None):
		super(SG_lodDistance, self).__init__(parent)

		self.initUI()

		self.initOptionVarLodDistance()

	def initUI(self):
		#create main layout
		self.baseLayout = QVBoxLayout(self)
		self.baseLayout.setSpacing(10)

		self.lod0Layout = QHBoxLayout()
		self.lod0Layout.setSpacing(10)
		self.lod0Layout.setContentsMargins(10, -1, 10, -1)
		self.lod1Layout = QHBoxLayout()
		self.lod1Layout.setSpacing(10)
		self.lod1Layout.setContentsMargins(10, -1, 10, -1)
		self.lod2Layout = QHBoxLayout()
		self.lod2Layout.setSpacing(10)
		self.lod2Layout.setContentsMargins(10, -1, 10, -1)
		self.lod3Layout = QHBoxLayout()
		self.lod3Layout.setSpacing(10)
		self.lod3Layout.setContentsMargins(10, -1, 10, -1)

		self.textLaybel_lod0 = QLabel('lod0')
		self.textLaybel_val0 = QLabel('32') # get option var
		self.lod0Slider = QSlider()
		self.lod0Slider.setRange(0, 200)
		self.lod0Slider.setSingleStep(1)
		self.lod0Slider.setOrientation(QtCore.Qt.Horizontal)

		self.textLaybel_lod1 = QLabel('lod1')
		self.textLaybel_val1 = QLabel('64') # get option var
		self.lod1Slider = QSlider()
		self.lod1Slider.setRange(0, 200)
		self.lod1Slider.setSingleStep(1)
		self.lod1Slider.setOrientation(QtCore.Qt.Horizontal)

		self.textLaybel_lod2 = QLabel('lod2')
		self.textLaybel_val2 = QLabel('96') # get option var
		self.lod2Slider = QSlider()
		self.lod2Slider.setRange(0, 200)
		self.lod2Slider.setSingleStep(1)
		self.lod2Slider.setOrientation(QtCore.Qt.Horizontal)

		self.textLaybel_lod3 = QLabel('lod3')
		self.textLaybel_val3 = QLabel('192') # get option var
		self.lod3Slider = QSlider()
		self.lod3Slider.setRange(0, 200)
		self.lod3Slider.setSingleStep(1)
		self.lod3Slider.setOrientation(QtCore.Qt.Horizontal)

		#parenting widgets
		self.lod0Layout.addWidget(self.textLaybel_lod0)
		self.lod0Layout.addWidget(self.lod0Slider)
		self.lod0Layout.addWidget(self.textLaybel_val0)

		self.lod1Layout.addWidget(self.textLaybel_lod1)
		self.lod1Layout.addWidget(self.lod1Slider)
		self.lod1Layout.addWidget(self.textLaybel_val1)

		self.lod2Layout.addWidget(self.textLaybel_lod2)
		self.lod2Layout.addWidget(self.lod2Slider)
		self.lod2Layout.addWidget(self.textLaybel_val2)

		self.lod3Layout.addWidget(self.textLaybel_lod3)
		self.lod3Layout.addWidget(self.lod3Slider)
		self.lod3Layout.addWidget(self.textLaybel_val3)

		self.baseLayout.addLayout(self.lod0Layout)
		self.baseLayout.addLayout(self.lod1Layout)
		self.baseLayout.addLayout(self.lod2Layout)
		self.baseLayout.addLayout(self.lod3Layout)

		self.loadOptionVarLodDistance()

		self.lod0Slider.valueChanged.connect(self.saveOptionVarLodDistance)
		self.lod1Slider.valueChanged.connect(self.saveOptionVarLodDistance)
		self.lod2Slider.valueChanged.connect(self.saveOptionVarLodDistance)
		self.lod3Slider.valueChanged.connect(self.saveOptionVarLodDistance)



	def initOptionVarLodDistance(self):

		if not cmds.optionVar( exists='distance_lod_0' ):
			cmds.optionVar( iv=('distance_lod_0', 32))
		if not cmds.optionVar( exists='distance_lod_1' ):
			cmds.optionVar( iv=('distance_lod_1', 64))
		if not cmds.optionVar( exists='distance_lod_2' ):
			cmds.optionVar( iv=('distance_lod_2', 96))
		if not cmds.optionVar( exists='distance_lod_3' ):
			cmds.optionVar( iv=('distance_lod_3', 192))

	def loadOptionVarLodDistance(self):


		self.lod0Slider.setValue(cmds.optionVar( q='distance_lod_0' ))
		self.textLaybel_val0.setText(str(cmds.optionVar( q='distance_lod_0' )))
		#print 'OPTION VAR 0', cmds.optionVar( q='distance_lod_0' )


		self.lod1Slider.setValue(cmds.optionVar( q='distance_lod_1' ))
		self.textLaybel_val1.setText(str(cmds.optionVar( q='distance_lod_1' )))
		#print 'OPTION VAR 1', cmds.optionVar( q='distance_lod_1' )

		self.lod2Slider.setValue(cmds.optionVar( q='distance_lod_2' ))
		self.textLaybel_val2.setText(str(cmds.optionVar( q='distance_lod_2' )))
		#print 'OPTION VAR 2', cmds.optionVar( q='distance_lod_2' )

		self.lod3Slider.setValue(cmds.optionVar( q='distance_lod_3' ))
		self.textLaybel_val3.setText(str(cmds.optionVar( q='distance_lod_3' )))
		#print 'OPTION VAR 3', cmds.optionVar( q='distance_lod_3' )


	def saveOptionVarLodDistance(self):
		val0 = self.lod0Slider.value()
		self.textLaybel_val0.setText(str(val0))

		val1 = self.lod1Slider.value()
		self.textLaybel_val1.setText(str(val1))

		val2 = self.lod2Slider.value()
		self.textLaybel_val2.setText(str(val2))

		val3 = self.lod3Slider.value()
		self.textLaybel_val3.setText(str(val3))

		#up
		if val0 > val1:
			self.lod1Slider.setValue(val0)
		if val1 > val2:
			self.lod2Slider.setValue(val1)
		if val2 > val3:
			self.lod3Slider.setValue(val2)

		#down
		if val1 < val0:
			self.lod0Slider.setValue(val1)
		if val2 < val1:
			self.lod1Slider.setValue(val2)
		if val3 < val2:
			self.lod2Slider.setValue(val3)

		#set distance attribut in node

		try:
			cmds.setAttr('switcher.threshold[0]', val0)
			cmds.setAttr('switcher.threshold[1]', val1)
			cmds.setAttr('switcher.threshold[2]', val2)
			cmds.setAttr('switcher.threshold[3]', val3)
		except:
			pass


		#save option var
		cmds.optionVar( iv=('distance_lod_0', val0))
		cmds.optionVar( iv=('distance_lod_1', val1))
		cmds.optionVar( iv=('distance_lod_2', val2))
		cmds.optionVar( iv=('distance_lod_3', val3))




