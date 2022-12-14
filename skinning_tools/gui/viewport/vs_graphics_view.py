from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from skinning_tools.gui.vs_constants import AXIS_FONT_SIZE
# from skinning_tools.gui.viewport.vs_scene import VSScene
from skinning_tools.gui.vs_session import Scene


# from skinning_tools.gui.vs_constants import Session, VSInitialisation


# create graphics view class
class VSGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(VSGraphicsView, self).__init__(parent)
        self.setObjectName('VSGraphicsView')
        # Rectangle selected
        self.setDragMode(QGraphicsView.RubberBandDrag)
        # Drag viewport
        # self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform |
                            QPainter.TextAntialiasing | QPainter.HighQualityAntialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        # Mouse settings
        self.zoom_clamp = Scene().zoom_clamp
        self._min_zoom = Scene().min_zoom
        self._max_zoom = Scene().max_zoom
        self.last_mouse_pos = QPoint()

        # Add scene to view
        # Load scene from Session class store (serialization
        self.scene = Scene().scene
        self.setScene(self.scene)

    def mousePressEvent(self, event):
        self.__last_pos = event.pos()
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.RubberBandDrag)

        if event.button() == Qt.MidButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)

        if event.button() == Qt.RightButton:
            self.setDragMode(QGraphicsView.NoDrag)
            item = self.get_item_at_click(event)
            if item:
                print('Item! {}'.format(item))

            else:
                print(self.scene.items())
                print('No item!')

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setDragMode(QGraphicsView.RubberBandDrag)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MidButton:
            delta = event.pos() - self.__last_pos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self.__last_pos = event.pos()
        super().mouseMoveEvent(event)

    def wheelEvent(self, event):
        # position
        old_cursor_position = self.mapToScene(event.pos())

        # scale
        scale_factor = pow(2.0, event.delta() / 240.0)
        factor = self.transform().scale(scale_factor, scale_factor).mapRect(QRectF(0, 0, 1, 1)).width()

        if self.zoom_clamp:
            if factor < self._min_zoom or factor > self._max_zoom:
                return
        self.scale(scale_factor, scale_factor)

        # position not working
        new_cursor_position = self.mapToScene(event.pos())
        delta = new_cursor_position - old_cursor_position
        self.translate(delta.x(), delta.y())

    '''
    # for example use ctrl + mouse wheel
    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            self.__scale_viewport(event)
        else:
            super().wheelEvent(event)
    '''

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            print('A key pressed')
            # self.fitInView(self.scene.sceneRect(), Qt::KeepAspectRatio)
            self.fitInView(QRectF(-150, -150, 300, 300), Qt.KeepAspectRatio)
            # self.ensureVisible(QRectF(100, 100, 100, 100))
        super().keyPressEvent(event)

    def get_item_at_click(self, event):
        pos = event.pos()
        print('Position: {}'.format(pos))
        obj = self.itemAt(pos)
        return obj
