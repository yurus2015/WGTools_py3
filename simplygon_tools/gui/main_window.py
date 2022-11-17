import maya.OpenMayaUI as omu
import maya.cmds as cmds
from shiboken2 import wrapInstance
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import simplygon_tools.utils.fbx as fbx
import simplygon_tools.utils.baker as baker
import simplygon_tools.utils.utilites as utl
from simplygon_tools.utils.utilites import Settings
from simplygon_tools.utils.constants import *

SUFFIX = (('AM', True),
          ('GM', True),
          ('AO', True),
          ('NM', True),
          ('MM', True),
          ('CM', False),
          ('BM', False),
          ('DM', False))


def main_window_pointer():
    point = omu.MQtUtil.mainWindow()
    return wrapInstance(int(point), QWidget)


class TanksWindow(QDialog):
    def __init__(self):
        super(TanksWindow, self).__init__()

        self.setParent(main_window_pointer())
        self.setWindowFlags(Qt.Window)
        self.setObjectName('SimplygonTanksWindow')
        self.setWindowTitle('Simplygon Tools: Tanks')
        self.setFixedHeight(300)

        self.init_ui()
        self.script_jons_start()
        self.save_position_window()
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

    def save_position_window(self):
        self.settings = QSettings('SimplygonTanksWindow')
        if self.settings.value('geometry') is not None:
            self.restoreGeometry(self.settings.value('geometry'))

    def closeEvent(self, event):
        self.settings.setValue('geometry', self.saveGeometry())

        # kill scriptJobs
        cmds.scriptJob(k=self.sj_open_scene, force=True)
        cmds.scriptJob(k=self.sj_change_selection, force=True)
        cmds.scriptJob(k=self.sj_change_name, force=True)

    def script_jons_start(self):
        self.sj_open_scene = cmds.scriptJob(e=["SceneOpened", self.calculate_polycount], p="SimplygonTanksWindow")
        self.sj_change_selection = cmds.scriptJob(e=["SelectionChanged", self.calculate_polycount],
                                                  p="SimplygonTanksWindow")
        self.sj_change_name = cmds.scriptJob(e=["NameChanged", self.calculate_polycount], p="SimplygonTanksWindow")

    def calculate_polycount(self):
        print('N', )
        table = self.simplygon_box.table()
        table.read_settings()
        # utl.calculate_polycount()
        # row = 1
        # for col in range(1, 5):
        #     item = table.item(row, col)
        #     item.setText(str(Settings.lods_calculate[col-1]))
        #
        # item = table.item(2, 1)
        # item.setText(str(Settings.lods_calculate[0]))


class TanksHorizontalLayout(QHBoxLayout):
    def __init__(self, parent=None):
        super(TanksHorizontalLayout, self).__init__(parent)
        self.setSpacing(3)
        self.setContentsMargins(5, 10, 5, 5)


class TanksVerticalLayout(QVBoxLayout):
    def __init__(self, parent=None):
        super(TanksVerticalLayout, self).__init__(parent)
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
        self._import_button.clicked.connect(fbx.export_selection)

        self._layout.addWidget(self._lod_button)
        self._layout.addWidget(self._proxy_button)
        self._layout.addWidget(self._import_button)
        self.setLayout(self._layout)

    def test(self):
        pass


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
        # self.setWordWrap(0)
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
        reduce_button_auto._reduce_button.clicked.connect(lambda: fbx.main_commands())
        self.setCellWidget(1, 6, reduce_button_auto)
        reduce_button_manual = TanksReduceButton()
        reduce_button_manual._reduce_button.clicked.connect(lambda: fbx.main_commands(True))
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

        for i in range(len(SUFFIX)):
            check_box = QCheckBox(SUFFIX[i][0])
            check_box.setObjectName(SUFFIX[i][0])
            check_box.setChecked(SUFFIX[i][1])
            self._check_box_layout.addWidget(check_box)

        self.setLayout(self._layout)
