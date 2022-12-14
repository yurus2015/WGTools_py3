from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from skinning_tools.gui.viewport.vs_graphics_view import VSGraphicsView


# create class widget
class VSEditorWidget(QWidget):
    def __init__(self, parent=None):
        super(VSEditorWidget, self).__init__(parent)
        self.setObjectName('VSEditorWidget')
        self.create_ui()

    def create_ui(self):
        # create main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # create splitter
        splitter = QSplitter()
        splitter.setOrientation(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)
        splitter.handleWidth()

        # create left panel
        # todo separate class
        viewport = VSGraphicsView()
        # viewport.setMinimumWidth(200)
        # viewport.setStyleSheet('background-color: #2d2d2d;')
        # left_panel_layout = QVBoxLayout()
        # left_panel_layout.setContentsMargins(0, 0, 0, 0)
        # viewport.setLayout(left_panel_layout)

        # create right panel widgets
        # todo separate class
        attribute_editor = QWidget()
        attribute_editor.setMinimumWidth(200)
        attribute_editor.setMaximumWidth(200)
        attribute_editor.setStyleSheet('background-color: #2d2d2d;')
        left_panel_layout = QVBoxLayout()
        left_panel_layout.setContentsMargins(0, 0, 0, 0)
        attribute_editor.setLayout(left_panel_layout)

        self.setLayout(main_layout)
        main_layout.addWidget(splitter)
        splitter.addWidget(viewport)
        splitter.addWidget(attribute_editor)
