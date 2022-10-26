from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.cmds as cmds
#from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from .gui.gui import *
from .gui.constants import AUTORUNOPTIONS, LABEL
import modelingToolset.gui.dock as dock

# import feedback.main as fbm
import traceback

CONTROLS = ['WG Toolset 2019', 'WG_Toolset_2019', 'WG_Toolset_2019WorkspaceControl']


def deleteUI():
	#delete old workspaceControl
	if cmds.workspaceControl('WG Toolset 2019', ex=True):
		cmds.deleteUI('WG Toolset 2019')

	if cmds.workspaceControl('WG_Toolset_2019', ex=True):
		cmds.deleteUI('WG_Toolset_2019')

	if cmds.workspaceControl(ToolsetMainWindow.CONTROL_NAME, ex=True):
		cmds.deleteUI(ToolsetMainWindow.CONTROL_NAME)


def deleteControl(control):
	if cmds.workspaceControl(control, q=True, exists=True):
		cmds.workspaceControl(control,e=True, close=True)
		cmds.deleteUI(control,control=True)

	# if cmds.workspaceControl(ToolsetMainWindow.CONTROL_NAME, ex=True):
	# 	cmds.deleteUI(ToolsetMainWindow.CONTROL_NAME)


def deleteHUDtexel():
	if cmds.headsUpDisplay( 'HUDtexelMessure', q=1, ex=1):
		cmds.headsUpDisplay( 'HUDtexelMessure', rem=True )


def main():
	'''
	Clear old workspaces
	'''
	for control in CONTROLS:
		deleteControl(control)

	deleteHUDtexel()

	'''
	Entry point to call ui from maya.
	'''
	DockManager.show(debug = True)
	try:
		cmds.workspaceControl(ToolKitMainWindow.CONTROL_NAME, e=True, label=ToolKitMainWindow.DOCK_LABEL_NAME)
	except:
		pass


class DockManager(dock.DockManager):
	'''
	overridden
	'''
	def __init__(self):
		super(DockManager, self).__init__()
		self.window_name = ToolKitMainWindow.CONTROL_NAME
		self.mixin_cls = lambda: MayaMixin(window_name=self.window_name,
														   main_widget_cls=ToolKitMainWindow,
														   title=LABEL)

class MayaMixin(MayaQWidgetDockableMixin, QWidget):
	def __init__(self, window_name, main_widget_cls, title, **kwargs):
		'''
		Wrapper for incoming widget(main_widget_cls).
		A Qwidget that is registered as a Maya Control (aka maya class wrapped UI) that is a container for our custom UI.

		:param str window_name: name used internally by maya to identify mixin
		:param QtWidgets.QWidget main_widget_cls: widget class to get wrapped in mixin
		:param str title: title for window/tab
		:param kwargs:
		'''
		super(MayaMixin, self).__init__(**kwargs)
		# Set the ui object name. Used by maya to find UI as maya control class
		self.setObjectName(window_name)
		# Layout to hold main_widget_cls
		self._mainLayout = QVBoxLayout()
		# Set no margins so layout doesnt bulk up UI
		self._mainLayout.setContentsMargins(0, 0, 0, 0)
		# Set the layout for this Qwidget
		self.setLayout(self._mainLayout)
		# Init main_widget_cls widget
		self.mainWidget = main_widget_cls()
		# Add mainWidget to the layout
		self._mainLayout.addWidget(self.mainWidget)
		print('Title', title)
		# Set the title of the mixin widget
		self.setWindowTitle(title)
