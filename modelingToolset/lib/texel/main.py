import maya.cmds as cmds
import maya.mel as mel
from maya.mel import eval as meval
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaRender as OpenMayaRender

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *


description = "Texel Computing. Please use options to compute texel"
buttonType = "opt"
beautyName = "Texel Computing"
iconName = "Calculate Texel"

DIMENSION = [256, 512, 1024, 2048, 4096]

class Utils(object):


	@classmethod
	def load_option_var(cls):
		#resolutions
		#offset type
		#offset value

		options = [2048, 0, 12, 40, 0]

		if cmds.optionVar( exists='texel_resolution' ):
			options[0] = cmds.optionVar( q='texel_resolution' )
		else:
			cmds.optionVar( iv=('texel_resolution', options[0]))

		if cmds.optionVar( exists='texel_offset_type' ):
			options[1] = cmds.optionVar( q='texel_offset_type' )
		else:
			cmds.optionVar( iv=('texel_offset_type', options[1]))

		if cmds.optionVar( exists='texel_offset_percent' ):
			options[2] = cmds.optionVar( q='texel_offset_percent' )
		else:
			cmds.optionVar( iv=('texel_offset_percent', options[2]))

		if cmds.optionVar( exists='texel_offset_polygons' ):
			options[3] = cmds.optionVar( q='texel_offset_polygons' )
		else:
			cmds.optionVar( iv=('texel_offset_polygons', options[3]))

		if cmds.optionVar( exists='texel_neitral_color' ):
			options[4] = cmds.optionVar( q='texel_neitral_color' )
		else:
			cmds.optionVar( iv=('texel_neitral_color', options[4]))

		return options


	@classmethod
	def save_option_var(cls, option, value):
		cmds.optionVar(iv=(option, int(value)))


class ToolOptions(QWidget):

	def __init__(self, parent = None):

		super(ToolOptions, self).__init__(parent)

		'''DATA'''
		self.texture_size_combobox = 1024
		self.resolutions = DIMENSION
		self.options = Utils.load_option_var()
		self.setLayout(self.createUI())

	def createUI(self):

		self.loadPlugin()

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

		self.resultLabel = QLabel("Texel calculation results: Select mesh or face(s) and press Compute")
		self.resultLabel.setMinimumHeight(40)
		self.resultLabel.setMaximumHeight(40)

		'''interactive'''
		self.hud_layout = QHBoxLayout()
		self.buttons_group = QButtonGroup()
		for res in self.resolutions:
			hud = QRadioButton(str(res))
			if res == self.options[0]:
				hud.setChecked(1)
			hud.clicked.connect(self.sender_value)
			self.buttons_group.addButton(hud)
			self.hud_layout.addWidget(hud)

		'''options'''
		self.optionLayout = QHBoxLayout()
		self.optA = QRadioButton("Normal Size")
		self.optA.setChecked(1)
		self.optA.clicked.connect(self.setValue)
		self.optB = QRadioButton("Half Vert")
		self.optB.clicked.connect(self.setValue)
		self.optC = QRadioButton("Half Horz")
		self.optC.clicked.connect(self.setValue)

		self.optionLayout.addWidget(self.optA)
		self.optionLayout.addWidget(self.optB)
		self.optionLayout.addWidget(self.optC)

		'''apply'''
		self.applyButton = QPushButton("Compute")
		self.applyButton.clicked.connect(self.setValue)

		'''main layout'''
		self.mainLayout.addLayout(self.optionLayout)
		self.mainLayout.addLayout(self.hud_layout)
		self.mainLayout.addWidget(self.resultLabel)
		self.mainLayout.addWidget(self.applyButton)

		return self.mainLayout


	def loadPlugin(self):
		if not cmds.pluginInfo( 'techartAPI2018', query=True, loaded=True):
			try:
				cmds.loadPlugin('techartAPI2018')
			except:
				print('Don`t load plugin')


	def sender_value(self):
		button = self.sender()
		Utils.save_option_var('texel_resolution', button.text())
		self.setValue()


	def setValue(self):
		#print 'Texel HUD'
		#self.loadPlugin()
		distortion = ''
		try:
			face_count = cmds.polyEvaluate( f=True )
			face_distortion = len(cmds.stretchUV())
			if float(face_distortion)/float(face_count) > 0.5:
				distortion = ' (distortion)'
		except:
			pass

		comp = cmds.texelFaces(avr =1, txl =1)

		if self.optB.isChecked():
			selected = cmds.filterExpand(sm = (12, 34))
			#cmds.polyListComponentConversion( fvf=True, te=True, vfa=True )
			uv  = cmds.polyListComponentConversion(selected, tuv=True)
			cmds.polyEditUV(uv, pu=0, pv=0, su=1, sv = 0.5)
			comp = cmds.texelFaces(avr =1, txl =1)
			cmds.polyEditUV(uv, pu=0, pv=0, su=1, sv = 2.0)

		if self.optC.isChecked():
			selected = cmds.filterExpand(sm = (12, 34))
			uv  = cmds.polyListComponentConversion(selected, tuv=True)
			cmds.polyEditUV(uv, pu=0, pv=0, su=0.5, sv = 1.0)
			comp = cmds.texelFaces(avr =1, txl =1)
			cmds.polyEditUV(uv, pu=0, pv=0, su=2, sv = 1)



		#face_count = cmds.polyEvaluate( f=True )
		#face_distortion = len(cmds.stretchUV())

		if comp > 0.0:
			value = Utils.load_option_var()[0]
			#if float(face_distortion)/float(face_count) > 0.5:
			#	comp = comp * 0.5

			result = int(value)/128.0*comp

			try:
				self.resultLabel.setText("Texel calculation results: " + str(int(result)))
			except:
				pass

			if cmds.headsUpDisplay('HUDtexelMessure', q=1, ex=1):
				cmds.headsUpDisplay('HUDtexelMessure', e=1, label=str(value) + ' ')

			print('Result', result)

			return str(int(result)) + distortion

		else:
			print('Nothing selected _')
			try:
				self.resultLabel.setText("Texel calculation results: Select mesh or face(s) and press Compute")
			except:
				pass

			return ''


	def main(self):
		cmds.inViewMessage(amg= '<hl>Please open options to compute texel</hl>' , pos = 'topLeft', fade = True, fot = 1000)
		self.loadPlugin()
		hud = Utils.load_option_var()

		if cmds.headsUpDisplay( 'HUDtexelMessure', q=1, ex=1):
			#print 'Exist'
			cmds.headsUpDisplay( 'HUDtexelMessure', rem=True )

		else:
			print('Don`t exist')
			nfb = cmds.headsUpDisplay(nfb =0);
			cmds.headsUpDisplay( 'HUDtexelMessure', section=0,
										block = nfb,
										blockSize='small',
										label=str(hud[0]) + ' ',
										labelFontSize='large',
										dfs = 'large',
										command= self.setValue,
										event='SelectionChanged')

