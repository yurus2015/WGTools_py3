from PySide2.QtGui import *
from PySide2.QtWidgets import *


class LogConsole(QTextEdit):
    """docstring for ClassName"""

    def __init__(self, parent=None):

        QTextEdit.__init__(self)
        self.setReadOnly(True)
        self.setMinimumHeight(400)

    def write(self, msg, err=None, wrg=None):
        """Add msg to the console's output, on a new line."""
        type_message = ''
        color = QColor(255, 255, 255)
        if err:
            color = QColor(255, 0, 0)
            type_message = 'Error: '
        if wrg:
            color = QColor(255, 255, 0)
            type_message = 'Warning: '
        self.setTextColor(color)
        type_message = type_message + msg
        if self.toPlainText():  # editor no empty - need new stroke
            type_message = '\n' + type_message
        self.insertPlainText(type_message)
        QApplication.processEvents()

    def clearing(self):
        self.clear()
