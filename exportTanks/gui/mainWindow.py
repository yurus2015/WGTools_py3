# create class qdialog for create window
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from maya.mel import eval as meval


class TankExportMainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        print('Parent: ', parent)
        self.setObjectName('TankExporterDockWindow')
        self.scroll_layout = QVBoxLayout()  # 3 create layout for this widget
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.scroll_layout)

        self.button = QPushButton('Test')
        self.scroll_layout.addWidget(self.button)

    def add_external_widget(self, widget):
        self.scroll_layout.addWidget(widget)
