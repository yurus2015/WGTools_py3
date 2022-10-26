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

import modelingToolset2019.utils.scene as scene_u

description = "Adds a rotation animation to all tracks found in the scene"
buttonType = "opt"
beautyName = "TrackAnimation"
iconType = "toggle"
iconName = "Animate tracks"


class ToolOptions(QWidget):

	def __init__(self, parent = None):

		super(ToolOptions, self).__init__(parent)

		self.setLayout(self.createUI())
		self.track_animation_state = False


	def createUI(self):

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setContentsMargins(5,5,5,5)
		self.mainLayout.setSpacing(5) #layout
		self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

		self.label  = QLabel("<b>Description:</b><p>Adds rotation animation to all tracks found in the<br> current scene</p>")

		'''Color or Bump'''
		self.options_layout = QHBoxLayout()
		self.options_layout.setContentsMargins(5,5,5,5)
		self.options_layout.setSpacing(5) #layout
		self.options_layout.setAlignment(QtCore.Qt.AlignLeft)
		self.rbt_01 = QRadioButton("Color")

		self.rbt_01.clicked.connect(lambda x = "color": self.set_channel_type(x))

		self.rbt_02 = QRadioButton("Bump")
		self.rbt_02.clicked.connect(lambda x = "normal": self.set_channel_type(x))
		self.rbt_02.setChecked(1)
		# self.rbt_02.setStyleSheet("QRadioButton::indicator{background-color: #fea;}")
		self.options_layout.addWidget(self.rbt_01)
		self.options_layout.addWidget(self.rbt_02)


		self.mnl_layout = QHBoxLayout()
		self.mnl_title = QLabel("Speed (1.0 - normal speed):")
		self.mnl_editline = QLineEdit()
		self.mnl_editline.setStyleSheet("background-color: RGB(10,10,10);")
		if cmds.optionVar(exists = 'wg_mdltls_trackAnimSpeed'):
			self.mnl_editline.setText(cmds.optionVar(q = 'wg_mdltls_trackAnimSpeed'))
		else:
			self.mnl_editline.setText("0.2")
		self.mnl_editline.setInputMask("9.9")
		self.mnl_editline.returnPressed.connect(self.applySpeed)
		self.mnl_layout.addWidget(self.mnl_title)
		self.mnl_layout.addWidget(self.mnl_editline)


		self.prs_layout = QHBoxLayout()
		self.prs_label = QLabel("Presets")
		self.prs_button_01 = QPushButton("0.8")
		self.prs_button_01.clicked.connect(lambda x = "0.8": self.applySpeed(x))
		self.prs_button_05 = QPushButton("1.5")
		self.prs_button_05.clicked.connect(lambda x = "1.5": self.applySpeed(x))
		self.prs_button_10 = QPushButton("3.0")
		self.prs_button_10.clicked.connect(lambda x = "3.0": self.applySpeed(x))
		self.prs_button_15 = QPushButton("1.5")
		self.prs_button_15.clicked.connect(lambda x = "1.5": self.applySpeed(x))
		self.prs_button_20 = QPushButton("2.0")
		self.prs_button_20.clicked.connect(lambda x = "2.0": self.applySpeed(x))
		self.prs_layout.addWidget(self.prs_label)
		self.prs_layout.addWidget(self.prs_button_01)
		self.prs_layout.addWidget(self.prs_button_05)
		self.prs_layout.addWidget(self.prs_button_10)
		# self.prs_layout.addWidget(self.prs_button_15)
		# self.prs_layout.addWidget(self.prs_button_20)


		self.extr_layout = QHBoxLayout()
		self.extr_buttonA = QPushButton("Play")
		self.extr_buttonB = QPushButton("Stop")
		self.extr_layout.addWidget(self.extr_buttonA)
		self.extr_layout.addWidget(self.extr_buttonB)

		self.mainLayout.addWidget(self.label)
		self.mainLayout.addLayout(self.options_layout)
		self.mainLayout.addLayout(self.mnl_layout)
		self.mainLayout.addLayout(self.prs_layout)
		# self.mainLayout.addLayout(self.extr_layout)

		return self.mainLayout

	def set_channel_type(self, ch_type = None):
		if ch_type:
			cmds.optionVar(sv=("wg_mdltls_trackAnimChannel", str(ch_type)))
		if cmds.play(q=1, state=1) == 1:
			if ch_type == "color":
				self.runAction(update = 1, channel = "color")
			else:
				self.runAction(update = 1)

	def applySpeed(self, speed = None):

		if not speed:
			speed = self.mnl_editline.text()
		else:
			self.mnl_editline.setText(speed)
		cmds.optionVar(sv=("wg_mdltls_trackAnimSpeed", str(self.mnl_editline.text())))

		if cmds.play(q=1, state=1) == 1:
			self.runAction(update = 1)

	def get_track_list(self):

		track_list = cmds.ls('track_L', 'track_R', l= 1, type = 'transform')
		return track_list

	def get_track_list_shape(self):

		track_list_shape = cmds.listRelatives(self.get_track_list(), c=1, f=1)
		return track_list_shape

	def getWheelsList(self):
		wheels = cmds.ls('w_*', 'wd_*', l= 1, type = 'transform')
		return wheels

	def main(self, update = 0, channel = None):

		print('RUNING MAN', channel)
		if channel == None:
			if cmds.optionVar(exists = 'wg_mdltls_trackAnimChannel'):
				channel = cmds.optionVar(q = 'wg_mdltls_trackAnimChannel')
			else:
				channel = "normal"

		#playback speed option - 24fps
		cmds.playbackOptions(ps =1)

		'''
		track selection valid
		'''
		selection = cmds.ls(sl=1,l=1)

		track_list_shape = cmds.listRelatives(cmds.ls(sl=1,l=1), c=1, f=1)
		if not track_list_shape:
			track_list_shape = self.get_track_list_shape()

		if not track_list_shape: #if still no wheels
			cmds.inViewMessage(amg= '<hl>Tracks were not found. Please select tracks manually.</hl>' , pos = 'midCenter', fade = True, fot = 1000)
			return

		'''
		if wheels are animated - stop wheels
		'''
		wheels = self.getWheelsList()
		if cmds.keyframe(wheels, q=1, keyframeCount =1):

			cmds.play(state = 0)

			cmds.cutKey(wheels, s=True)
			for i in wheels:
				cmds.setAttr(i + ".rotateX", 0)

			cmds.playbackOptions(e=1, ast = 1)
			cmds.playbackOptions(e=1, aet = 48)
			cmds.playbackOptions(min = 1, max = 24)
			cmds.currentTime(1)



		'''
		tracks  place2dTexture assign
		'''
		for ii in track_list_shape:
			place2dTextureColor = scene_u.get_color_Place2dTexture(ii)
			place2dTextureBump = scene_u.get_bump_Place2dTexture(ii)


		speed = float(self.mnl_editline.text())

		#START animation for one channel
		if cmds.play(q=1, state=1) == 0:

			readyForAnimation = False

			place2dTexture = None
			if channel == "color":
				place2dTexture = place2dTextureColor
				if not place2dTexture:
					cmds.inViewMessage(amg= '<hl>Assign color texture for moving control.</hl>' , pos = 'midCenter', fade = True, fot = 1000)
					#continue
					return
			elif channel == "normal":
				place2dTexture = place2dTextureBump
				#print '2D ', place2dTexture
				if not place2dTexture:
					cmds.inViewMessage(amg= '<hl>Assign normal texture for moving control.</hl>' , pos = 'midCenter', fade = True, fot = 1000)
					#continue
					return
			if place2dTexture:
				#print '2d node exist ', place2dTexture

				readyForAnimation = True
				cmds.setKeyframe( place2dTexture, time = 1, value = 0, at = "offsetV" )
				cmds.setKeyframe( place2dTexture, time = 24, value = speed, at = "offsetV" )
				cmds.keyTangent(place2dTexture, itt="linear", ott="linear")
				cmds.setInfinity(place2dTexture, poi = "cycleRelative")

			if readyForAnimation:
				cmds.playbackOptions(e=1, ast = 1)
				cmds.playbackOptions(e=1, aet = 192)
				cmds.playbackOptions(min = 1, max = 192)
				cmds.play(forward=1)
				cmds.inViewMessage(amg= '<hl>Track are animated</hl>' , pos = 'topLeft', fade = True, fot = 1000)


		#stop animation for all channels
		elif cmds.play(q=1, state=1) == 1:


			if place2dTextureColor:
				cmds.cutKey(place2dTextureColor, s=True)
				cmds.setAttr(place2dTextureColor + ".offsetV", 0)

			if place2dTextureBump:
				cmds.cutKey(place2dTextureBump, s=True)
				cmds.setAttr(place2dTextureBump + ".offsetV", 0)

			cmds.currentTime(1)
			cmds.playbackOptions(e=1, ast = 1)
			cmds.playbackOptions(e=1, aet = 48)
			cmds.playbackOptions(min = 1, max = 24)
			#cmds.inViewMessage(amg= '<hl>Tracks animation has been stopped1</hl>' , pos = 'topLeft', fade = True, fot = 1000)
			cmds.play(state = 0)

		if update == 1:
			print('WTF')

			place2dTexture = None
			if channel == "color":
				place2dTexture = place2dTextureColor

			elif channel == "normal":
				place2dTexture = place2dTextureBump

			if place2dTexture:
				cmds.setKeyframe( place2dTexture, time = 1, value = 0, at = "offsetV" )
				cmds.setKeyframe( place2dTexture, time = 24, value = speed, at = "offsetV" )
				cmds.keyTangent(place2dTexture, itt="linear", ott="linear")
				cmds.setInfinity(place2dTexture, poi = "cycleRelative")

				cmds.playbackOptions(e=1, ast = 1)
				cmds.playbackOptions(e=1, aet = 192)
				cmds.playbackOptions(min = 1, max = 192)
				cmds.play(forward=1)
			else:
				#print 'Check assign texture'
				cmds.inViewMessage(amg= '<hl>No texture assigned </hl>' , pos = 'topLeft', fade = True, fot = 1000)
				cmds.currentTime(1)
				cmds.playbackOptions(e=1, ast = 1)
				cmds.playbackOptions(e=1, aet = 48)
				cmds.playbackOptions(min = 1, max = 24)
				cmds.inViewMessage(amg= '<hl>Tracks animation has been stopped</hl>' , pos = 'topLeft', fade = True, fot = 1000)
				cmds.play(state = 0)

			#if place2dTexture:
			#	cmds.playbackOptions(e=1, ast = 1)
			#	cmds.playbackOptions(e=1, aet = 192)
			#	cmds.playbackOptions(min = 1, max = 192)
			#	cmds.play(forward=1)
			#else:
			#	cmds.currentTime(1)
			#	cmds.playbackOptions(e=1, ast = 1)
			#	cmds.playbackOptions(e=1, aet = 48)
			#	cmds.playbackOptions(min = 1, max = 24)
			#	cmds.inViewMessage(amg= '<hl>Tracks animation has been stopped</hl>' , pos = 'topLeft', fade = True, fot = 1000)
			#	cmds.play(state = 0)






