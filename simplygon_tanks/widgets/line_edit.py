#from PySide import QtCore, QtGui
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

import maya.cmds as cmds
import os
#import maya.utils as utils

#import base

class SG_LineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        QLineEdit.__init__(self, *args, **kwargs)


class SG_ButtonLineEdit(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)


class SG_Browser(QHBoxLayout):
    def __init__(self, *args, **kwargs):
        QHBoxLayout.__init__(self)

        self.button = SG_ButtonLineEdit()
        self.button.setText(args[0])
        self.button.setMinimumWidth(args[1])
        self.button.setMaximumHeight(args[2])

        if args[3] == 'dir':
            self.button.clicked.connect(self.choose_directory)
        else:
            self.button.clicked.connect(self.choose_file)
        self.addWidget(self.button)

        self.line = SG_LineEdit()
        self.line.setObjectName(args[0].replace(' ',''))
        self.addWidget(self.line)
        self.line.setMinimumWidth(300)


    def choose_directory(self):
        """
        Opens a file dialog and sets the file text box to the chosen texture.
        """
        mayaFileName=cmds.file( q=True, loc=True)
        filePath=os.path.dirname(mayaFileName)
        #dirname = self.get_default_directory()
        dirname = QFileDialog.getExistingDirectory(None, 'Choose Directory', filePath, options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks | QFileDialog.ReadOnly)
        if os.path.exists(dirname):    # avoids problems if <Cancel> was selected
            self.line.setText(str(dirname))

    def choose_file(self):
        """
        Opens a file dialog and sets the file text box to the chosen track texture.
        """
        mayaFileName=cmds.file( q=True, loc=True)
        filePath=os.path.dirname(mayaFileName)
        #dirname = self.get_default_directory()
        filename = QFileDialog.getOpenFileName(None, 'Choose Track texture', filePath, "Image Files (*.tga)", options= QFileDialog.DontResolveSymlinks | QFileDialog.ReadOnly)
        if os.path.isfile(filename[0]):    # avoids problems if <Cancel> was selected
            self.line.setText(str(filename[0]))






