# -*- coding: utf-8 -*-
import os
import maya.OpenMayaUI as Omu
from shiboken2 import wrapInstance
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import maya.cmds as cmds
import sys
import importlib
import modelingToolset.lib.uvChecker.gui.widgets

importlib.reload(modelingToolset.lib.uvChecker.gui.widgets)
from modelingToolset.lib.uvChecker.gui.widgets import *


class ToolOptions(QWidget):
    def __init__(self, parent=None):
        super(ToolOptions, self).__init__(parent)

        self.central_layout = QVBoxLayout()
        self.central_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.central_layout.setSpacing(5)
        self.central_layout.setContentsMargins(0, 0, 0, 5)
        self.setLayout(self.central_layout)

        self.radio_widget = WidgetRadioButtons()
        self.icon_widget = WidgetCamouflage()
        self.restore_widget = WidgetRestoreButton()
        self.central_layout.addWidget(self.radio_widget)
        self.central_layout.addWidget(self.icon_widget)
        self.central_layout.addWidget(self.restore_widget)
