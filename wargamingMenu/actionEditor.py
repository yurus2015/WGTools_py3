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

#from shiboken2 import wrapInstance
#
#
#try:
#	import shiboken
#except:
#	import shiboken2 as shiboken
#
#try:
#	from shiboken import wrapInstance
#except:
#	from shiboken2 import wrapInstance
#
#from PySide import QtCore, QtGui
#from shiboken import wrapInstance
import shutil

import sys
import os


from utils import Utils
import main as Main


class ActionRecord(QWidget):

	def __init__(self, parent = None, actionName = None, label = None,  icon = None):

		QWidget.__init__(self,parent)

		'''Vars'''
		self.actionFile = actionName
		self.actionFileName = self.actionFile.split("\\")[-1].split(".")[0]
		self.actionLabel = label
		self.actionCategory = None
		self.actionIcon = icon
		self.iconPath = None

		if "/" in self.actionLabel:
			self.actionCategory = self.actionLabel.split("/")[0]

		'''UI'''
		self.setFixedSize(980, 30)
		self.setAttribute(QtCore.Qt.WA_StyledBackground)

		self.setAutoFillBackground(True)
		self.setPalette(QPalette(QColor(80, 80, 80)))

		self.setLayout(self.createUI())

	def readActionData(self):
		pass

	def createUI(self):

		self.mainLayout = QHBoxLayout()
		self.mainLayout.setAlignment(QtCore.Qt.AlignLeft)
		self.mainLayout.setContentsMargins(5,5,5,5)
		self.mainLayout.setSpacing(10)


		'''Content'''

		self.checkbox = QCheckBox("")
		self.checkbox.setFixedSize(23, 20)


		self.actionName_label = QLabel(self.actionLabel)
		self.actionName_label.setFixedSize(163, 20)

		self.newName_tedit = QLineEdit()
		self.newName_tedit.setStyleSheet("QLineEdit{background-color: #222;}")
		self.newName_tedit.setFixedSize(195, 20)

		self.submenu_tedit = QLineEdit()
		self.submenu_tedit.setStyleSheet("QLineEdit{background-color: #222;}")
		self.submenu_tedit.setFixedSize(198, 20)
		if self.actionCategory:
			self.submenu_tedit.setText(self.actionCategory)

		self.icon_tedit = QLineEdit()
		# self.icon_tedit.setEnabled(0)
		self.icon_tedit.setFixedSize(300, 20)
		self.icon_tedit.setStyleSheet("QLineEdit{color: #aaa; background-color: #555;}")
		if self.actionIcon:
			self.icon_tedit.setText(self.actionIcon)

		self.icon_button =QPushButton("Set")
		self.icon_button.setStyleSheet("QLineEdit{color: #aaa; background-color: #aaa;}")
		self.connect(self.icon_button, QtCore.SIGNAL("clicked()"), self.pathBrowser)
		self.icon_button.setFixedSize(40, 19)





		'''main layout'''
		self.mainLayout.addWidget(self.checkbox)
		self.mainLayout.addWidget(self.actionName_label)
		self.mainLayout.addWidget(self.newName_tedit)
		self.mainLayout.addWidget(self.submenu_tedit)
		self.mainLayout.addWidget(self.icon_tedit)
		self.mainLayout.addWidget(self.icon_button)



		return self.mainLayout

	def pathBrowser(self): #open browser to set export path
		path = None
		try:
			path = cmds.fileDialog2(fm=1, dialogStyle=2)[0]
		except:
			pass

		if path:
			self.icon_tedit.setText(path.split("/")[-1])
			self.iconPath = path



class ActionEditor(QDialog):

	def __init__(self, parent = Utils.getWindowPointer()):

		QDialog.__init__(self,parent)

		'''vars'''
		#none

		'''ui'''
		self.setFixedSize(1000,600)
		self.setWindowTitle("Action Editor")
		self.setObjectName("wgMenuActionEditor")


		self.setLayout(self.createUI())

		'''data'''
		self.requestData()


	def createUI(self):

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
		self.mainLayout.setContentsMargins(5,5,5,5)
		self.mainLayout.setSpacing(5)

		'''Header'''

		self.header = QWidget()
		self.header.setFixedSize(990, 30)
		self.header.setAttribute(QtCore.Qt.WA_StyledBackground)
		self.header.setStyleSheet( ".QWidget{\
										border: 1px solid #555;\
										border-width: 0px 0px 1px 0px;\
										}")

		self.headerLayout = QHBoxLayout()
		self.headerLayout.setAlignment(QtCore.Qt.AlignLeft)
		self.headerLayout.setContentsMargins(3,3,3,3)
		self.headerLayout.setSpacing(5)
		self.header.setLayout(self.headerLayout)

		self.label_Trash = QLabel("")
		self.label_Trash.setFixedSize(30, 20)
		# self.label_Trash.setGeometry(0, 0, 20, 20)
		self.label_Trash.setPixmap(QPixmap(Utils.getCurrentDir() + "\\res\\small_icons\\" + str("icon_trash.png")).scaled(15,15, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
		self.label_Trash.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)

		self.label_Action =QLabel("Action")
		self.label_Action.setFixedSize(170, 20)

		self.label_NewName =QLabel("New Name")
		self.label_NewName.setFixedSize(200, 20)

		self.label_Submenu =QLabel("SubMenu")
		self.label_Submenu.setFixedSize(200, 20)

		self.label_Icon =QLabel("Icon")
		self.label_Icon.setFixedSize(200, 20)


		self.headerLayout.addWidget(self.label_Trash)
		self.headerLayout.addWidget(self.label_Action)
		self.headerLayout.addWidget(self.label_NewName)
		self.headerLayout.addWidget(self.label_Submenu)
		self.headerLayout.addWidget(self.label_Icon)



		'''ScrollArea'''

		self.scrollarea= QScrollArea() #1 scrollArea Widget
		self.scrollarea.setWidgetResizable(True)
		self.scrollarea.setFixedSize(990,530)
		self.scrollarea.setFrameShape(QFrame.NoFrame);
		self.scrollarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

		self.scroll_area_widget = QWidget() #2 create Widget to place it inside scroll area

		self.scroll_layout = QVBoxLayout() #3 create layout for this widget
		self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
		self.scroll_layout.setContentsMargins(0,0,0,0)
		self.scroll_layout.setSpacing(5)

		self.scrollarea.setWidget(self.scroll_area_widget)
		self.scroll_area_widget.setLayout(self.scroll_layout)#set layout to widget


		'''Footer'''


		self.buttons_Layout = QHBoxLayout()
		self.scroll_layout.setAlignment(QtCore.Qt.AlignLeft)
		self.scroll_layout.setContentsMargins(0,0,0,0)
		self.scroll_layout.setSpacing(5)

		self.buttonOK = QPushButton("Done")
		self.connect(self.buttonOK, QtCore.SIGNAL("clicked()"), self.complete)
		self.buttonCancel = QPushButton("Cancel")
		self.connect(self.buttonCancel, QtCore.SIGNAL("clicked()"), self.cancel)

		self.buttons_Layout.addWidget(self.buttonOK)
		self.buttons_Layout.addWidget(self.buttonCancel)

		'''Main Layout'''
		self.mainLayout.addWidget(self.header)
		self.mainLayout.addWidget(self.scrollarea)
		self.mainLayout.addLayout(self.buttons_Layout)

		return self.mainLayout

	def requestData(self):

		self.recordList = []

		self.fileList = Utils.getActionFiles()

		for i in self.fileList:
			if "user_" in i:

				#get file content
				actionLabel = None
				actionCategory = None
				actionIcon = None
				actionFile = i

				with open(i) as runActionFile:
					for line in runActionFile:
						if "action_label" in line:
							actionLabel = line.split("=")[-1].strip().replace("\"","")
						elif "action_category" in line:
							actionCategory = line.split("=")[-1].strip().replace("\"","")
						elif "action_icon" in line:
							actionIcon = line.split("=")[-1].strip().replace("\"","")

				if not actionLabel: continue



				widget = ActionRecord(actionName = actionFile, label = actionLabel, icon = actionIcon)
				self.recordList.append(widget)
				self.scroll_layout.addWidget(widget)



		#add NULL widget

		null = QWidget()
		null.setFixedSize(500, 530)
		self.scroll_layout.addWidget(null)

	def complete(self):
		for i in self.recordList:

			if i.checkbox.isChecked():
				os.remove(i.actionFile)
				try:
					os.remove(Utils.getCurrentDir().replace("\\","/") + "/res/small_icons/" + "icon_" + i.actionFileName + ".png")
				except:
					pass
			else:
				#change File DATA
				filedata = None
				with open(i.actionFile, 'r') as f :
					filedata = f.read()

				newName = i.newName_tedit.text()
				newSubmenu = i.submenu_tedit.text()
				newIcon = i.icon_tedit.text()

				#check if we wrote new name
				if newName:
					#add submenu to name
					if newSubmenu:
						newName = newSubmenu + "/" + newName
				else:
					#name is old but we changed submenu
					if newSubmenu:
						#check if name already has submenu
						if "/" in i.actionLabel:
							newName = newSubmenu + "/"  +  i.actionLabel[len(i.actionLabel.split("/")[0]) + 1 : ]
						else:
							newName = newSubmenu + "/" + i.actionLabel
					else:
						if "/" in i.actionLabel:
							newName = i.actionLabel[ len(i.actionLabel.split("/")[0])+1 : ]


				if newName:
					#write to file
					filedata = filedata.replace(i.actionLabel, newName)

				if newIcon:
					#check if file has action_icon

					#if its not the same file
					if i.iconPath:
						if i.iconPath != Utils.getCurrentDir().replace("\\","/") + "/res/small_icons/" + "icon_" + i.actionFileName + ".png":
							shutil.copy2(i.iconPath, Utils.getCurrentDir().replace("\\","/") + "/res/small_icons/" + "icon_" + i.actionFileName + ".png")


					if i.actionIcon:
						#replace by new name
						filedata = filedata.replace(i.actionIcon, "icon_" + i.actionFileName + ".png")
					else:
						#create new line
						filedata = filedata + '\n\naction_icon = "icon_' + i.actionFileName + '.png"'


				if newName or newIcon:
					#write to file
					with open(i.actionFile, 'w') as f:
						f.write(filedata)



		Main.run()
		dialogAE.close()
		dialogAE.deleteLater()


	def cancel(self):
		dialogAE.close()
		dialogAE.deleteLater()




def main():

	global dialogAE
	try:
		dialogAE.close()
		dialogAE.deleteLater()
	except:
		pass
	dialogAE = ActionEditor()
	dialogAE.show()