from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from skinning_tools.gui.vs_constants import AXIS_FONT_SIZE
# from skinning_tools.gui.viewport.vs_scene import VSScene
from skinning_tools.gui.vs_session import Scene, Session
from skinning_tools.gui.viewport.vs_items import TextItem, EllipseNode


# from skinning_tools.gui.viewport.vs_context_menu import ContextMenuMain


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
        self.zoom_clamp = Session().zoom_clamp
        self._min_zoom = Session().min_zoom
        self._max_zoom = Session().max_zoom
        self.last_mouse_pos = QPoint()

        # Viewport settings

        # Add scene to view
        # Load scene from Session class store (serialization)
        # self.scene = Session().scene
        # self.setScene(self.scene)

        # Load context menu from Session class store (serialization)
        # self.context_menu = Scene().context_menu

    def set_scene(self, scene):
        self.scene = scene
        self.setScene(self.scene)

    def paintEvent(self, event):
        super().paintEvent(event)
        rect = self.viewport().rect()

        # Create a QPainter object
        painter = QPainter(self.viewport())
        painter.begin(self.viewport())

        # Set the pen style, width, and color
        painter.setPen(QPen(Qt.blue, 1, Qt.SolidLine))

        # Draw the first line and text
        painter.drawLine(20, rect.bottom() - 20, 50, rect.bottom() - 20)
        painter.drawText(QPointF(55, rect.bottom() - 20), 'z')

        # Set the pen style, width, and color
        painter.setPen(QPen(Qt.green, 1, Qt.SolidLine))

        # Draw the second line and text
        painter.drawLine(20, rect.bottom() - 20, 20, rect.bottom() - 50)
        painter.drawText(QPointF(18, rect.bottom() - 55), 'y')

        # Set the pen style, width, and color
        painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
        # Draw text
        painter.drawText(QPointF(10, 30), 'Information HUD: ')

        painter.end()

    # TODO: for all events check what under mouse - empty, node, edge, etc.
    def mousePressEvent(self, event):
        self.__last_pos = event.pos()

        # Point position in scene coordinates
        self.start_scene_point = self.mapToScene(event.pos())

        # Point position in viewport coordinates
        self.start_view_point = event.pos()

        if event.button() == Qt.LeftButton:
            # Check under mouse
            item = self.get_item_at_click(event)
            if not item:
                print('Viewport: Empty space')
                # Check active tool - create node, create edge, etc.
                if Session().active_tool == 'create_node':
                    # Create node
                    self.ellipse_item = EllipseNode(QRectF(self.start_scene_point, self.start_scene_point))
                    self.scene.addItem(self.ellipse_item)
                    self.ellipse_item.update()
                    self.scene.update()
                    self.setDragMode(QGraphicsView.NoDrag)

            self.setDragMode(QGraphicsView.RubberBandDrag)

        if event.button() == Qt.MidButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.vertex_del_me()

        if event.button() == Qt.RightButton:
            self.setDragMode(QGraphicsView.NoDrag)
            item = self.get_item_at_click(event)
            if item:
                print('Item! {}'.format(item))

            else:
                print(self.scene.items())
                print('No item!')
                self.scene_context_menu(event)
                # Scene().context_menu
                # create item under right click
                item = TextItem('Test')
                item.set_scene(self.scene)
                item.setPos(self.mapToScene(event.pos()))
                # pos = self.mapToScene(event.pos())
                # print('Position: {}'.format(pos))
                # self.add_item_to_scene(pos)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setDragMode(QGraphicsView.RubberBandDrag)
        if event.button() == Qt.RightButton:
            self.scene.removeItem(self.context)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.end_position = self.mapToScene(event.pos())
            # Calculate the bounding rectangle of the ellipse based on the start and end points
            top_left = QPointF(min(self.start_scene_point.x(), self.end_position.x()),
                               min(self.start_scene_point.y(), self.end_position.y()))
            bottom_right = QPointF(max(self.start_scene_point.x(), self.end_position.x()),
                                   max(self.start_scene_point.y(), self.end_position.y()))
            rect = QRectF(top_left, bottom_right)

            # Set the ellipse's bounding rectangle
            if self.ellipse_item:
                self.ellipse_item.setRect(rect)
                self.ellipse_item.update()
                self.scene.update()
            # self.ellipse_item.setRect(rect)
            # self.ellipse_item.update()

            # Update the scene
            self.scene.update()

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
        self.safe_scale(scale_factor)

        # position
        new_cursor_position = self.mapToScene(event.pos())
        delta = new_cursor_position - old_cursor_position
        self.translate(delta.x(), delta.y())

    def safe_scale(self, scale_factor):
        factor = self.transform().scale(scale_factor, scale_factor).mapRect(QRectF(0, 0, 1, 1)).width()
        if self.zoom_clamp:
            if factor < self._min_zoom or factor > self._max_zoom:
                return
        self.scale(scale_factor, scale_factor)

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
            self.fit_in_view()
        if event.key() == Qt.Key_F:
            print('F key pressed')
            self.fit_in_view(True)
        super().keyPressEvent(event)

    # TODO make common method for return item under mouse - type, class, etc.
    def get_item_at_click(self, event):
        pos = event.pos()
        # print('Position: {}'.format(pos))
        obj = self.itemAt(pos)
        return obj

    # very-very-temporary solution - for testing
    # def set_item_position(self, item, pos):
    #     item = TextItem()
    #     self.scene.addItem(item)
    #     item.setPos(pos)

    def fit_in_view(self, selection=None):
        rect = QRect()
        if selection:  # press F key
            items = self.scene.selectedItems()
            if not items:
                return
            for item in items:
                rect = rect.united(item.sceneBoundingRect())
        else:  # press A key
            items = self.scene.items()
            if items:
                rect = self.scene.itemsBoundingRect()
                # rect = QRectF(rect.left(), rect.top(), rect.width() * 1.5, rect.height() * 1.5)
            else:
                self.resetTransform()
                # rect = self.viewport().rect()
                # rect = QRectF(-(rect.width() / 4), -rect.height() / 4, rect.width() / 2, rect.height() / 2)
        self.fitInView(rect, Qt.KeepAspectRatio)
        self.centerOn(rect.center())
        scale_factor = self.transform().m11()
        if scale_factor > self._max_zoom:
            self.safe_scale(self._max_zoom / scale_factor)

    '''
    Scene context menu
    '''

    def scene_context_menu(self, event):
        self.context = Session().context_menu
        self.context.set_scene(self.scene)
        self.context.setPos(self.mapToScene(event.pos()))

    def vertex_del_me(self):
        print('Vertex delete me')
        '''
        vertices = [QPointF(10, 10), QPointF(20, 30), QPointF(40, 30), QPointF(30, 10)]

        # Create a QPolygonF object from the list of vertices
        polygon = QPolygonF(vertices)

        # Add the polygon to the scene
        self.scene.addPolygon(polygon, brush=Qt.blue)

        # Add a circle at each vertex of the polygon
        for vertex in vertices:
            self.scene.addEllipse(vertex.x() - 2, vertex.y() - 2, 4, 4, brush=Qt.red)
        '''
        rect = QRectF(20, 20, 100, 100)
        ellipse = EllipseNode(rect)
        self.scene.addItem(ellipse)
