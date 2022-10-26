#from PySide import QtCore, QtGui
#from PySide.QtWebKit import QWebView, QWebFrame, QWebPage, QWebElement
import maya.cmds as cmds
import maya.OpenMayaUI as omu
import os

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
from PySide2.QtWebKitWidgets import QWebView, QWebFrame, QWebPage, QWebElement


currentFilePath = os.path.dirname(os.path.realpath(__file__))
parentDir = currentFilePath.split('widgets')[0]
#print 'PARENT', parentDir
def mainWindowPointer():
	ptr = omu.MQtUtil.mainWindow() #pointer for the main window
	return wrapInstance(long(ptr), QWidget)

class SG_helpImage(QWidget):
	def __init__(self, parent = mainWindowPointer()):
		super(SG_helpImage, self).__init__(parent)

		#self.setWindowFlags(QtCore.Qt.ToolTip)
		self.setWindowFlags(QtCore.Qt.Window)
		self.setWindowTitle('Simplygon Help')
		#self.setModal(False)
		cursorPosition = QCursor.pos()
		#print 'CURSOR', cursorPosition
		self.setGeometry(cursorPosition.x(), cursorPosition.y(), 605, 800)

		self.initUI()

	def initUI(self):

		self.mainLayout = QVBoxLayout(self) #main layout

		self.topLayout = QFrame() #close layout
		self.topLayout.setMinimumHeight(8)
		self.topLayout.setMaximumHeight(8)


		#self.closeLabel = ClickableLabel(self.topLayout)
		#self.closeLabel.clicked.connect(self.anotherSlot)



		vebWiew = QWebView()
		#url = QtCore.QUrl.fromLocalFile('d:/BRANCH3/devtools/scripts/simplygon/docs/simplygon_doc.html')
		url = QtCore.QUrl.fromLocalFile(parentDir + 'docs/simplygon_doc.html')
		vebWiew.setUrl(url)

		self.mainLayout.addWidget(self.topLayout)
		self.mainLayout.addWidget(vebWiew)

	def anotherSlot(self):
		self.close()
		self.deleteLater()
		#print "now I'm in Main.anotherSlot"


class Browser(QWebView):
	def __init__(self):
		QWebView.__init__(self)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
		self.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)
		self.setStyleSheet("border:5px; background: rgb(0, 0, 0);")
		self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
		self.linkClicked.connect(self.test)


	@QtCore.Slot(QtCore.QUrl)
	def test(self, url):
		link =  url.toString().encode('Windows-1251')
		webbrowser.open(link)


	def event(self, event):
		if event.type() == 11:
			self.close()
			self.deleteLater()
			return False
		return QWidget.event(self, event)
