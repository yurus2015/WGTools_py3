import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from maya.mel import eval as meval
import xml.etree.ElementTree as ET
#import xmlEdit as xml
import os
import posixpath
import time

MINIMUM_WIDTH = 180
MAXIMUM_HEIGHT = 18

def getWindowPointer():
		#Get and return Maya Main window pointer
		main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
		return wrapInstance(long(main_window_ptr), QWidget)

class MainTrunkSelector(QObject):
	def __init__(self):
		super(MainTrunkSelector, self).__init__()
		self.setObjectName('MainTrunkSelector')

		#self.getWindowPointer()

		self.root_window = getWindowPointer()


	# def getWindowPointer(self):
	# 	#Get and return Maya Main window pointer
	# 	main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
	# 	self.root_window = wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


	def getWorkspacePointer(self):
		self.selector_layout = self.root_window.findChildren(QHBoxLayout)
		for layout in self.selector_layout:
			if layout.objectName() == 'workspaceSelectorLayout':
				print layout.objectName()
				return layout


	def editDefaultUI(self, parent):
		widget = TrunkSelectorWidget()
		parent.insertWidget(0, widget)

		self.empty_widget = QLabel()
		self.empty_widget2 = QLabel()

		parent.insertWidget(1, self.empty_widget)
		parent.insertWidget(2, self.empty_widget2)


	def main(self):
		selector_layout = self.getWorkspacePointer()
		self.editDefaultUI(selector_layout)
		meval('updateWorkspacesList();')


class TrunkSelectorWidget(QWidget):
	def __init__(self):
		super(TrunkSelectorWidget, self).__init__()
		self.setObjectName('Trunk_Selector_Widget')
		self.initUI()


	def initUI(self):
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(0,0,0,0)
		self.main_layout.setSpacing(0)

		self.label = QLabel('Current Trunk: ')

		self.trunk_line = QLineEdit()
		self.trunk_line.setEnabled(False)
		self.trunk_line.setFixedHeight(MAXIMUM_HEIGHT)
		self.trunk_line.setMinimumWidth (MINIMUM_WIDTH)
		self.trunk_line.setStyleSheet("""color: rgb(180,180,180);""")

		self.trunk_menu = QMenu()
		self.trunk_menu.setMinimumWidth(MINIMUM_WIDTH)

		self.base_action = TrunkMenuAction(self.trunk_menu, '>>>ADD NEW TRUNK<<<', options=False)
		self.base_action.triggered.connect(self.dir_browser)

		self.trunk_menu.addAction(self.base_action)

		#add from xml
		self.adding_paths()

		self.trunk_button = QLabel()
		self.trunk_button.setPixmap(os.path.join(Utility.getCurrentDir(), 'source', 'arrow.svg'))
		self.trunk_button.mousePressEvent = self.open_menu

		#add visual plugin path
		base_path = Utility.get_default_plugin()

		self.main_layout.addWidget(self.label)
		self.main_layout.addWidget(self.trunk_line)
		self.main_layout.addWidget(self.trunk_button)




	# def addMenuActions(self):
	# 	delete = QAction(self)
	# 	delete.setText("remove")
	# 	delete.triggered.connect(self.remove_trunk)
	# 	self.addAction(delete)


	# def remove_trunk(self):
	# 	print("Removing")


	# def browser_callable(self, index = 0):
	# 	if self.trunk_Combo.currentText() == '>>>ADD NEW TRUNK<<<':
	# 		print('some_callable')
	# 		self.trunk_Combo.setCurrentIndex(0)
	# 		self.dir_browser()
		#self.trunk_Combo.activated[0]


	#def mousePressEvent(self, QMouseEvent):
	#	if QMouseEvent.button() == Qt.LeftButton:
	#		print("Left Button Clicked")
	#		self.trunk_menu.show()
	#		#self.trunk_menu.move(self.trunk_menu.parent().mapToGlobal(QtCore.QPoint(0,0))-QtCore.QPoint(0, self.trunk_menu.height()))
	#		self.trunk_menu.exec_(self.trunk_line.mapToGlobal(QtCore.QPoint(0, MAXIMUM_HEIGHT)))
#
	#	elif QMouseEvent.button() == Qt.RightButton:
	#		print("Right Button Clicked")
	#		#self.addMenuActions()


	def dir_browser(self): #open browser to set export path
		print 'im'
		bpath = None
		try:
			bpath = cmds.fileDialog2(fm=3, dialogStyle=1)[0]
		except:
			#pass
			return

		if bpath:
			print 'Path: ', bpath
			self.options_window = OptionActionWindow(real_path = bpath, widget = self)
			self.show_start_options()

			new_action = TrunkMenuAction(self.trunk_menu, bpath, widget = self)
			new_action.triggered.connect(lambda: self.set_current_trunk(new_action))

			self.trunk_menu.insertAction(self.base_action, new_action)
			Utility.trunk_list(bpath)

			#self.trunk_line.setText(bpath)
		else:
			pass
			#cmds.confirmDialog( title='Warning', message= 'Select "vehicles" dir in your trank', button=['   OK   '], defaultButton='   OK   ')


	def set_current_trunk(self, actionName):
		#print widget
		#widget.action_name()
		self.trunk_line.setText(actionName.action_text())


	def set_short_name(self, text):
		self.trunk_line.setText(text)


	def open_menu(self, event):
		self.trunk_menu.show()
		self.trunk_menu.exec_(self.trunk_line.mapToGlobal(QtCore.QPoint(0, MAXIMUM_HEIGHT)))


	def show_start_options(self):
		self.options_window.show()
		print 'Feedback_01'


	def adding_paths(self):
		paths = Utility.trunk_list()
		if paths:
			for path in paths:
				if cmds.optionVar( exists = path ):

					self.new_action = TrunkMenuAction(self.trunk_menu, cmds.optionVar( q = path), widget = self)
					self.trunk_menu.insertAction(self.base_action, self.new_action)


	def removing_path(self, actionName):
		self.trunk_menu.removeAction(actionName)
		xml = Utility.xml_path()
		Utility.editXML(actionName.action_text(), xml, delete = True)
		Utility.delete_option_var(actionName.action_text())


class TrunkMenuAction(QWidgetAction):
	def __init__(self, parent, titleText, icon = None, options = True, widget = None):

		QWidgetAction.__init__(self, parent)
		self.parent = parent
		self.titleText = titleText
		self.icon = icon
		self.options = options
		self.widget = widget

		self.mainWidget = TrunkStandartWidget(self, title = titleText, icon = self.icon, options = self.options, widget = self.widget, actionName = self)

		self.setDefaultWidget(self.mainWidget)
		self.triggered.connect(self.action_name)


	def action_name(self):
		#check adding action
		try:
			self.widget.set_current_trunk(self)
		except:
			pass


	def action_text(self):

		return self.titleText


class TrunkStandartWidget(QWidget):
	def __init__(self, parent, title, icon, options, widget = None, actionName = None):
		QWidget.__init__(self)

		self.titleText = title
		self.icon = icon
		self.options = options
		self.widget = widget
		self.actionName = actionName
		self.setStyleSheet("background-color: rgb(68,68,68);")

		self.setLayout(self.createUI())

	def createUI(self):

		self.mainLayout = QHBoxLayout()
		self.mainLayout.setAlignment(QtCore.Qt.AlignLeft)
		self.mainLayout.setContentsMargins(0,0,0,0)
		self.mainLayout.setSpacing(0)


		'''text'''
		self.textWrapper = QWidget()

		self.textLayout = QHBoxLayout()
		self.textLayout.setAlignment(QtCore.Qt.AlignTop)
		self.textLayout.setContentsMargins(0,0,0,0)
		self.textLayout.setSpacing(0)

		self.textWrapper.setLayout(self.textLayout)

		self.label = QLabel(self.titleText)
		self.label.setMinimumHeight(MAXIMUM_HEIGHT)
		self.label.setStyleSheet("padding-left: 14px;")

		self.textLayout.addWidget(self.label)

		self.mainLayout.insertSpacing(0, 10)
		self.mainLayout.addWidget(self.textWrapper)

		if self.options:
			self.option_icon  = QPixmap(os.path.join(Utility.getCurrentDir(), 'source', 'options.svg')).scaled(11, 11, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
			self.option_button = QPushButton()
			self.option_button.setIcon(self.option_icon)
			self.option_button.setMinimumSize(MAXIMUM_HEIGHT,MAXIMUM_HEIGHT)
			self.option_button.setMaximumSize(MAXIMUM_HEIGHT,MAXIMUM_HEIGHT)
			self.option_button.clicked.connect(self.show_options)
			self.option_window = OptionActionWindow(real_path = self.titleText, widget=self)
			self.mainLayout.addWidget(self.option_button, Qt.AlignRight)

		return self.mainLayout


	def show_options(self):
		self.option_window.show()
		print 'Feedback'


	def set_short_name(self, name):
		self.label.setText(name)


	def get_text(self):
		return self.titleText


	def enterEvent(self, event):

		#if self.newItemCheck == 0:
			#its old item
		self.textWrapper.setStyleSheet("background-color: #5285a6;")
		#self.textLabel.setStyleSheet("color: rgb(230,230,230); padding-left: 14px;")

		# if self.newItemCheck == 1:
		# 	#its new item
		# 	self.textWrapper.setStyleSheet("background-color: #5285a6; background-image: url(" + Utils.getCurrentDir().replace("\\","/") + "/res/small_icons/newItemBG.png);")
		# 	self.textLabel.setStyleSheet("color: #66ff33; padding-left: 14px;")

	def leaveEvent(self, event):
		#if self.newItemCheck == 0:
			#its old item
		self.textWrapper.setStyleSheet("background-color: rgb(68,68,68);")
		# 	self.textLabel.setStyleSheet("color: rgb(230,230,230); padding-left: 14px;")

		# if self.newItemCheck == 1:
		# 	#its new item
		# 	self.textWrapper.setStyleSheet("background-color: rgb(82,82,82); background-image: url(" + Utils.getCurrentDir().replace("\\","/") + "/res/small_icons/newItemBG.png);")
		# 	self.textLabel.setStyleSheet("color: #66ff33; padding-left: 14px;")

	def delete_menu(self):
		#print 'Parent'
		#print self.widget
		self.widget.removing_path(self.actionName)


class OptionActionWindow(QDialog):
	def __init__(self, parent = getWindowPointer(), title = None, real_path = None, widget = None):
		QDialog.__init__(self, parent = parent)

		self.setMinimumWidth (350)
		self.path = real_path
		self.widget = widget
		self.setLayout(self.createUI())
		self.setWindowTitle('Short name dialog')


	def createUI(self):
		self.mainLayout = QVBoxLayout()
		self.shortNameLayout = QHBoxLayout()
		self.longNameLayout = QHBoxLayout()
		self.shortNameLabel = QLabel('Short name       ')
		self.longNameLabel = QLabel('Real trunk path')
		self.shortNameLine = QLineEdit()
		self.longNameLine = QLineEdit()
		self.longNameLine.setText(self.path)
		self.longNameLine.setReadOnly(True)

		#self.dialog = QInputDialog()

		self.buttonLayout = QHBoxLayout()

		self.delButton = QPushButton('Delete Trunk')
		self.delButton.clicked.connect(self.delete_action)

		self.okButton = QPushButton('Save')
		self.okButton.clicked.connect(self.save_options)

		self.cancelButton = QPushButton('Cancel')
		self.cancelButton.clicked.connect(self.save_options)

		#adding
		self.buttonLayout.addWidget(self.delButton)
		self.buttonLayout.addWidget(self.okButton)
		self.buttonLayout.addWidget(self.cancelButton)

		self.mainLayout.addLayout(self.shortNameLayout)
		self.mainLayout.addLayout(self.longNameLayout)
		#self.mainLayout.addWidget(self.dialog)
		self.mainLayout.addLayout(self.buttonLayout)

		self.shortNameLayout.addWidget(self.shortNameLabel)
		self.shortNameLayout.addWidget(self.shortNameLine)

		self.longNameLayout.addWidget(self.longNameLabel)
		self.longNameLayout.addWidget(self.longNameLine)

		return self.mainLayout


	def save_options(self):
		if self.widget:

			print 'test', self.path
			print 'test', self.shortNameLine.text()
			# if self.widget.objectName() == 'Trunk_Selector_Widget':
			# 	if self.shortNameLine.text():
			# 		self.widget.set_short_name(self.shortNameLine.text())
			# 	else:
			# 		self.widget.set_short_name(self.path)

			# else:
			if self.shortNameLine.text():

				self.widget.set_short_name(self.shortNameLine.text())
				Utility.save_option_var(self.shortNameLine.text(), self.path)
			else:
				self.widget.set_short_name(self.path)
				Utility.save_option_var(self.path, self.path)

		self.close()


	def delete_action(self):
		if self.widget:
			print self.widget
			self.widget.delete_menu()
			Utility.delete_option_var(self.path)

		self.close()

	def cancel_action(self):
		self.close()



class Utility():

	@classmethod
	def getWindowPointer(cls):
		#Get and return Maya Main window pointer
		main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
		return wrapInstance(long(main_window_ptr), QWidget)


	@classmethod
	def get_default_plugin(cls):
		if not cmds.pluginInfo( 'visual', query=True, l=True ):

			try:
				cmds.loadPlugin('visual')
			except:
				return 'No trunk'

		#return cmds.pluginInfo('visual', query = True, p = True).split('bin/tools')[0]
		return cmds.pluginInfo('visual', query = True, p = True)


	@classmethod
	def xml_path(cls):
		visual_path = cls.get_default_plugin()
		parent_dir = os.path.dirname(visual_path)
		#print 'Visual ', parent_dir
		xml_path = posixpath.join(parent_dir, 'paths.xml')
		return xml_path


	@classmethod
	def trunk_list(cls, new_path = None):
		visual_path = cls.get_default_plugin()
		parent_dir = os.path.dirname(visual_path)
		print 'Visual ', parent_dir
		xml_path = posixpath.join(parent_dir, 'paths.xml')
		print 'Visual ', xml_path
		add_paths = cls.editXML(new_path, xml_path)
		return add_paths


	@classmethod
	def all_files(cls):
		for path, subdirs, files in os.walk(root):
			for name in files:
				print os.path.join(path, name)


	@classmethod
	def getCurrentDir(cls):
		# Get the place where this .py file is located
		path = str(os.path.dirname(__file__))
		return path


	@classmethod
	def editXML(cls, do, xml, delete=False):

		defoultPathes = ['../../../../res/wot', '../../../../res/bigworld', '../../../../bin/tools/exporter/resources']
		pathesText = []
		#pathContent, xml = pluginTrankPathes()[2], pluginTrankPathes()[3]

		et = ET.parse(xml)
		root = et.getroot()
		mainPath = []
		#print 'base', mainPath
		if do:
			cmds.unloadPlugin('visual')
			time.sleep(1)
			if delete:
				for pths in root:
					for p in pths:
						if p.text == do:
							pths.remove(p)
			else:
				for pths in root:
					newPath = ET.Element('Path')
					newPath.text = do
					pths.append(newPath)
			et.write(xml)
			cmds.loadPlugin('visual')

		else:
			for pths in root:
				for p in pths:
					pathesText.append(p.text)
			print 'Pathes_:', pathesText

			addingPath = [x for x in pathesText if x not in defoultPathes]
			mainPath.extend(addingPath)
			print 'Pathes: ', addingPath, mainPath
			return mainPath


	@classmethod
	def save_option_var(cls, name, value):
		# if cmds.optionVar( exists = name ):
		# 	pass
		# else:
		cmds.optionVar( sv=(name, value) )


	@classmethod
	def delete_option_var(cls, name):
		print 'nnnn', name
		cmds.optionVar( remove = name )
