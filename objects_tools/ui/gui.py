import importlib
import os
import posixpath
import re
import maya.OpenMayaUI as omu
from shiboken2 import wrapInstance

import objects_tools.export as OE
import objects_tools.ui.dockWidgets as docks

importlib.reload(docks)
import objects_tools.ui.centralWidget as central

importlib.reload(central)

from objects_tools.ui.dockWidgets import *
from objects_tools.ui.centralWidget import *

WIDTH = 400
HEIGHT = 100
CURRENT_FILE = os.path.dirname(os.path.abspath(__file__))


def main_window_pointer():
    ptr = omu.MQtUtil.mainWindow()  # pointer for the main window
    return wrapInstance(int(ptr), QWidget)


class MainObjectsWindow(QMainWindow):
    def __init__(self, parent=main_window_pointer()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle("Objects Tools")
        self.setObjectName("MainObjectWnd")
        self.setTabPosition(Qt.AllDockWidgetAreas, QTabWidget.North)
        self.setDockOptions(QMainWindow.AnimatedDocks | QMainWindow.AllowNestedDocks |
                            QMainWindow.AllowTabbedDocks | QMainWindow.GroupedDragging)
        self.setMouseTracking(True)

        self.central_widget = ObjectsCentralWidget()
        self.setCentralWidget(self.central_widget)

        self.validator_dock = ValidatorDock('Validator(Coming soon)')
        self.addDockWidget(self.validator_dock.default_dock_area(), self.validator_dock)
        self.console_dock = ConsoleDock('Console')
        self.addDockWidget(self.console_dock.default_dock_area(), self.console_dock)
        self.tabifyDockWidget(self.validator_dock, self.console_dock)

        # save position window
        self.settings = QSettings("MainObjectWnd")
        if not self.settings.value("geometry") is None:
            self.restoreGeometry(self.settings.value("geometry"))

        self.read_settings()

    def closeEvent(self, event):
        # restore position window
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue('windowState', self.saveState())

    def read_settings(self):
        self.restoreGeometry(self.settings.value("geometry"))
        self.restoreState(self.settings.value("windowState"))

    def get_console(self):
        return self.console_dock


class BranchSelectionWnd(QDialog):
    def __init__(self, parent=main_window_pointer()):
        QDialog.__init__(self, parent)

        # self.setFixedSize(WIDTH, HEIGHT)
        self.setWindowTitle("Objects Export Branch")
        self.setModal(False)
        self.setWindowFlags(Qt.Window)
        self.setObjectName("BranchSelection")

        # save position window
        self.settings = QSettings("BranchSelection")
        if not self.settings.value("geometry") is None:
            self.restoreGeometry(self.settings.value("geometry"))

        Utils.load_option_var()

        """Adding"""
        self.main_vertical_layout = QVBoxLayout(self)
        # todo all frames in custom class
        self.export_frame = QFrame()
        self.export_frame.setFrameShape(QFrame.StyledPanel)
        self.havok_frame = QFrame()
        self.havok_frame.setFrameShape(QFrame.StyledPanel)
        # self.export_frame.setFrameShadow(QFrame.Shadow)
        self.main_vertical_layout.addWidget(self.export_frame)
        self.main_vertical_layout.addWidget(self.havok_frame)

        # self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        trank_list = self.trank_list()
        buttons_layout = self.buttons_layout()
        main_layout.addWidget(trank_list)
        main_layout.addLayout(buttons_layout)

    def trank_list(self):
        # self.pathes = Utils.editXML()
        # d:\ART_MAIN\game\bin\tools\devtools\scripts\maya2018\wargamingMenu\options\objectExporter\
        posixpath.join(CURRENT_FILE, 'delete_path.svg')
        self.pathes = Utils.load_option_var()
        self.trank_Combo = QComboBox()
        self.trank_Combo.setFixedHeight(22)
        self.trank_Combo.setObjectName('customTrankCombo')
        self.trank_Combo.currentIndexChanged.connect(self.save_current_path)
        self.buttonDir = self.init_button(command=lambda: self.dir_browser())
        self.buttonDir.setFixedWidth(20)
        self.buttonDir.setFixedHeight(20)
        self.icon_add = QIcon(posixpath.join(CURRENT_FILE, 'add_path.svg'))
        self.buttonDir.setIcon(self.icon_add)
        self.buttonDir.setIconSize(QSize(18, 18))
        self.buttonDir.setStyleSheet("QPushButton {border:0px; background: rgb(0, 0, 0, 0);}")
        self.delete_path = self.init_button(command=lambda: self.delete_trunk())
        self.delete_path.setFixedWidth(20)
        self.delete_path.setFixedHeight(20)
        self.icon_del = QIcon(posixpath.join(CURRENT_FILE, 'delete_path.svg'))
        self.delete_path.setIcon(self.icon_del)
        self.delete_path.setIconSize(QSize(18, 18))
        self.delete_path.setStyleSheet("QPushButton {border:0px; background: rgb(0, 0, 0, 0);}")
        self.trank_Layout = ComboBoxLayout(self.trank_Combo, self.buttonDir, self.delete_path)

        current_branch = cmds.optionVar(q='current_branch')
        self.pathes = Utils.load_option_var()

        if self.pathes:
            for i in range(len(self.pathes)):
                self.trank_Combo.addItem(self.pathes[i])
                if current_branch == self.pathes[i]:
                    self.trank_Combo.setCurrentIndex(i)

        return self.trank_Layout

    def save_current_path(self):
        Utils.save_option_var(self.trank_Combo.currentText())

    def init_button(self, parent=None, title="", command=None, h=None):
        self._button = QPushButton(title)
        if command:
            self._button.clicked.connect(command)

        return self._button

    def buttons_layout(self):
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignRight)
        self.export_btn = self.init_button(self, title='Export', h=60, command=lambda: self.export_selected_trunk())
        self.export_btn.setToolTip("Export objects")
        self.export_btn.setFixedWidth(100)
        self.close_btn = self.init_button(self, title='Close', command=lambda: close_window(), h=60)
        self.close_btn.setToolTip("Close dialog")
        self.close_btn.setFixedWidth(100)
        self.buttons_layout.addWidget(self.export_btn)
        self.buttons_layout.addWidget(self.close_btn)
        return self.buttons_layout

    def dir_browser(self):  # open browser to set export path
        bpath = None
        try:
            bpath = cmds.fileDialog2(fm=3, dialogStyle=1)[0]
        except ValueError:
            pass

        if not bpath:
            return

        if bpath and 'content' in bpath:
            if bpath not in self.pathes:
                self.trank_Combo.addItem(bpath)
                self.trank_Combo.setCurrentIndex(self.trank_Combo.count() - 1)
                self.pathes.append(bpath)
                Utils.save_option_var(bpath, delete=False)
        else:
            cmds.confirmDialog(title='Warning', message='Select "content*" dir in your branch',
                               button=['   OK   '], defaultButton='   OK   ')

    def delete_trunk(self):
        indx = self.trank_Combo.currentIndex()
        bpath = self.trank_Combo.currentText()
        self.trank_Combo.removeItem(indx)
        # self.save_current_path(bpath, delete=True)
        Utils.save_option_var(self.trank_Combo.currentText(), True)

    # Utils.editXML(bpath, True)

    def export_selected_trunk(self):
        bpath = self.trank_Combo.currentText()
        print('External path:', bpath)
        if os.path.exists(bpath):
            print('Path exists:', bpath)
            # wtite to xml a parent directory of ../content*
            parent_path = re.split('/content', bpath)[0]
            Utils.edit_xml(parent_path)
            OE.main(bpath)
            Utils.edit_xml(parent_path, True)
        else:
            cmds.confirmDialog(title='Warning', message='Directory "' + bpath + '" does not exist',
                               button=['   OK   '], defaultButton='   OK   ')


class ComboBoxLayout(QWidget):

    def __init__(self, *args, **kwargs):
        QWidget.__init__(self)
        # self.setContentsMargins(0, 0, 0, 0)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        for arg in args:

            if type(arg) == type(list()):
                for i in arg:
                    layout.addWidget(i)
            else:
                try:
                    layout.addLayout(arg)
                except Exception:
                    layout.addWidget(arg)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            print("Left Button Clicked")
        elif QMouseEvent.button() == Qt.RightButton:
            print("Right Button Clicked")


def close_window():
    if cmds.window("BranchSelection", q=True, exists=True):
        cmds.deleteUI("BranchSelection")
    try:
        cmds.deleteUI('MayaWindow|BranchSelection')
    except:
        pass


def delete_window():
    if cmds.window("MainObjectWnd", q=True, exists=True):
        cmds.deleteUI("MainObjectWnd")
    try:
        cmds.deleteUI('MayaWindow|MainObjectWnd')
    except Exception:
        pass


def main():
    delete_window()
    maya_window = main_window_pointer()
    window = MainObjectsWindow(maya_window)
    window.show()
