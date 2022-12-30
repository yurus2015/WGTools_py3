from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


# from skinning_tools.gui.vs_session import Scene


class ContextMenuMain(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.setAcceptHoverEvents(True)

        self.setZValue(100)

        self.context_menu = QMenu()
        self.context_menu.addAction('Action 1')
        self.context_menu.addAction('Action 2')
        self.context_menu.addAction('Action 3')

    def boundingRect(self):
        return QRectF(0, 0, 100, 10)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.white, 1))
        painter.setBrush(QBrush(Qt.gray))
        painter.drawRect(self.boundingRect())

    def hoverEnterEvent(self, event):
        self.context_menu.exec_(event.screenPos())

    def hoverLeaveEvent(self, event):
        self.context_menu.close()

    def set_scene(self, scene):
        scene.addItem(self)
