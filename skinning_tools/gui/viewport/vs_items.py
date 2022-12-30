import math

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from skinning_tools.gui.vs_session import Session


class TextItem(QGraphicsTextItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.setFont(QFont('Ubuntu', 10))
        self.setPlainText('New text')
        self.setDefaultTextColor(Qt.white)

    def set_scene(self, scene):
        scene.addItem(self)

    def set_position(self, position):
        self.setPos(position)

    def set_text(self, text):
        self.setPlainText(text)


# create class for rectangle node
class RectangleNode(QGraphicsRectItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.setRect(0, 0, 100, 100)
        self.setBrush(QBrush(Qt.gray))
        self.setPen(QPen(Qt.white, 1))


class EllipseNode(QGraphicsEllipseItem):
    def __init__(self, rect, parent=None):
        super().__init__(rect, parent)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setBrush(QBrush(Qt.yellow))
        self.setPen(QPen(Qt.black))
        self.handles = []
        self.create_handles()
        self.resizing = Session.active_transform

    def create_handles(self):
        self.handles.append(Handle(QRectF(-5, -5, 10, 10), 0, self))
        self.handles.append(Handle(QRectF(self.rect().width() - 5, -5, 10, 10), 1, self))
        self.handles.append(Handle(QRectF(self.rect().width() - 5, self.rect().height() - 5, 10, 10), 2, self))
        self.handles.append(Handle(QRectF(-5, self.rect().height() - 5, 10, 10), 3, self))

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        for handle in self.handles:
            handle.setBrush(QBrush(Qt.blue))
            handle.setPen(QPen(Qt.black))
            handle.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            nearest = self.find_nearest_item(event.pos(), self.handles)
            index = nearest.index
            print('index', index)
            # index = -1
            # # index = 1
            # for i, handle in enumerate(self.handles):
            #     print('handle', handle.index)
            #     if handle.isUnderMouse():
            #         index = i
            #         break
            if index > -1 and self.resizing == 'scale':
                # self.resizing = True
                # self.resize_handle = handle
                self.resize_handle = self.handles[index]
                self.mouse_press_pos = event.pos()
                self.mouse_press_rect = self.rect()
            else:
                super().mousePressEvent(event)
        elif event.button() == Qt.RightButton:
            self.setSelected(not self.isSelected())
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if self.resizing == 'scale':
            self.prepareGeometryChange()
            index = self.handles.index(self.resize_handle)
            delta = event.pos() - self.mouse_press_pos
            print('delta', delta, index)
            if index == 0:
                self.setRect(QRectF(self.mouse_press_rect.topLeft() + delta,
                                    self.mouse_press_rect.bottomRight()))
            elif index == 1:
                self.setRect(QRectF(self.mouse_press_rect.topRight() + delta,
                                    self.mouse_press_rect.bottomLeft()))
            elif index == 2:
                self.setRect(QRectF(self.mouse_press_rect.bottomRight() + delta,
                                    self.mouse_press_rect.topLeft()))
            elif index == 3:
                self.setRect(QRectF(self.mouse_press_rect.bottomLeft() + delta,
                                    self.mouse_press_rect.topRight()))
            self.update()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.resizing:
            self.resizing = False
            self.resize_handle = None
            self.mouse_press_pos = None
            self.mouse_press_rect = None
            self.update()
        else:
            super().mouseReleaseEvent(event)

    # nearest item
    def find_nearest_item(self, point: QPointF, items: list):
        nearest_item = None
        nearest_distance = 0
        for item in items:
            if item is self:
                continue
            # Calculate the distance between the item and the point
            # print('value', self.mapToParent(item.pos()))
            # print('points', item.pos().x(), item.pos().y(), point.x(), point.y())
            distance = self.distance(item.pos(), point)
            # distance = math.dist(point, item.pos())
            # distance = math.sqrt((point.x() - item.pos().x()) ** 2 + (point.y() - item.pos().y()) ** 2)
            if nearest_item is None or distance < nearest_distance:
                nearest_item = item
                nearest_distance = distance
        print('nearest_item', nearest_item)
        return nearest_item

    # remove to utilities
    @staticmethod
    def distance(p1, p2):
        print('points', p1, p2)
        dx = p1.x() - p2.x()
        dy = p1.y() - p2.y()
        distance = math.sqrt(dx * dx + dy * dy)
        # return math.sqrt((p1.x() - p2.x()) ** 2 + (p1.y() - p2.y()) ** 2)
        return distance


class Handle(QGraphicsRectItem):
    def __init__(self, rect, index, parent=None):
        super().__init__(rect, parent)
        self.setBrush(QBrush(Qt.blue))
        self.setPen(QPen(Qt.black))
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.index = index

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.isUnderMouse():
                pass
                # print('handle is under mouse \n', self.index)
            self.setSelected(not self.isSelected())
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)


class EllipseDrawer(QGraphicsView):
    def __init__(self):
        super().__init__()

        # Set up the scene and view
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Set up the ellipse item
        self.ellipse_item = QGraphicsEllipseItem()
        self.ellipse_item.setPen(QPen(Qt.black, 2))
        self.ellipse_item.setBrush(QBrush(Qt.gray))

        # Set up the start and end points
        self.start_point = None
        self.end_point = None

    def mousePressEvent(self, event):
        # Set the start point when the mouse is pressed
        self.start_point = event.pos()

    def mouseMoveEvent(self, event):
        # Update the end point as the mouse is moved
        self.end_point = event.pos()

        # Calculate the bounding rectangle of the ellipse based on the start and end points
        top_left = QPointF(min(self.start_point.x(), self.end_point.x()), min(self.start_point.y(), self.end_point.y()))
        bottom_right = QPointF(max(self.start_point.x(), self.end_point.x()),
                               max(self.start_point.y(), self.end_point.y()))
        rect = QRectF(top_left, bottom_right)

        # Set the ellipse's bounding rectangle
        self.ellipse_item.setRect(rect)

        # Update the scene
        self.scene.update()

    def mouseReleaseEvent(self, event):
        # Add the ellipse to the scene when the mouse is released
        self.scene.addItem(self.ellipse_item)
        self.ellipse_item = QGraphicsEllipseItem()
        self.ellipse_item.setPen(QPen(Qt.black, 2))
        self.ellipse_item.setBrush(QBrush(Qt.gray))
