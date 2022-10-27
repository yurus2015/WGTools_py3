from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import os

description = "Runs Validator"
buttonType = "opt"
beautyName = "Validator"
iconName = "Validator"


class ToolOptions(QWidget):

    def __init__(self, parent=None):
        super(ToolOptions, self).__init__(parent)

        self.setLayout(self.createUI())

    def createUI(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(5)  # layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.label = QLabel("<b>Description:</b><p>Press the icon to run Validator</p>")

        self.mainLayout.addWidget(self.label)

        return self.mainLayout

    # @classmethod
    def main(self):
        import validator.main as vld
        vld.main(autoload=False)
