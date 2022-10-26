import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import os, re, math
import difflib


description = "Expose all the geometry in the scene by moving them out of their original position"
buttonType = "opt"
beautyName = "ExposeGeo"
iconName = "Expose Geometry"
RANGE_SLIDER = 100
OFFSET_COEFF = 0.01
MAX_RANGE = 10.0

class Utils():
	def __init__(self):
		print('utils')


	@classmethod
	def removeList(cls, fromList, thisList):
		resultList =  [n for n in fromList if n not in thisList]
		resultList = list(resultList)
		return resultList


	@classmethod
	def diffrent_names(cls, first, second):
		normalized1 = first.lower()
		normalized2 = second.lower()
		matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
		return matcher.ratio()


	@classmethod
	def lods_list(cls, parent = None):
		'''not selected'''
		lods = cmds.ls('lod*', tr = True)
		if parent:
			children = cmds.listRelatives(parent, t = 'transform', f = True)
			lods = cmds.ls(children, 'lod*', tr = True)


	@classmethod
	def file_name(cls):
		sceneName = cmds.file( q=True, sn=1, shn=1)
		name = os.path.splitext(sceneName)[0]
		return name


	@classmethod
	def size_bounding_box(cls, obj):

		#bbx = cmds.xform(obj, q=True, bb=True, ws=True) # world space
		value = [0, 0, 0]
		value[0] = cmds.getAttr(obj + ".boundingBoxSizeX")
		value[2] = cmds.getAttr(obj + ".boundingBoxSizeZ")

		return value


	@classmethod
	def center_bounding_box(cls, obj):

		bbx = cmds.xform(obj, q=True, bb=True, ws=True) # world space
		value = [0, 0, 0]
		value[0] = (bbx[3] + bbx[0])/2    #width x
		value[1] = (bbx[4] + bbx[1])/2   #hight y
		value[2] = (bbx[5] + bbx[2])/2   #depth z

		# value[0] = cmds.getAttr(obj + ".boundingBoxCenterX")
		# value[2] = cmds.getAttr(obj + ".boundingBoxCenterZ")

		return value


class ToolOptions(QWidget):

	def __init__(self, parent = None):

		super(ToolOptions, self).__init__(parent)

		self.assetList = []
		self.lodList = []
		self.havokList = []

		#populate assets and lods  [asset1, asset2, asset3]  [ [lod0,lod1,lod2] [lod0, lod1, lod2] ]
		self.setLayout(self.createUI())
		self.collect_data()


	def createUI(self):

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setContentsMargins(5,5,5,5)
		self.mainLayout.setSpacing(10) #layout
		self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
		self.mainLayout.setObjectName("expose_geometry")

		'''description'''
		self.label  = QLabel("<b>Description:</b><p>Moves geometry by assets and lods to make them visible apart from other assets/lods</p><br>")
		self.label.setWordWrap(1)

		'''axis layout'''
		self.axisLayout = QHBoxLayout()
		self.axisLabel = QLabel("Slide axis")
		self.group_btn = QButtonGroup()
		self.positiveX = QRadioButton("X")
		self.positiveX.setMaximumWidth(40)
		self.positiveX.setChecked(True)
		self.positiveX.toggled.connect(self.axis_changed)
		self.group_btn.addButton(self.positiveX)
		self.positiveZ = QRadioButton("Z")
		self.positiveZ.setMaximumWidth(40)
		self.positiveZ.toggled.connect(self.axis_changed)
		self.group_btn.addButton(self.positiveZ)

		self.axisLayout.addWidget(self.axisLabel, Qt.AlignLeft)
		self.axisLayout.addWidget(self.positiveX, Qt.AlignLeft)
		self.axisLayout.addWidget(self.positiveZ, Qt.AlignLeft)

		'''assets slider'''
		self.assets_layout = QHBoxLayout()
		self.assets_label = QLabel("Assets:")
		self.assets_label.setMinimumWidth(40)
		self.assets_label.setMaximumWidth(40)
		self.assets_slider = QSlider(QtCore.Qt.Horizontal)
		self.assets_slider.setObjectName("assetsSlider")
		self.assets_slider.setMinimum(0)
		self.assets_slider.setMaximum(RANGE_SLIDER)
		self.assets_slider.setValue(0)
		self.assets_slider.valueChanged.connect(lambda:self.assets_slider_changed())
		self.assets_slider.setStyleSheet("background-color: #000;")

		self.spinBox_assets = QDoubleSpinBox()
		self.spinBox_assets.setRange(1.0, MAX_RANGE)
		self.spinBox_assets.setSingleStep(0.1)
		self.spinBox_assets.setValue(1.0)
		self.spinBox_assets.setFixedWidth(60)
		self.spinBox_assets.valueChanged.connect(lambda:self.assets_slider_changed())

		self.assets_layout.addWidget(self.assets_label)
		self.assets_layout.addWidget(self.assets_slider)
		self.assets_layout.addWidget(self.spinBox_assets)

		'''havok slider'''
		self.havok_layout = QHBoxLayout()
		self.havok_label = QLabel("Havok:")
		self.havok_label.setMinimumWidth(40)
		self.havok_label.setMaximumWidth(40)
		self.havok_slider = QSlider(QtCore.Qt.Horizontal)
		self.havok_slider.setObjectName("havokSlider")
		self.havok_slider.setMinimum(0)
		self.havok_slider.setMaximum(RANGE_SLIDER)
		self.havok_slider.setValue(0)
		self.havok_slider.valueChanged.connect(lambda:self.havok_slider_changed())
		self.havok_slider.setStyleSheet("background-color: #000;")

		self.spinBox_havok = QDoubleSpinBox()
		self.spinBox_havok.setRange(1.0, MAX_RANGE)
		self.spinBox_havok.setSingleStep(0.1)
		self.spinBox_havok.setValue(1.0)
		self.spinBox_havok.setFixedWidth(60)
		self.spinBox_havok.valueChanged.connect(lambda:self.havok_slider_changed())

		self.havok_layout.addWidget(self.havok_label)
		self.havok_layout.addWidget(self.havok_slider)
		self.havok_layout.addWidget(self.spinBox_havok)

		'''lods slider'''
		self.lods_layout = QHBoxLayout()
		self.lods_label = QLabel("Lods:")
		self.lods_label.setMinimumWidth(40)
		self.lods_label.setMaximumWidth(40)
		self.lods_slider = QSlider(QtCore.Qt.Horizontal)
		self.lods_slider.setObjectName("assetsSlider")
		self.lods_slider.setMinimum(0)
		self.lods_slider.setMaximum(RANGE_SLIDER)
		self.lods_slider.setValue(0)
		self.lods_slider.valueChanged.connect(self.lods_slider_changed)
		self.lods_slider.setStyleSheet("background-color: #000;")

		self.spinBox_lods = QDoubleSpinBox()
		self.spinBox_lods.setRange(1.0, MAX_RANGE)
		self.spinBox_lods.setSingleStep(0.1)
		self.spinBox_lods.setValue(1.0)
		self.spinBox_lods.setFixedWidth(60)
		self.spinBox_lods.valueChanged.connect(self.lods_slider_changed)

		self.lods_layout.addWidget(self.lods_label)
		self.lods_layout.addWidget(self.lods_slider)
		self.lods_layout.addWidget(self.spinBox_lods)

		'''options'''
		self.opt_layout = QHBoxLayout()
		self.opt_checkbox_normal = QCheckBox("Normal")
		self.opt_checkbox_normal.clicked.connect(self.toggle_normal)
		self.opt_checkbox_normal.setChecked(1)
		self.opt_checkbox_normal.setMinimumWidth(60)
		self.opt_checkbox_normal.setMaximumWidth(60)
		self.opt_checkbox_crash = QCheckBox("Damage")
		self.opt_checkbox_crash.clicked.connect(self.toggle_crash)
		self.opt_checkbox_crash.setChecked(1)
		self.opt_layout.addWidget(self.opt_checkbox_normal)
		self.opt_layout.addWidget(self.opt_checkbox_crash)

		'''button'''
		self.btn_reset  = QPushButton("Reset")
		self.btn_reset.clicked.connect(self.reset)

		'''main layout'''
		self.mainLayout.addWidget(self.label)
		self.mainLayout.addLayout(self.axisLayout)
		self.mainLayout.addLayout(self.assets_layout)
		self.mainLayout.addLayout(self.lods_layout)
		self.mainLayout.addLayout(self.havok_layout)
		self.mainLayout.addLayout(self.opt_layout)
		self.mainLayout.addWidget(self.btn_reset)

		return self.mainLayout


	def script_job_selections(self):
		script_job = cmds.scriptJob( e= ["SelectionChanged", self.collect_data], p = "expose_geometry")


	def dag_objects(self):
		camera = cmds.listRelatives(cmds.ls(ca=1), p=1)
		dags = cmds.ls(assemblies=1)
		dags = Utils.removeList(dags, camera)
		return dags


	def collect_data(self):
		self.assetList = []
		self.lodList = []
		self.havokList = []
		# sceneName = Utils.file_name()
		# sceneName = cmds.file( q=True, sn=1, shn=1)

		topLevelDAG = self.dag_objects()
		for dag in topLevelDAG:
			if '__n' in dag:
				meshes = cmds.listRelatives(dag, ad=1, f=1, type = 'mesh')
				meshes = cmds.listRelatives(meshes, p=1, f=1, type = 'transform')
				for mesh in meshes:
					attr = []
					attr.append(mesh)
					bbx = Utils.size_bounding_box(mesh)
					center = Utils.center_bounding_box(mesh)
					area_xz = bbx[0]*bbx[2]
					pivot = cmds.xform(mesh, q=1, rp=1, ws=True)
					attr.extend([bbx[0], bbx[2], center, area_xz, pivot])
					self.havokList.append(attr)
				self.havok_sorted_x = sorted(self.havokList, key=lambda x: x[1])
				self.havok_sorted_z = sorted(self.havokList, key=lambda x: x[2])
				self.havok_sorted = sorted(self.havokList, key=lambda x: x[4])
				#print 'HAVOK ', self.havok_sorted
						#return
			#if Utils.diffrent_names(sceneName, dag) > 0.8:
			self.assetList.append(dag)
			i_lods = cmds.ls(cmds.listRelatives(dag, c=1, f=1), l=1)
			lod_list = []
			for ii in i_lods:
				if "lod" in ii:
					lod_list.append(ii)
			if lod_list:
				self.lodList.append(lod_list)


	def axis_changed(self):
		self.assets_slider_changed()
		self.lods_slider_changed()
		self.havok_slider_changed()


	def lods_slider_changed(self):

		if self.lodList:
			axis = ".tz"
			width = 2
			anti_axis = '.tx'
			coeff = self.spinBox_lods.value()

			if self.positiveZ.isChecked():
				axis = ".tx"
				width = 0
				anti_axis = '.tz'

			for lod in self.lodList:
				if len(lod) > 1:
					for indx in range(1, len(lod)):
						bbx_ = Utils.size_bounding_box(lod[indx-1])
						bbx = Utils.size_bounding_box(lod[indx])
						pos = cmds.getAttr(lod[indx-1] + axis)
						asset_position = float(self.lods_slider.value())*OFFSET_COEFF*(bbx[width]+bbx_[width])*coeff + pos
						cmds.setAttr(lod[indx] + axis, asset_position)
						cmds.setAttr(lod[indx] + anti_axis, 0)

		else:
			return


	def assets_slider_changed(self):
		if len(self.assetList) > 1:

			axis = ".tx"
			width = 0
			anti_axis = '.tz'
			coeff = self.spinBox_assets.value()
			if self.positiveZ.isChecked():
				axis = ".tz"
				width = 2
				anti_axis = '.tx'

			for indx in range(1, len(self.assetList)):
				bbx_ = Utils.size_bounding_box(self.assetList[indx-1])
				bbx = Utils.size_bounding_box(self.assetList[indx])
				pos = cmds.getAttr(self.assetList[indx-1] + axis)
				asset_position = float(self.assets_slider.value())*OFFSET_COEFF*(bbx[width]+bbx_[width])*coeff + pos
				cmds.setAttr(self.assetList[indx] + axis, asset_position)
				cmds.setAttr(self.assetList[indx] + anti_axis, 0)
		else:
			return


	def havok_slider_changed(self):

		if len(self.havokList) > 1:
			axis = ".tx"
			anti_axis = '.tz'
			sort_list = self.havok_sorted
			coeff = self.spinBox_havok.value()

			num = int(math.ceil(math.sqrt(len(sort_list))))

			i = 1
			for y in range(num):
				for x in range(num):
					if i < len(sort_list):
						offcet_position_x = sort_list[i][5][0] - sort_list[i][3][0]
						offcet_position_z = sort_list[i][5][2] - sort_list[i][3][2]
						cmds.setAttr(sort_list[i][0] + ".inheritsTransform", 0)
						cmds.setAttr(sort_list[i][0] + axis, y*self.havok_slider.value()*OFFSET_COEFF*coeff + offcet_position_x)
						cmds.setAttr(sort_list[i][0] + anti_axis, x*self.havok_slider.value()*OFFSET_COEFF*coeff + offcet_position_z)
						i = i + 1
		else:
			return


	def reset(self):

		self.collect_data()


		self.assets_slider.setValue(0)
		self.lods_slider.setValue(0)
		self.havok_slider.setValue(0)

		if self.assetList:
			for i in self.assetList:
				cmds.setAttr(i + ".tx", 0)
				cmds.setAttr(i + ".tz", 0)

		if self.lodList:
			for i in self.lodList:
				for j in i:
					cmds.setAttr(j + ".tx", 0)
					cmds.setAttr(j + ".tz", 0)

		if self.havokList:
			for i in self.havokList:
				cmds.setAttr(i[0] + ".tx", 0)
				cmds.setAttr(i[0] + ".tz", 0)
				cmds.setAttr(i[0] + ".inheritsTransform", 1)

		self.collect_data()


	def toggle_normal(self):
		for i in self.lodList:
			for lod in i:
				children = cmds.listRelatives(lod, c=1, pa=1)
				for j in children:
					name = j.split("|")[-1]
					if name[0] == "n":
						state = cmds.getAttr(j + ".v")
						cmds.setAttr(j + ".v", (not state))


	def toggle_crash(self):
		for i in self.lodList:
			for lod in i:
				children = cmds.listRelatives(lod, c=1, pa=1)
				for j in children:
					name = j.split("|")[-1]
					if name[0] == "d":
						state = cmds.getAttr(j + ".v")
						cmds.setAttr(j + ".v", (not state))


	def main(self):

		cmds.inViewMessage(amg= '<hl>Please open Options to apply Expose Geometry</hl>' , pos = 'midCenter', fade = True, fot = 1000)
