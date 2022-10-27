from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import importlib
import objects_tools.ui.console as Console

importlib.reload(Console)

style = """
QDockWidget {
border: 5px solid lightgray;
    titlebar-close-icon: url(d:/Development/WG/DevTools2022/scripts/py3/objects_tools/ui/images/delete.png);
    titlebar-normal-icon: url(undock.png);
}

QDockWidget::title {
    text-align: left; /* align the text to the left */
    background: black;
    padding-left: 5px;
}

QDockWidget::close-button, QDockWidget::float-button {
    border: 1px solid transparent;
    background: darkgray;
    padding: 0px;
}

QDockWidget::close-button:hover, QDockWidget::float-button:hover {
    background: gray;
}

QDockWidget::close-button:pressed, QDockWidget::float-button:pressed {
    padding: 1px -1px -1px 1px;
}
"""


class ObjectsDock(QDockWidget):
    def __init__(self, title=None):
        QDockWidget.__init__(self, title)
        self.setFeatures(QDockWidget.DockWidgetMovable)
        self.setObjectName('consoleDockWidget')
        self.setMinimumWidth(250)
        self.setAcceptDrops(True)
        self.setWindowTitle(title)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.central_widget = QWidget()
        self.setWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(4)
        self.main_layout.setContentsMargins(0, 0, 2, 0)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.setObjectName('configCentralLayout')

        self.central_widget.setLayout(self.main_layout)

    @staticmethod
    def default_dock_area():
        return Qt.RightDockWidgetArea


class ConsoleDock(ObjectsDock):
    def __init__(self, *args):
        super().__init__(*args)
        self.text_edit = Console.LogConsole()
        self.setWidget(self.text_edit)
        self.setObjectName("DockConsoleObjects")

    def set_text_line(self, log_message, error=None, warning=None):
        self.text_edit.write(log_message, error, warning)

    def clear_console(self):
        self.text_edit.clearing()


class ValidatorDock(ObjectsDock):
    def __init__(self, *args):
        super().__init__(*args)
