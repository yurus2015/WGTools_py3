import os
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from .constants import *
import modelingToolset as MTS
dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class DataWidget(QWidget):
	def __init__(self, label=None, action=None, parent=None, options_layout=None):
		super(DataWidget, self).__init__()
		self.action = action
		self.options_layout = options_layout
		self.dataMainLayout = QHBoxLayout()
		self.dataMainLayout.setAlignment(Qt.AlignLeft)
		self.dataMainLayout.setContentsMargins(0,2,0,2)

		self.setAutoFillBackground(True)
		self.p = self.palette()
		self.inActiveColor = QColor(BUTTON_INACTIVE_COLOR[0], BUTTON_INACTIVE_COLOR[1], BUTTON_INACTIVE_COLOR[2])
		self.hoverColor = QColor(SCROLLAREA_COLOR[0], SCROLLAREA_COLOR[1], SCROLLAREA_COLOR[2], SCROLLAREA_COLOR[3])
		self.p.setColor(self.backgroundRole(), self.inActiveColor)
		self.setPalette(self.p)
		self.active = False

		self.button = QPushButton( self)
		self.button.setObjectName('icon_button')
		self.button.setVisible(True)
		self.button.setIcon(QIcon(os.path.join(dir, 'lib', action, 'icon.svg')))
		self.button.setIconSize(QSize(22, 22))
		self.button.setStyleSheet("QPushButton {border:0px; background: rgb(0, 0, 0, 0);}")

		self.label = QLabel(label, self)
		self.label.setStyleSheet("color: white;");

		self.dataMainLayout.addWidget(self.button)
		self.dataMainLayout.addWidget(self.label)
		self.setLayout(self.dataMainLayout)

	# todo refactor this
	def mousePressEvent(self, e):
		# print('===', LIBS + self.action + '.main as action')
		exec(LIBS + self.action + '.main as action')
		exec('self.action_ui = MTS.lib.' + self.action + '.main.ToolOptions()')
		# self.action_ui = action.ToolOptions()

		if e.button() == Qt.LeftButton:
			#print("Left Button Clicked")
			self.action_ui.main()

		elif e.button() == Qt.RightButton:
			#print("Right Button Clicked")
			self.clearLayout()
			self.options_layout.addWidget(self.action_ui)

	def clearLayout(self):
		for i in range(0, self.options_layout.count()):
			widget = self.options_layout.itemAt(i)
			item = widget.widget()
			name = item.objectName()
			item.deleteLater()

	def setIconSize(self, size):
		self.button.setIconSize(QSize(size, size))

	def event(self, event):
		if event.type() == 10:
			self.p.setColor(self.backgroundRole(), self.hoverColor)
			self.setPalette(self.p)

		if event.type() == 11:
			self.p.setColor(self.backgroundRole(), self.inActiveColor)
			self.setPalette(self.p)

		return QWidget.event(self, event)
		# return True
