from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as omu
from shiboken2 import wrapInstance
from skinning_tools.gui.vs_constants import MAIN_WINDOW_NAME
from skinning_tools.gui.vs_menu_toolbars import VSMenuBar, VSToolBarTools, VSToolBarSystem, VSToolBarItems
from skinning_tools.gui.vs_editor_widget import VSEditorWidget


# create parent to maya main window
def main_window_pointer():
    point = omu.MQtUtil.mainWindow()
    return wrapInstance(int(point), QWidget)


# create maya main window class
class STMainWindow(QMainWindow):
    def __init__(self, parent=main_window_pointer()):
        super(STMainWindow, self).__init__(parent)
        self.setObjectName('SkinningToolsWindow')
        self.setWindowTitle(MAIN_WINDOW_NAME)
        self.setGeometry(200, 200, 800, 600)
        self.create_ui()
        self.tool_bars_ui()

    def create_ui(self):
        self.statusBar().showMessage('Opanki!')

        # crate menu bar
        self.menu_bar = VSMenuBar()
        self.setMenuBar(self.menu_bar)

        # Create central widget
        self.editor = VSEditorWidget()
        self.setCentralWidget(self.editor)

    def tool_bars_ui(self):
        # create tool bars
        self.tool_bar = VSToolBarTools()
        self.addToolBar(Qt.LeftToolBarArea, self.tool_bar)
        self.tool_bar.setAllowedAreas(Qt.LeftToolBarArea | Qt.RightToolBarArea)

        self.system_bar = VSToolBarSystem()
        self.addToolBar(Qt.TopToolBarArea, self.system_bar)
        self.system_bar.setAllowedAreas(Qt.TopToolBarArea)

        self.item_bar = VSToolBarItems()
        self.addToolBar(Qt.TopToolBarArea, self.item_bar)
        self.item_bar.setAllowedAreas(Qt.TopToolBarArea)

    # Save settings window
    def closeEvent(self, event):
        settings = QSettings('Opanki', 'SkinningTools')  # what is it?
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('windowState', self.saveState())
        QMainWindow.closeEvent(self, event)

    # Load settings window
    def showEvent(self, event):
        settings = QSettings('Opanki', 'SkinningTools')  # what is it?
        self.restoreGeometry(settings.value('geometry'))
        self.restoreState(settings.value('windowState'))
        QMainWindow.showEvent(self, event)
