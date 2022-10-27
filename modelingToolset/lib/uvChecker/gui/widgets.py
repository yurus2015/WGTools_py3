from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import importlib
import os
import modelingToolset.lib.uvChecker.utils.util as Util

importlib.reload(Util)
import modelingToolset.lib.uvChecker.gui.buttons

importlib.reload(modelingToolset.lib.uvChecker.gui.buttons)
from modelingToolset.lib.uvChecker.gui.buttons import ButtonAdd, ButtonCamouflage

import modelingToolset.lib.uvChecker.gui.radio

importlib.reload(modelingToolset.lib.uvChecker.gui.radio)
from modelingToolset.lib.uvChecker.gui.radio import RadioDimensionLayout

current_dir = os.path.dirname(os.path.abspath(__file__))

myMimeType = "application/MyWindow"


class GridCamouflage(QGridLayout):
    def __init__(self):
        super(GridCamouflage, self).__init__()
        self.row = 4
        self.column = 4
        self.setSpacing(5)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.read_yaml()

    def read_yaml(self):  # todo refactor
        self.counts = self.count()
        self.row_position = 0
        self.column_position = 0

        def override_position():
            self.counts = self.count()
            self.row_position = self.counts // self.row
            self.column_position = self.counts % self.column

        icons = Util.read_yaml(current_dir, 'icons')
        if icons:
            for i in icons:
                override_position()
                camouflage_button = ButtonCamouflage(i, None)
                camouflage_button.set_grid(self)
                self.addWidget(camouflage_button, self.row_position, self.column_position)

        override_position()
        self.main_button = ButtonAdd('add', None)  # todo add icon
        self.main_button.set_grid(self)
        self.addWidget(self.main_button, self.row_position, self.column_position)
        # print(self.row_position, self.column_position)

    def save_yaml(self):
        icons = self.all_camouflage_buttons()
        print('Icons for save in yaml', icons)
        Util.write_yaml(current_dir, icons)

    def all_camouflage_buttons(self):
        count = self.count()
        icons = []
        for i in range(count):
            button = self.itemAt(i).widget()
            if isinstance(button, ButtonCamouflage):
                _icon = button.get_icon()
                if _icon:
                    icons.append(button.get_icon())
        return icons

    def adding_item(self, icon=None):
        i = self.count()
        row_position = (i - 1) // self.row
        column_position = (i - 1) % self.column
        camouflage_button = ButtonCamouflage(icon, None)
        camouflage_button.set_grid(self)  # send parent layer
        self.addWidget(camouflage_button, row_position, column_position)
        # print(row_position, column_position)
        self.addWidget(self.main_button, i // self.row, i % self.column)

    def reformat_items(self):
        count = self.count()
        row = self.rowCount()
        column = self.columnCount()
        widgets = []
        for i in (range(count)):
            w = self.itemAt(i).widget()
            widgets.append(w)
        try:
            index = 0
            for x in range(row):
                for y in range(column):
                    self.addWidget(widgets[index], x, y)
                    index += 1
        except IndexError:
            pass

    def get_position(self, item):
        index = self.get_index(item)
        return self.getItemPosition(index)

    def get_index(self, item):
        return self.indexOf(item)


class WidgetCamouflage(QWidget):
    def __init__(self, parent=None):
        super(WidgetCamouflage, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setMouseTracking(True)  # todo check necessary

        self.grid = GridCamouflage()
        self.setLayout(self.grid)


class WidgetRadioButtons(QWidget):
    def __init__(self, parent=None):
        super(WidgetRadioButtons, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)
        self.dimension_layout = RadioDimensionLayout()

        self.setLayout(self.dimension_layout)


class WidgetRestoreButton(QWidget):
    def __init__(self, parent=None):
        super(WidgetRestoreButton, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        button = QPushButton('Restore')
        button.setFixedSize(215, 22)
        button.clicked.connect(Util.restore)

        self.setLayout(layout)
        layout.addWidget(button)
