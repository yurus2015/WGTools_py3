from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import modelingToolset.lib.uvChecker.utils.util as Util
import maya.cmds as cmds


class RadioButton(QRadioButton):
    def __init__(self, value, checked=False):
        super(RadioButton, self).__init__(value)
        self.setChecked(checked)


class RadioDimensionLayout(QGridLayout):
    def __init__(self, parent=None):
        super(RadioDimensionLayout, self).__init__()
        self.setAlignment(Qt.AlignLeft)
        dimension_start = 4
        dimension_count = 4
        uv_sets_count = 3

        dimension_group = QButtonGroup(self)
        sets_group = QButtonGroup(self)

        for i in range(dimension_count):
            button = RadioButton(str(dimension_start * 128), not i)
            button.toggled.connect(self.change_dimension)
            button.dim = dimension_start
            dimension_start = dimension_start * 2
            dimension_group.addButton(button)
            self.addWidget(button, 0, i)

        for i in range(uv_sets_count):
            button = RadioButton('map' + str(i + 1), not i)
            button.toggled.connect(self.change_uvset)
            button.uv = str(i)
            sets_group.addButton(button)
            self.addWidget(button, 1, i)

    def change_dimension(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            print("Dimension is %s" % radio_button.dim)
            Util.assign_checker_texture(iterator=radio_button.dim)

    def change_uvset(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            print("UVSet is %s" % radio_button.uv)
            Util.assign_checker_texture(uvset=radio_button.uv)
