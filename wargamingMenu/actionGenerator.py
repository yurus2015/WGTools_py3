import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaRender as OpenMayaRender


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


#try:
#	import shiboken
#except:
#	import shiboken2 as shiboken
#
#try:
#	from shiboken import wrapInstance
#except:
#	from shiboken2 import wrapInstance

#from PySide import QtCore, QtGui
#from shiboken import wrapInstance
import shutil

import sys
import os


from utils import Utils
import main as Main

import syntax
reload(syntax)

class ActionGenerator(QDialog):

	def __init__(self, parent = Utils.getWindowPointer()):
		QDialog.__init__(self,parent)


		'''data'''
		self.iconPath = None

		self.setWindowTitle("Action Creator")
		self.setObjectName("wgActionGenerator")

		self.setFixedSize(800, 760)

		self.setLayout(self.createUI())



	def createUI(self):

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
		self.mainLayout.setContentsMargins(3,3,3,3)
		self.mainLayout.setSpacing(5)

		'''layouts'''
		self.optionsLayout = QVBoxLayout()
		self.optionsLayout.setAlignment(QtCore.Qt.AlignLeft)
		self.optionsLayout.setContentsMargins(10,10,10,10)
		self.optionsLayout.setSpacing(10)

		self.textLayout = QVBoxLayout()
		self.textLayout.setAlignment(QtCore.Qt.AlignLeft)
		self.textLayout.setContentsMargins(0,0,0,0)
		self.textLayout.setSpacing(5)


		self.buttonsLayout = QHBoxLayout()
		self.buttonsLayout.setAlignment(QtCore.Qt.AlignBottom)
		self.buttonsLayout.setContentsMargins(0,0,0,0)
		self.buttonsLayout.setSpacing(2)

		'''Option fields'''
		self.opt_groupBox = QGroupBox("Options")
		self.opt_groupBox.setFixedSize(795, 100)
		self.opt_groupBox.setLayout(self.optionsLayout)



		self.opt_layer01 = QHBoxLayout()
		self.opt_layer02 = QHBoxLayout()

		self.opt_nameLayout = QHBoxLayout()
		self.opt_nameLayout.setAlignment(QtCore.Qt.AlignLeft)
		self.opt_nameLayout.setSpacing(0)

		self.opt_iconLayout = QHBoxLayout()
		self.opt_iconLayout.setAlignment(QtCore.Qt.AlignLeft)
		self.opt_iconLayout.setSpacing(5)

		self.opt_subMenuLayout = QHBoxLayout()
		self.opt_subMenuLayout.setAlignment(QtCore.Qt.AlignLeft)
		self.opt_subMenuLayout.setSpacing(0)

		self.opt_layer01.addLayout(self.opt_nameLayout)
		self.opt_layer01.addLayout(self.opt_iconLayout)
		self.opt_layer02.addLayout(self.opt_subMenuLayout)

		self.optionsLayout.addLayout(self.opt_layer01)
		self.optionsLayout.addLayout(self.opt_layer02)


		#name
		self.nameLabel = QLabel("Script Name*")
		self.nameLabel.setFixedSize(80,20)

		self.nameEdit = QLineEdit()
		self.nameEdit.setStyleSheet("border-style: no-focus")
		self.nameEdit.setFixedSize(200,20)


		self.opt_nameLayout.addWidget(self.nameLabel)
		self.opt_nameLayout.addWidget(self.nameEdit)

		#icon
		self.iconLabel = QLabel("Icon Path")
		self.iconLabel.setFixedSize(60,20)

		self.iconEdit = QLineEdit()
		self.iconEdit.setStyleSheet("border-style: no-focus")
		self.iconEdit.setFixedSize(350, 20)
		self.iconEdit.setEnabled(0)

		self.iconPathButton = QPushButton("Set")
		self.connect(self.iconPathButton, QtCore.SIGNAL("clicked()"), self.pathBrowser)
		self.iconPathButton.setFixedSize(40,20)

		self.opt_iconLayout.addWidget(self.iconLabel)
		self.opt_iconLayout.addWidget(self.iconEdit)
		self.opt_iconLayout.addWidget(self.iconPathButton)

		#submenu
		self.subMenuLabel = QLabel("SubMenu")
		self.subMenuLabel.setFixedSize(80,20)

		self.subMenuEdit = QLineEdit()
		self.subMenuEdit.setStyleSheet("border-style: no-focus")
		self.subMenuEdit.setFixedSize(200,20)


		self.opt_subMenuLayout.addWidget(self.subMenuLabel)
		self.opt_subMenuLayout.addWidget(self.subMenuEdit)

		'''Editor'''
		self.editorLabel = QLabel("Script:")

		self.editor = QPlainTextEdit()
		self.editor.setFrameStyle(QFrame.NoFrame)
		self.editor.setFixedSize(795,600)
		self.editor.setStyleSheet("font-size: 14px; font-family: 'Lucida Console'; line-height: 18px;")
		self.editor.setWordWrapMode(QTextOption.NoWrap)
		self.editor.setTabStopWidth(32)
		highlight = syntax.PythonHighlighter(self.editor.document())

		self.textLayout.addWidget(self.editorLabel)
		self.textLayout.addWidget(self.editor)


		'''buttons'''
		self.button_create = QPushButton("Create Action")
		self.button_create.setMaximumHeight(26)
		self.connect(self.button_create, QtCore.SIGNAL("clicked()"), self.addScriptToMenu)

		self.runButton = QPushButton("Run Script")
		self.runButton.setMaximumHeight(26)
		self.runButton.setIcon(QIcon(Utils.getCurrentDir() + "\\res\\small_icons\\icon_RunScript.png"))
		self.connect(self.runButton, QtCore.SIGNAL("clicked()"), self.runScript)

		self.button_cancel = QPushButton("Cancel")
		self.button_cancel.setMaximumHeight(26)
		self.connect(self.button_cancel, QtCore.SIGNAL("clicked()"), self.closeApp)

		self.buttonsLayout.addWidget(self.button_create)
		self.buttonsLayout.addWidget(self.runButton)
		self.buttonsLayout.addWidget(self.button_cancel)


		'''main layout'''
		self.mainLayout.addWidget(self.opt_groupBox)
		self.mainLayout.addLayout(self.textLayout)
		self.mainLayout.addLayout(self.buttonsLayout)

		return self.mainLayout

	def closeApp(self):
		cmds.deleteUI("wgActionGenerator")

	def runScript(self):
		script = self.editor.toPlainText()
		exec(script)


	def pathBrowser(self): #open browser to set export path
		path = None
		try:
			path = cmds.fileDialog2(fm=1, dialogStyle=2)[0]
		except:
			pass

		if path:
			self.iconEdit.setText(path.split("/")[-1])
			self.iconPath = path


	def addScriptToMenu(self):

		scriptName = self.nameEdit.text()
		fileName = "user_"+"".join(scriptName.split())
		subMenuName = self.subMenuEdit.text()
		script = self.editor.toPlainText()

		if not scriptName:
			cmds.warning("You need to set the script name")
			return

		if not script:
			cmds.warning("Put some python script in a 'script' section")
			return


		print "New action '"+scriptName+"' was added"


		if not subMenuName:
			scriptFormat = "#modificators\n\naction_label = \"" + str(scriptName) + "\"\n"
		else:
			scriptFormat = "#modificators\n\naction_label = \"" +str(subMenuName)+"/"+ str(scriptName) + "\"\n"

		if self.iconPath:
			scriptFormat += "action_icon = \"" + str("icon_" + fileName + ".png") + "\""
			shutil.copy2(self.iconPath, Utils.getCurrentDir() + "/res/small_icons/" + "icon_" + fileName + ".png")

		scriptFormat += "\n\n" + "#running procedure" + "\n\n" + script


		#new file
		try:
			newFile = open(Utils.getCurrentDir() + "\\actions\\"+fileName+".py",'w')   # Trying to create a new file
			newFile.write(scriptFormat)
			newFile.close()
		except:
			cmds.warning("something wrong with writting data on your disk. Check if you have a right to create files in your trank folder")
			return

		#copy icon to res folder and rename it according scriptName   icon_fileName.png
		# print self.iconPath
		# print self.iconPath[ : -1 * len(self.iconPath.split("/")[-1])  ] + "icon_" + fileName + ".png"


		#restarg everything
		Main.run()
		cmds.deleteUI("wgActionGenerator")






def main():

	# if cmds.window("wgActionGenerator",q=True,exists=True):
	#     cmds.deleteUI("wgActionGenerator")

	global dialogAG
	try:
		dialogAG.close()
		dialogAG.deleteLater()
	except:
		pass
	dialogAG = ActionGenerator()
	dialogAG.show()