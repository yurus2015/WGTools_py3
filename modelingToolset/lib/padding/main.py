import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaRender as OpenMayaRender

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import os, time
import struct
from . import opencv as Ocv
import importlib

description = "Use this checker to make sure a model's uvs are created correctly"
buttonType = "opt"
beautyName = "UV Checker"
iconName = "UV Checker"

DIMENSION = [512, 1024, 2048, 4096]
PADDINGVALUE = 4
SHELLCOLOR = (255, 255, 255)
PADDINGCOLOR = (0, 255, 0)
INTERSECTIONCOLOR = (255, 0, 255)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPDIR = cmds.internalVar(utd=True)

class Utils(object):
	@classmethod
	def load_option_var(cls):

		options = [2048, 4, cls.rgb2hex((0,255,0)), cls.rgb2hex((255,0,255))]
		print('Default options ', options)

		if cmds.optionVar( exists='padding_resolution' ):
			options[0] = cmds.optionVar( q='padding_resolution' )
		else:
			cmds.optionVar( iv=('padding_resolution', options[0]))

		if cmds.optionVar( exists='padding_offset' ):
			options[1] = cmds.optionVar( q='padding_offset' )
		else:
			cmds.optionVar( iv=('padding_offset', options[1]))

		if cmds.optionVar( exists='padding_line_color' ):
			options[2] = cmds.optionVar( q='padding_line_color' )
		else:
			cmds.optionVar( sv=('padding_line_color', options[2]))

		if cmds.optionVar( exists='padding_intersect_color' ):
			options[3] = cmds.optionVar( q='padding_intersect_color' )
		else:
			cmds.optionVar( sv=('padding_intersect_color', options[3]))

		return options


	@classmethod
	def save_option_int(cls, option, value):
		cmds.optionVar(iv=(option, int(value)))


	@classmethod
	def save_option_str(cls, option, value):
		cmds.optionVar(sv=(option, str(value)))


	@classmethod
	def hex2rgb(cls, hex):
		return struct.unpack('BBB', hex.decode('hex'))


	@classmethod
	def rgb2hex(cls, rgb):
		return struct.pack('BBB',*rgb).encode('hex')


	@classmethod
	def color_picker(cls, button, option):
		values = None
		cmds.colorEditor()
		if cmds.colorEditor(query=True, result=True):
			values = cmds.colorEditor(query=True, rgb=True)
			values = [x * 255 for x in values]
			print('RGB = ' + str(values))

			hex_color = cls.rgb2hex(values)
			button.setStyleSheet("background-color:#" + hex_color)
			cls.save_option_str(option, hex_color)

		else:
			print('Editor was dismissed')

		return values


	@classmethod
	def selected(cls):
		meshes = cmds.filterExpand(sm = 12, fp = 1)
		if meshes:
			return meshes
		else:
			cmds.confirmDialog( title='Select meshes', message='Select poligonal mesh', button=['Yes'], defaultButton='Yes' )
			return


	@classmethod
	def create_padding_node(cls):
		check_node = cmds.ls('padding_file')
		check_node2d = cmds.ls('padding_2d')

		if check_node:
			file = check_node[0]
		else:
			file = cmds.shadingNode('file', asTexture=True, name = "padding_file")

		if check_node2d:
			node_2d = check_node2d[0]
		else:
			node_2d = cmds.shadingNode('place2dTexture', asUtility =1, n = 'padding_2d')
			cmds.setAttr(node_2d + ".repeatUV.repeatV", 1)

		cmds.defaultNavigation(connectToExisting=1, source = node_2d, destination = file)
		return file


	@classmethod
	def take_shaders(cls, mesh):
		shader_engines = cmds.listConnections(cmds.listHistory(mesh), type = 'shadingEngine')
		materials = cmds.ls(cmds.listConnections(shader_engines), materials= True)

		return materials


	@classmethod
	def take_texture_file(cls, materials):
		texture = []
		for mat in materials:
			texture_node = cmds.listConnections(mat + ".color", type="file")
			if texture_node:
				texture.append(texture_node[0])
			else:
				texture.append(None)
		return texture


	@classmethod
	def connect_texture_file(cls, texture, padding_node):
		texture_path = os.path.join(TEMPDIR, texture)
		cmds.setAttr(padding_node + ".fileTextureName", texture_path, type = "string")


	@classmethod
	def connect_texture_materials(cls, textures, materials, padding_node):

		for i in range (len(materials)):
			if textures[i] == None:
				cmds.connectAttr(padding_node + ".outColor", materials[i] + ".color", force = 1)

			elif textures[i] != padding_node:
				cmds.connectAttr(padding_node + ".outColor", textures[i] + ".colorGain", force = 1)
				# cmds.connectAttr(padding_node + ".outColor", textures[i] + ".colorOffset", force = 1)
				cmds.setAttr(textures[i] + ".disableFileLoad", 1)



	@classmethod
	def delete_padding_node(cls):
		check_node = cmds.ls('padding_file')
		check_node2d = cmds.ls('padding_2d')
		check_node.extend(check_node2d)
		try:
			cmds.delete(check_node)
		except:
			pass
		all_file_nodes = cmds.ls(type = 'file')
		for f in all_file_nodes:
			cmds.setAttr(f + ".disableFileLoad", 0)


	@classmethod
	def toggle_padding_textures(cls):
		check_node = cmds.ls('padding_file')
		if check_node:
			for f in check_node:
				value_visible = cmds.getAttr(f + ".disableFileLoad")
				cmds.setAttr(f + ".disableFileLoad", not value_visible)
				# print 'VALUE: ', value_visible
				if value_visible:
					# print 'ON SOLO', cmds.soloMaterial(f, q=1)
					#soloMaterial -node "padding_file";
					cmds.soloMaterial( node=str(f))
				#find real connect texrure
				real_texture = cmds.listConnections( f, d=True, s=False, t = 'file' )
				if real_texture:
					cmds.setAttr(real_texture[0] + ".disableFileLoad", value_visible)
					if not value_visible:
						cmds.soloMaterial( node=real_texture[0])




	@classmethod
	def create_material(cls, texture):
		selected = cls.selected()
		if not selected:
			return

		texWinName = cmds.getPanel(sty='polyTexturePlacementPanel')
		textures = cmds.textureWindow(texWinName[0], q=True, txn=True )

		padding_node = cls.create_padding_node()
		assigned_shaders = cls.take_shaders(selected)
		texture_nodes = cls.take_texture_file(assigned_shaders)
		cls.connect_texture_materials(texture_nodes, assigned_shaders, padding_node)
		cls.connect_texture_file(texture, padding_node)

		textures = cmds.textureWindow(texWinName[0], q=True, txn=True )
		if textures:
			for i in range(len(textures)):
				print('check ', textures[i])
				if textures[i] == texture:
					print('find', (textures[i]))
					mel.eval('textureWindowSelectTexture ' + str(i) +' polyTexturePlacementPanel1;uvTbUpdateTextureItems polyTexturePlacementPanel1;')
					cmds.textureWindow(texWinName[0], e=1, displayCheckered = 1)
					cmds.textureWindow(texWinName[0], e=1, displayCheckered = 0)# -edit  -checkerColorMode 0
					break

		cmds.select(selected)


class ToolOptions(QWidget):

	def __init__(self, parent = None):

		super(ToolOptions, self).__init__(parent)
		self.options = Utils.load_option_var()
		print('Options ', self.options)
		self.setLayout(self.createUI())


	def createUI(self):

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setContentsMargins(5,5,5,5)
		self.mainLayout.setSpacing(5) #layout
		self.mainLayout.setAlignment(QtCore.Qt.AlignLeft)
		self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

		'''texture size'''
		self.dimention_layout = QHBoxLayout()
		self.buttons_group = QButtonGroup()
		for size in DIMENSION:
			radio = QRadioButton(str(size))
			if size == self.options[0]:
				radio.setChecked(1)
			radio.clicked.connect(self.sender_value)
			self.dimention_layout.addWidget(radio)

		self.padding_layout = QHBoxLayout()
		self.padding_layout.setAlignment(QtCore.Qt.AlignLeft)
		self.padding_value = QSpinBox()
		self.padding_value.setRange(1, 8)
		self.padding_value.setSingleStep(1)
		self.padding_value.setValue(self.options[1])
		self.padding_value.setFixedWidth(60)
		self.padding_value.valueChanged.connect(lambda:Utils.save_option_int('padding_offset', self.padding_value.value()))
		self.padding_value_label = QLabel("Padding size in pixel")
		self.padding_layout.addWidget(self.padding_value)
		self.padding_layout.addWidget(self.padding_value_label)

		self.color_layout = QVBoxLayout()

		# self.padding_color_layout = QHBoxLayout()
		# self.color_padding_button = QPushButton()
		# self.color_padding_button.setStyleSheet("background-color:#" + self.options[2])
		# self.color_padding_button.setFixedSize(60,20)
		# self.color_padding_button.clicked.connect(lambda: Utils.color_picker(self.color_padding_button, 'padding_line_color'))
		# self.color_padding_label = QLabel("Color padding")
		# self.padding_color_layout.addWidget(self.color_padding_button)
		# self.padding_color_layout.addWidget(self.color_padding_label)

		self.intersection_color_layout = QHBoxLayout()
		self.color_intersection_button = QPushButton()
		self.color_intersection_button.setStyleSheet("background-color:#" + self.options[3])
		self.color_intersection_button.setFixedSize(60,20)
		self.color_intersection_button.clicked.connect(lambda: Utils.color_picker(self.color_intersection_button, 'padding_intersect_color'))
		self.color_intersection_label = QLabel("Color intersection")
		self.intersection_color_layout.addWidget(self.color_intersection_button)
		self.intersection_color_layout.addWidget(self.color_intersection_label)


		# self.color_layout.addLayout(self.padding_color_layout)
		self.color_layout.addLayout(self.intersection_color_layout)

		# self.icon_layout = QHBoxLayout()
		# self.icon_layout.setAlignment(QtCore.Qt.AlignLeft)

		# self.label_padding = QToolButton()
		# self.label_padding.setFixedSize(50,50)
		# self.icon_padding = QIcon(QPixmap(os.path.join(CURRENT_DIR, "icons/padding.svg")).scaled(50,50, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
		# self.label_padding.setIcon(self.icon_padding)
		# self.label_padding.setIconSize(QSize(50, 50))
		# self.label_padding.clicked.connect(lambda: Utils.create_material("padding.jpg"))

		# self.label_intersection = QToolButton()
		# self.label_intersection.setFixedSize(50,50)
		# self.icon_intersection = QIcon(QPixmap(os.path.join(CURRENT_DIR, "icons/intrsct.svg")).scaled(50,50, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
		# self.label_intersection.setIcon(self.icon_intersection)
		# self.label_intersection.setIconSize(QSize(50, 50))
		# self.label_intersection.clicked.connect(lambda: Utils.create_material("intersection.jpg"))

		# self.label_plus = QToolButton()
		# self.label_plus.setFixedSize(50,50)
		# self.icon_plus = QIcon(QPixmap(os.path.join(CURRENT_DIR, "icons/padIntsct.svg")))
		# self.label_plus.setIcon(self.icon_plus)
		# self.label_plus.setIconSize(QSize(50, 50))
		# self.label_plus.clicked.connect(lambda:Utils.create_material("padintr.jpg"))

		# self.icon_layout.addWidget(self.label_padding)
		# self.icon_layout.addWidget(self.label_intersection)
		# self.icon_layout.addWidget(self.label_plus)

		self.command_layout = QHBoxLayout()
		self.command_button = QPushButton("Calculate")
		self.command_button.clicked.connect(self.compute_command)
		self.command_layout.addWidget(self.command_button)

		self.reset_layout = QHBoxLayout()
		self.reset_button = QPushButton("Toggle textures")
		self.reset_button.clicked.connect(Utils.toggle_padding_textures)
		self.reset_layout.addWidget(self.reset_button)

		self.mainLayout.addLayout(self.dimention_layout)
		self.mainLayout.addLayout(self.padding_layout)
		self.mainLayout.addLayout(self.color_layout)
		self.mainLayout.addLayout(self.command_layout)
		# self.mainLayout.addLayout(self.icon_layout)
		self.mainLayout.addLayout(self.reset_layout)

		return self.mainLayout


	def sender_value(self):
		button = self.sender()
		Utils.save_option_int('padding_resolution', button.text())


	def compute_command(self):
		importlib.reload(Ocv)
		Utils.delete_padding_node()
		dimention = cmds.optionVar( q='padding_resolution' )
		padding = cmds.optionVar( q='padding_offset' )*2
		padding_color = Utils.hex2rgb(str(cmds.optionVar( q='padding_line_color' )))
		intersection_color = Utils.hex2rgb(str(cmds.optionVar( q='padding_intersect_color' )))
		Ocv.main(dimention, padding, padding_color, intersection_color)
		Utils.create_material("intersection.jpg")


	def main(self):
		cmds.inViewMessage(amg= '<hl>Please open options to apply checker</hl>' , pos = 'topLeft', fade = True, fot = 1000)

