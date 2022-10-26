from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import maya.cmds as cmds
#import wg_modelingToolset.utils.scene as scene_u
from . import snapShellGrid as snp_s
import importlib
importlib.reload(snp_s)

description = "Scale uv-shell to the nearest grid value"
buttonType = "opt"
beautyName = "Shell Scale to Grid"
iconName = "Shell Scale to Grid"

error_selected = "Select mesh or mesh components"
error_value = "Enter value in custom texture field"
error_color = 'red'
error_size = '4'
texture_maximum = 10000
value_labels = ['256', '512', '1024', '2048', '4096', '8192']

class ToolOptions(QWidget):

	def __init__(self, parent = None):
		super(ToolOptions, self).__init__(parent)

		self.setLayout(self.layers())
		self.button_labels()
		self.compileLayers()
		self.currentGridSubdive = 1

	def layers(self):
		self.masterLayout = QVBoxLayout()
		self.masterLayout.setContentsMargins(5,5,5,5)
		self.masterLayout.setSpacing(10) #layout
		self.masterLayout.setAlignment(QtCore.Qt.AlignTop)

		self.checkLayout = QHBoxLayout()
		self.checkLayout.setSpacing(10)
		self.checkLayout.setContentsMargins(0,0,0,0)
		self.checkLayout.setAlignment(QtCore.Qt.AlignLeft)

		self.presetLayout0 = QHBoxLayout()
		self.presetLayout0.setSpacing(10)
		self.presetLayout0.setContentsMargins(0,0,0,0)

		self.presetLayout1 = QHBoxLayout()
		self.presetLayout1.setSpacing(10)
		self.presetLayout1.setContentsMargins(0,0,0,0)

		self.presetLayout2 = QHBoxLayout()
		self.presetLayout2.setSpacing(10)
		self.presetLayout2.setContentsMargins(0,0,0,0)

		self.presetLayout3 =  QGridLayout()
		self.presetLayout3.setSpacing(10)
		self.presetLayout3.setContentsMargins(0,0,0,0)
		self.presetLayout3.setColumnStretch(0, 1)
		self.presetLayout3.setColumnStretch(1, 1)

		self.fieldLayout = QHBoxLayout()
		self.fieldLayout.setSpacing(10)
		self.fieldLayout.setContentsMargins(0,0,0,0)

		self.butLayout = QHBoxLayout()
		self.butLayout.setSpacing(10)
		self.butLayout.setContentsMargins(0,0,0,0)

		return self.masterLayout

	def button_labels(self):
		self.label  = QLabel("<b>Description:</b><p>Scale uv-shell to the nearest grid value</p>")
		self.gridCheckBtn = QPushButton('Display uv-editor grid')
		self.gridCheckBtn.setCheckable(True)
		self.gridCheckBtn.setChecked(False)
		self.gridCheckBtn.clicked.connect(lambda:self.gridChanges(self.gridCheckBtn.isChecked()))
		self.smallSelectBtn = QPushButton('Select unsnapped(small) shells')
		self.smallSelectBtn.setCheckable(True)
		self.smallSelectBtn.setChecked(False)
		#self.smallSelectBtn.clicked.connect(lambda:self.selectSmall(self.smallSelectBtn.isChecked()))
		self.scale_256 = QPushButton("256*256")
		self.scale_256.clicked.connect(lambda x = 256: self.setShellSize(x))
		self.scale_1024 = QPushButton("1024*1024")
		self.scale_512 = QPushButton("512*512")
		self.scale_512.clicked.connect(lambda x = 512: self.setShellSize(x))
		self.scale_1024 = QPushButton("1024*1024")
		self.scale_1024.clicked.connect(lambda x = 1024: self.setShellSize(x))
		self.scale_2048 = QPushButton("2048*2048")
		self.scale_2048.clicked.connect(lambda x = 2048: self.setShellSize(x))
		self.scale_4096 = QPushButton("4096*4096")
		self.scale_4096.clicked.connect(lambda x = 4096: self.setShellSize(x))
		self.scale_8192 = QPushButton("8192*8192")
		self.scale_8192.clicked.connect(lambda x = 8192: self.setShellSize(x))
		self.customLabel = QLabel("Custom Texture Size: ")
		self.customValue = QLineEdit()
		self.customValue.setStyleSheet("background-color: #111;")
		self.customValue.setValidator(QIntValidator(0, texture_maximum))
		self.customButton = QPushButton("Snap Shell")
		self.customButton.clicked.connect(lambda: self.setShellSize(self.customValue.text()))
		self.errorMsg  = QLabel()
		self.errorMsg.setVisible(False)

	def compileLayers(self):
		self.masterLayout.addLayout(self.checkLayout)
		self.masterLayout.addLayout(self.presetLayout0)
		self.masterLayout.addLayout(self.presetLayout0)
		self.masterLayout.addLayout(self.presetLayout1)
		self.masterLayout.addLayout(self.presetLayout2)
		self.masterLayout.addLayout(self.presetLayout3)
		self.masterLayout.addWidget(self.errorMsg)

		self.checkLayout.addWidget(self.gridCheckBtn)
		self.checkLayout.addWidget(self.smallSelectBtn)

		self.presetLayout0.addWidget(self.scale_256)
		self.presetLayout0.addWidget(self.scale_512)
		self.presetLayout1.addWidget(self.scale_1024)
		self.presetLayout1.addWidget(self.scale_2048)
		self.presetLayout2.addWidget(self.scale_4096)
		self.presetLayout2.addWidget(self.scale_8192)
		self.presetLayout3.addLayout(self.fieldLayout, 0, 0)
		self.presetLayout3.addLayout(self.butLayout, 0, 1)
		self.fieldLayout.addWidget(self.customLabel)
		self.fieldLayout.addWidget(self.customValue)
		self.butLayout.addWidget(self.customButton)

	def gridChanges(self, checked):
		print('checked', checked)
		texWinName = cmds.getPanel(sty='polyTexturePlacementPanel')
		if checked:
			self.currentGridSubdive = cmds.textureWindow(texWinName[0], q=True, d=True)
		if not checked:
			cmds.textureWindow(texWinName[0], e=True, d=self.currentGridSubdive)

	def setShellSize(self, size = None):
		grid = self.gridCheckBtn.isChecked()
		small = self.smallSelectBtn.isChecked()
		if size and int(size):
			size = int(size)
			if snp_s.snapShell(size, grid, small):
				self.errorMsg.setText("<b>Error:</b><p><font color='"+ error_color +"', size = "+ error_size +">"+error_selected+"</font></p>")
				self.errorMsg.setVisible(True)
			else:
				self.errorMsg.setVisible(False)
		else:
			self.errorMsg.setText("<b>Error:</b><p><font color='"+ error_color +"', size = "+ error_size +">"+error_value+"</font></p>")
			self.errorMsg.setVisible(True)

	def main():
		pass

