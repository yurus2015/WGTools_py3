from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from skinning_tools.gui.viewport.vs_graphics_view import VSGraphicsView
from skinning_tools.gui.vs_session import Session


# create class widget
class VSEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('VSEditorWidget')
        self.create_ui()

    def create_ui(self):
        # create main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # create splitter
        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.handleWidth()

        # create left panel
        # create tab widget
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.setMovable(False)
        # add tabwidget switch command
        self.tab_widget.currentChanged.connect(self.tab_widget_switch)

        # create left panel
        self.viewport = VSGraphicsView()
        self.viewport.set_scene(Session().scene_left)
        self.viewport_right_side = VSGraphicsView()
        self.viewport_right_side.set_scene(Session().scene_right)

        # create right panel widgets
        self.attribute_editor = QWidget()
        self.attribute_editor.setMinimumWidth(200)
        # self.attribute_editor.setMaximumWidth(200)
        self.attribute_editor.setStyleSheet('background-color: #2d2d2d;')
        self.left_panel_layout = QVBoxLayout(self.attribute_editor)
        self.left_panel_layout.setContentsMargins(0, 0, 0, 0)

        # add widgets to main layout
        self.main_layout.addWidget(self.splitter)
        # self.splitter.addWidget(self.viewport)
        self.splitter.addWidget(self.tab_widget)
        self.splitter.addWidget(self.attribute_editor)

        # add tab
        self.tab_widget.addTab(self.viewport, 'Left Side')
        self.tab_widget.addTab(self.viewport_right_side, 'Right Side')

    def tab_widget_switch(self):
        # get index of tab
        index = self.tab_widget.currentIndex()
        if index == 0:
            print('left side')
            # self.viewport.set_scene(Session().scene_left)
        elif index == 1:
            print('right side')
            # self.viewport.set_scene(Session().scene_right)
        else:
            print('error')
