import maya.OpenMayaUI as omu
import maya.cmds as cmds
import logging

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from shiboken2 import wrapInstance
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import simplygon_tools.utils.fbx as fbx
import simplygon_tools.utils.baker as baker
import simplygon_tools.utils.utilites as utl
from ..utils.utilites import Settings
from ..utils.constants import *


def main_window_pointer():
    point = omu.MQtUtil.mainWindow()
    return wrapInstance(int(point), QWidget)


class MayaWindow(QDialog):
    def __init__(self, parent=main_window_pointer(), window_name=None, window_title=None):
        super(MayaWindow, self).__init__(parent=parent)
        self.window_name = window_name
        self.window_title = window_title
        self.setWindowFlags(Qt.Window)
        self.setObjectName(self.window_name)
        self.setWindowTitle(self.window_title)
        self.save_position_window()

        # I request from class
        print(f'I request from class {self.__class__}')

    def save_position_window(self):
        self.settings = QSettings(self.window_name)
        if self.settings.value('geometry') is not None:
            self.restoreGeometry(self.settings.value('geometry'))

    def closeEvent(self, event):
        self.settings.setValue('geometry', self.saveGeometry())


class TanksWindow(MayaWindow):
    def __init__(self):
        super().__init__(window_name='SimplygonTanksWindow', window_title='Simplygon Tools: Tanks')
        self.setFixedHeight(310)

        self.init_ui()
        self.script_jobs_start()
        self.calculate_polycount()
        utl.load_plugin('techartAPI')
        utl.load_plugin('fbxmaya')

    def init_ui(self):
        self.central_layout = QVBoxLayout(self)
        self.central_layout.setSpacing(10)
        self.central_layout.setContentsMargins(10, 15, 10, 15)
        self.central_layout.setAlignment(Qt.AlignTop)

        self.simplygon_box = TanksReduceBlock('Simplygon calculator')
        self.texture_box = TanksTextureBlock('Bake proxy textures')
        self.tools_box = TanksToolsBlock('Tools')

        # parenting widgets
        self.central_layout.addWidget(self.simplygon_box)
        self.central_layout.addWidget(self.texture_box)
        self.central_layout.addWidget(self.tools_box)

    def closeEvent(self, event):
        self.settings.setValue('geometry', self.saveGeometry())

        # Delete script jobs
        for event in self.script_jobs:
            cmds.scriptJob(k=event, force=True)

    def script_jobs_start(self):
        self.script_jobs = []
        events = ['SceneOpened', 'SelectionChanged', 'NameChanged']
        for event in events:
            self.script_jobs.append(cmds.scriptJob(event=[event, self.calculate_polycount], p=self.window_name))

    def calculate_polycount(self):
        print('N', )
        table = self.simplygon_box.table()
        table.read_settings()


class TanksHorizontalLayout(QHBoxLayout):
    def __init__(self, parent=None):
        super(TanksHorizontalLayout, self).__init__()
        self.setSpacing(3)
        self.setContentsMargins(5, 10, 5, 5)


class TanksVerticalLayout(QVBoxLayout):
    def __init__(self, parent=None):
        super(TanksVerticalLayout, self).__init__()
        self.setSpacing(3)
        self.setContentsMargins(5, 10, 5, 5)


class TanksGroupBox(QGroupBox):
    def __init__(self, title=None):
        super(TanksGroupBox, self).__init__(title)
        self.setTitle(title)
        self.setStyleSheet("QGroupBox {border: 1px solid #8C8C8C;margin-top: 0.5em;} "
                           "QGroupBox::title {top: -8px;left: 18px;}")


class TanksReduceBlock(TanksGroupBox):
    def __init__(self, *args):
        super().__init__(*args)
        self._layout = TanksVerticalLayout()
        self._table = TanksTable()
        self._layout.addWidget(self._table)
        self.setLayout(self._layout)

    def table(self):
        return self._table


class TanksToolsBlock(TanksGroupBox):
    def __init__(self, *args):
        super().__init__(*args)
        self._layout = TanksHorizontalLayout()
        # buttons
        self._lod_button = TanksButton(label='Create lods hierarchy')
        self._lod_button.clicked.connect(utl.create_hierarchy)
        self._proxy_button = TanksButton(label='Proxy lod generate')
        self._proxy_button.clicked.connect(fbx.export_selection)
        self._import_button = TanksButton(label='Import proxy lod')
        self._import_button.clicked.connect(utl.color_picker)

        self._layout.addWidget(self._lod_button)
        self._layout.addWidget(self._proxy_button)
        self._layout.addWidget(self._import_button)
        self.setLayout(self._layout)


class TanksButton(QPushButton):
    def __init__(self, label=None, icon=None, width=None, checkable=False, *args, **kwargs):
        super(TanksButton, self).__init__(*args, **kwargs)
        self.setText(label)


class TanksTable(QTableWidget):
    def __init__(self):
        super(TanksTable, self).__init__(3, 7)
        self.horizontalHeader().setVisible(0)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.verticalHeader().setVisible(0)
        self.verticalHeader().setDefaultSectionSize(25)

        self.setMinimumWidth(550)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAlternatingRowColors(1)

        self.setDragDropOverwriteMode(False)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setTextElideMode(Qt.ElideNone)
        self.setWordWrap(False)
        self.setCornerButtonEnabled(False)
        self.setObjectName("simplygonTab")

        self.black_background_brush = QBrush(QColor(10, 10, 10, 255))
        self.gray_background_brush = QBrush(QColor(30, 30, 30, 255))
        self.white_text_brush = QBrush(QColor(255, 255, 255, 255))
        self.green_text_brush = QBrush(QColor(200, 255, 200, 255))
        self.blue_text_brush = QBrush(QColor(200, 200, 255, 255))

        for row in range(0, 3):
            for col in range(0, 7):
                item = TanksTableCell(self.gray_background_brush)
                self.setItem(row, col, item)

        reduce_button_auto = TanksReduceButton()
        reduce_button_auto._reduce_button.clicked.connect(lambda: fbx.main_commands(1, 5))
        self.setCellWidget(1, 6, reduce_button_auto)
        reduce_button_manual = TanksReduceButton()
        reduce_button_manual._reduce_button.clicked.connect(lambda: fbx.main_commands(1, 5, True))
        self.setCellWidget(2, 6, reduce_button_manual)

        self.colorize_background()
        self.empty_cell()
        self.color_text()
        self.naming_cell()
        self.non_editable()
        self.read_settings()
        self.cellChanged.connect(self.write_settings)

    def colorize_background(self):
        row = 0
        for col in range(0, 7):
            item = self.item(row, col)
            item.setBackground(self.black_background_brush)
        col = 0
        for row in range(1, 3):
            item = self.item(row, col)
            item.setBackground(self.black_background_brush)

    def naming_cell(self):
        row = 0
        lod_name = ('', 'lod0', 'lod1', 'lod2', 'lod3', 'lod4', '')
        for col in range(1, 6):
            item = self.item(row, col)
            item.setText(lod_name[col])
            item.setForeground(self.white_text_brush)

        col = 5
        for row in range(1, 3):
            item = self.item(row, col)
            item.setText('proxy')

        item = self.item(1, 0)
        item.setText('Auto')
        item.setForeground(self.green_text_brush)

        item = self.item(2, 0)
        item.setText('Manual')
        item.setForeground(self.green_text_brush)

        row = 2
        for col in range(2, 5):
            item = self.item(row, col)
            item.setText('Enter value')

    def empty_cell(self):
        for row in range(1, 3):
            for col in range(1, 5):
                item = self.item(row, col)
                item.setText('-')
                item.setForeground(self.green_text_brush)

    def color_text(self):
        row = 1
        for col in range(0, 5):
            item = self.item(row, col)
            item.setForeground(self.blue_text_brush)

    def non_editable(self):
        for row in range(0, 2):
            for col in range(0, 7):
                item = self.item(row, col)
                item.setFlags(Qt.ItemIsEditable)

        item = self.item(2, 0)
        item.setFlags(Qt.ItemIsEditable)

        item = self.item(2, 1)
        item.setFlags(Qt.ItemIsEditable)

        item = self.item(2, 5)
        item.setFlags(Qt.ItemIsEditable)

        item = self.item(2, 6)
        item.setFlags(Qt.ItemIsEditable)

    def read_settings(self):
        print('M', Settings.manual_polycount)
        utl.calculate_polycount()
        row = 1
        for col in range(1, 5):
            item = self.item(row, col)
            item.setText(str(Settings.lods_calculate[col - 1]))

        item = self.item(2, 1)
        item.setText(str(Settings.lods_calculate[0]))

    def write_settings(self, row, column):
        print('Write', row, column)

        # only for manual
        # column from 2 to 4
        # settings from 0 to 2
        item = self.item(2, column)
        if item.text().isdigit():
            Settings.lods_manual[column - 2] = item.text()
            print('Item text', item.text(), ' in ', column - 2)
        else:
            print('ERROR: enter only digits')
            item.setText('Enter value')
            Settings.lods_manual[column - 2] = item.text()


class TanksTableCell(QTableWidgetItem):
    def __init__(self, b_color=None):
        super(TanksTableCell, self).__init__()
        self.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
        self._background_color = b_color
        self.setBackground(self._background_color)


class TanksReduceButton(QWidget):
    def __init__(self):
        super(TanksReduceButton, self).__init__()
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._reduce_button = QPushButton("&Reduce")
        # self._reduce_button.clicked.connect(fbx.main_commands)  # simplygon command
        self._layout.addWidget(self._reduce_button, Qt.AlignHCenter | Qt.AlignVCenter)


# todo
'''
# вынести в отдельный модуль
'''


class TanksTextureBlock(TanksGroupBox):
    def __init__(self, *args):
        super().__init__(*args)
        self._layout = TanksVerticalLayout()
        self._original_textures_layout = TanksHorizontalLayout()
        self._suffix_layout = TanksHorizontalLayout()
        self._suffix_layout.setAlignment(Qt.AlignLeft)
        self._check_box_layout = TanksHorizontalLayout()
        self._layout.addLayout(self._original_textures_layout)
        self._layout.addLayout(self._suffix_layout)

        self._button = TanksButton(label='Texture dir')
        self._button.setMaximumHeight(20)
        self._button.clicked.connect(baker.test)
        self._line = QLineEdit()
        self._original_textures_layout.addWidget(self._button)
        self._original_textures_layout.addWidget(self._line)

        self._button_bake = TanksButton(label='Bake proxy')
        self._button_bake.setMaximumHeight(20)
        self._button_bake.clicked.connect(fbx.export_selection)
        self._suffix_layout.addWidget(self._button_bake)
        self._suffix_layout.addLayout(self._check_box_layout)

        for i in SUFFIX:
            check_box = QCheckBox(i)
            check_box.setObjectName(i)
            check_box.setChecked(SUFFIX.get(i))
            self._check_box_layout.addWidget(check_box)

        self.setLayout(self._layout)


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class LogWindow(MayaWindow, QPlainTextEditLogger):
    def __init__(self):
        super(LogWindow, self).__init__()
        self.setWindowFlags(Qt.Window)
        self.setObjectName('SimplygonLog')
        self.setWindowTitle('Simplygon Tools: Log')

        self.log_text_box = QPlainTextEditLogger(self)
        # You can format what is printed to text box
        self.log_text_box.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(self.log_text_box)
        # You can control the logging level
        logging.getLogger().setLevel(logging.DEBUG)

        self._button = QPushButton(self)
        self._button.setText('Test Meee-e')

        layout = QVBoxLayout()
        # Add the new logging box widget to the layout
        layout.addWidget(self.log_text_box.widget)
        layout.addWidget(self._button)
        self.setLayout(layout)

        # Connect signal to slot
        self._button.clicked.connect(self.test)

    def test(self):
        logging.debug('damn, a bug')
        logging.info('something to remember')
        logging.warning('that\'s not right')
        logging.error('foobar')

# create dockable window using workspaceControl and MayaMixin
