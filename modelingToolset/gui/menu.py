from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import maya.cmds as cmds
import os
import subprocess

from .constants import MENU, AUTORUN, AUTORUNOPTIONS

class MenuBar(QMenuBar):
	def __init__(self, parent=None):
		super(MenuBar, self).__init__()
		self.setObjectName('toolset_menu_bar')

		self.options_menu = self.addMenu(MENU[0])
		self.about_menu = QAction(MENU[1], self)
		self.autorun_submenu = QAction(AUTORUN, self, checkable=True, triggered = self.save_options)
		self.options_menu.addAction(self.autorun_submenu)
		self.addAction(self.about_menu)

		self.aboutWindow = False

		self.set_options()


	def showAbout (self):
		if not self.aboutWindow:
			self.aboutWindow = aboutWindow()
			self.aboutWindow.show()
		else:
			self.aboutWindow.show()


	def set_options(self):
		self.autorun_submenu.setChecked(cmds.optionVar(q = AUTORUNOPTIONS))


	def save_options(self):
		cmds.optionVar(iv = (AUTORUNOPTIONS, self.autorun_submenu.isChecked()))


	def svn_revision(self):
		current_dir = os.path.dirname(os.path.realpath(__file__)).lower()
		svn = current_dir.split('devtools')[0] +'devtools\\svn\\svn_1.9\\wgta-svn.exe'
		print(svn)
		print(os.path.dirname(os.path.realpath(__file__)))
		rev = ' rev.' + subprocess.Popen(svn + " info --show-item=last-changed-revision " + current_dir, shell=True, stdout=subprocess.PIPE).stdout.read()
		print('REVISION: ' + rev)