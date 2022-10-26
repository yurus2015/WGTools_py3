import maya.cmds as cmds
from maya.mel import eval as meval
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

MENU = 'mainFileMenu'
ACTION = 'exportActiveFileOptions'
BWACTION = '    Export BigWorld'
BWACTIONNAME = 'bigWorldExportMenu'

class BigWorldExport(QObject):
	def __init__(self):
		super(BigWorldExport, self).__init__()
		self.setObjectName('BigWorldExport')
		self.getWindowPointer()
		Utility.mel_command()


	def actionToDo(self):
		Utility.get_default_plugin()


	def triggered(self):
		self.bw_action.triggered.connect(self.actionToDo)


	def getWindowPointer(self):
		#Get and return Maya Main window pointer
		main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
		self.root_window = wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


	def getWorkspacePointer(self, object_root, object_type, object_name):
		all_objects = object_root.findChildren(object_type)
		widget = [item for item in all_objects if item.objectName() == object_name][0]
		return widget


	def addMenuToMaya(self):
		file_menu = self.getWorkspacePointer(self.root_window, QMenu, MENU)
		meval('buildFileMenu();')
		action = self.getWorkspacePointer(file_menu, QAction, ACTION)
		self.bw_action = QAction(BWACTION, file_menu) #need class
		self.bw_action.setObjectName('bigWorldExportMenu')
		file_menu.insertAction(action, self.bw_action)


class Utility():

	@classmethod
	def get_default_plugin(cls):
		if not cmds.pluginInfo( 'visual', query=True, l=True ):

			try:
				cmds.loadPlugin('visual')
			except:
				return 'No brunch'


	@classmethod
	def mel_command(cls):
		cmd = 'buildFileMenu(); global string $gMainWindow; setParent $gMainWindow; '
		cmd += 'if (`menu -q -exists mainFileMenu`) {'
		cmd += 'setParent -menu mainFileMenu;'
		cmd += 'menuItem -divider true -insertAfter exportActiveFileOptions sendToDivider2;'
		cmd += 'menuItem -subMenu true  -label "Export to BigWorld" -insertAfter sendToDivider2 sendToBWMenu;'
		cmd += 'menuItem -label "Export All"  -c ("python (\\"import wargamingMenu.trunk.gui; reload(wargamingMenu.trunk.gui)\\"); python (\\"wargamingMenu.trunk.gui.main(export = False)\\")") sendAllToBWMenu;'
		cmd += 'menuItem -label "Export Selection" -c ("python (\\"import wargamingMenu.trunk.gui; reload(wargamingMenu.trunk.gui)\\"); python (\\"wargamingMenu.trunk.gui.main(export = True)\\")") sendActiveToBWMenu;'
		cmd += '}'

		meval(cmd)
		cls.get_default_plugin()


def main():
	menu = BigWorldExport()
