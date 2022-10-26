from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import os, posixpath, time, re
import xml.etree.ElementTree as ET
import maya.cmds as cmds
import maya.OpenMayaUI as omu
from shiboken2 import wrapInstance
import objectExport.objectsExporter as OE


WIDTH = 400
HEIGHT = 100
CURRENT_FILE = os.path.dirname(os.path.abspath(__file__))

def mainWindowPointer():
	ptr = omu.MQtUtil.mainWindow() #pointer for the main window
	return wrapInstance(long(ptr), QWidget)


class Utils(object):

	@classmethod
	def load_option_var(cls):
		current_branch = list_branches = None
		if cmds.optionVar( exists='current_branch' ):
			current_branch = cmds.optionVar( q='current_branch' )
		else:
			cmds.optionVar( sv=('current_branch', current_branch))

		if cmds.optionVar( exists='list_branches' ):
			list_branches = cmds.optionVar( q='list_branches' )
		else:
			cmds.optionVar( sva=('list_branches', list_branches))

		return list_branches


	@classmethod
	def save_option_var(cls, path, delete = None):
		#delete path from combobox
		if delete == True:
			pathes = cmds.optionVar( q='list_branches' )
			index = pathes.index(path)
			cmds.optionVar( rfa=('list_branches', index) )
			return

		#add path to combobox
		if delete == False:
			cmds.optionVar(sva=('list_branches', path))
			return

		#set selection path
		if delete == None:
			cmds.optionVar( sv=('current_branch', path))


	@classmethod
	def loadVisualPlugin(cls):
		if not cmds.pluginInfo( 'visual', query=True, l=True ):
			try:
				cmds.loadPlugin('visual')
				return True
			except:
				message('Load visual plugin', 'The visual plugin don`t load.\n   Load plugin manualy.  ')
				return False
		else:
			return True


	@classmethod
	def pluginPathes(cls):
		cls.loadVisualPlugin()
		pluginDir = pathExport = pathContent = xmlFile = None
		pluginPath = cmds.pluginInfo('visual', query = True, p = True)
		pluginDir = os.path.dirname(pluginPath)
		xmlFile = posixpath.join(pluginDir, 'paths.xml')

		return xmlFile


	@classmethod
	def editXML(cls, path = None, delete = None):
		xml = cls.pluginPathes()
		et = ET.parse(xml)
		root = et.getroot()

		if path:
			new_path = ET.Element('Path')
			new_path.text = path
			for pths in root:
				check = True
				for p in pths:
					if p.text == path:
						check = False
						if delete:
							pths.remove(p)
							break
				if check:
					pths.append(new_path)
			et.write(xml)

			#restart plugin
			cmds.unloadPlugin('visual')
			time.sleep(1)
			cmds.loadPlugin('visual')


class BranchSelection_Wnd(QDialog):
	def __init__(self, parent = mainWindowPointer()):
		QDialog.__init__(self, parent)

		self.setFixedSize(WIDTH, HEIGHT)
		self.setWindowTitle("Object Export Branch")
		self.setModal(False)
		self.setWindowFlags(QtCore.Qt.Window)
		self.setObjectName("BranchSelection")

		#save position window
		self.settings = QtCore.QSettings("BranchSelection")
		if not self.settings.value("geometry") == None:
			self.restoreGeometry(self.settings.value("geometry"))

		Utils.load_option_var()
		self.initUI()


	def initUI(self):
		main_layout = QVBoxLayout(self)
		trank_list = self.trankList()
		buttons_layout = self.buttons_layout()
		main_layout.addWidget(trank_list)
		main_layout.addLayout(buttons_layout)


	def trankList(self):
		# self.pathes = Utils.editXML()
		# d:\ART_MAIN\game\bin\tools\devtools\scripts\maya2018\wargamingMenu\options\objectExporter\
		posixpath.join(CURRENT_FILE, 'delete_path.svg')
		self.pathes = Utils.load_option_var()
		self.trank_Combo = QComboBox()
		self.trank_Combo.setFixedHeight(22)
		self.trank_Combo.setObjectName('customTrankCombo')
		self.trank_Combo.currentIndexChanged.connect(self.save_current_path)
		self.buttonDir  = self.initButton(command = lambda:self.dirBrowser())
		self.buttonDir.setFixedWidth(20)
		self.buttonDir.setFixedHeight(20)
		self.icon_add = QIcon(posixpath.join(CURRENT_FILE, 'add_path.svg'))
		self.buttonDir.setIcon(self.icon_add)
		self.buttonDir.setIconSize(QSize(18, 18))
		self.buttonDir.setStyleSheet("QPushButton {border:0px; background: rgb(0, 0, 0, 0);}")
		self.delete_path  = self.initButton(command = lambda:self.delete_trunk())
		self.delete_path.setFixedWidth(20)
		self.delete_path.setFixedHeight(20)
		self.icon_del = QIcon(posixpath.join(CURRENT_FILE, 'delete_path.svg'))
		self.delete_path.setIcon(self.icon_del)
		self.delete_path.setIconSize(QSize(18, 18))
		self.delete_path.setStyleSheet("QPushButton {border:0px; background: rgb(0, 0, 0, 0);}")
		self.trank_Layout = ComboBoxLayout(self.trank_Combo, self.buttonDir, self.delete_path)

		current_branch = cmds.optionVar( q='current_branch' )
		self.pathes = Utils.load_option_var()

		if self.pathes:
			for i in range(len(self.pathes)):
				self.trank_Combo.addItem(self.pathes[i])
				if current_branch == self.pathes[i]:
					self.trank_Combo.setCurrentIndex(i)

		return self.trank_Layout


	def save_current_path(self):
		Utils.save_option_var(self.trank_Combo.currentText())


	def initButton(self, parent=None, title="", command = None, h = None):
		self._button = QPushButton(title)
		if command:
			self._button.clicked.connect(command)

		return self._button


	def buttons_layout(self):
		self.buttons_layout = QHBoxLayout()
		self.buttons_layout.setAlignment(Qt.AlignRight)
		self.export_btn = self.initButton(self, title = 'Export', h =60, command = lambda:self.export_selected_trunk())
		self.export_btn.setToolTip("Export objects")
		self.export_btn.setFixedWidth(100)
		self.close_btn = self.initButton(self, title = 'Close', command = lambda:close_window(), h =60)
		self.close_btn.setToolTip("Close dialog")
		self.close_btn.setFixedWidth(100)
		self.buttons_layout.addWidget(self.export_btn)
		self.buttons_layout.addWidget(self.close_btn)

		return self.buttons_layout


	def dirBrowser(self): #open browser to set export path
		bpath = None
		try:
			bpath = cmds.fileDialog2(fm=3, dialogStyle=1)[0]
		except:
			pass

		if not bpath:
			return

		if bpath and 'content' in bpath:
			if bpath not in self.pathes:
				self.trank_Combo.addItem(bpath)
				self.trank_Combo.setCurrentIndex(self.trank_Combo.count() -1)
				self.pathes.append(bpath)
				Utils.save_option_var(bpath, delete=False)
		else:
			cmds.confirmDialog( title='Warning', message= 'Select "content*" dir in your branch',
				button=['   OK   '], defaultButton='   OK   ')


	def delete_trunk(self):
		indx = self.trank_Combo.currentIndex()
		bpath = self.trank_Combo.currentText()
		self.trank_Combo.removeItem(indx)
		# self.save_current_path(bpath, delete=True)
		Utils.save_option_var(self.trank_Combo.currentText(), True)
		# Utils.editXML(bpath, True)


	def export_selected_trunk(self):
		bpath = self.trank_Combo.currentText()
		print 'External path:', bpath
		if os.path.exists(bpath):
			print 'Path exists:', bpath
			#wtite to xml a parent directory of ../content*
			parent_path = re.split('/content', bpath)[0]
			Utils.editXML(parent_path)
			OE.main(bpath)
			Utils.editXML(parent_path, True)
		else:
			cmds.confirmDialog( title='Warning', message= 'Directory "' + bpath + '" does not exist',
				button=['   OK   '], defaultButton='   OK   ')


class ComboBoxLayout(QWidget):

	def __init__(self,*args, **kwargs):
		QWidget.__init__(self)
		#self.setContentsMargins(0, 0, 0, 0)
		layout  = QHBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		for arg in args:

			if type(arg) == type(list()):
				for i in arg:
					layout.addWidget(i)
			else:
				try:
					layout.addLayout(arg)
				except:
					layout.addWidget(arg)

	def mousePressEvent(self, QMouseEvent):
		if QMouseEvent.button() == Qt.LeftButton:
			print("Left Button Clicked")
		elif QMouseEvent.button() == Qt.RightButton:
			print("Right Button Clicked")


def close_window():
	if cmds.window("BranchSelection", q=True, exists=True):
		cmds.deleteUI("BranchSelection")
	try:
		cmds.deleteUI('MayaWindow|BranchSelection')
	except:
		pass

def main():
	close_window()
	dialog = BranchSelection_Wnd()
	dialog.show()