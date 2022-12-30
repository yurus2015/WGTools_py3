import math
# from skinning_tools.gui.vs_session import Scene
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from skinning_tools.gui.vs_constants import AXIS_FONT_SIZE


# create scene class
class VSScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(VSScene, self).__init__(parent)
        self.setObjectName('VSScene')
        # self.create_ui()

        # settings
        # todo get from constants?
        self.grid_size = 20
        self.grid_square_size = 5
        self.color_background = QColor('#2f2f2f')
        self.color_light = QColor('#e5e5e5')
        self.color_dark = QColor('#1a1a1a')

        self.setBackgroundBrush(self.color_background)
        self.create_grid()

    def create_grid(self):
        # create grid
        left = -5000
        right = 5000
        top = 5000
        bottom = -5000

        start_left = left - (left % self.grid_size)
        start_top = top - (top % self.grid_size)
        lines_light, lines_dark = [], []
        for x in range(start_left, right, self.grid_size):
            if x % self.grid_square_size == 0:
                lines_dark.append(QLineF(x, top, x, bottom))
            else:
                lines_light.append(QLineF(x, top, x, bottom))

        for y in range(start_top, bottom, self.grid_size):
            if y % self.grid_square_size == 0:
                lines_dark.append(QLineF(left, y, right, y))
            else:
                lines_light.append(QLineF(left, y, right, y))

        # draw lines
        painter = QPainter()
        painter.setPen(QPen(self.color_light, 1))
        painter.drawLines(lines_light)
        painter.setPen(QPen(self.color_dark, 1))
        painter.drawLines(lines_dark)

        # for x in range(0, int(self.width()), self.grid_size):
        #     for y in range(0, int(self.height()), self.grid_size):
        #         # create rect
        #         rect = QRectF(x, y, self.grid_size, self.grid_size)
        #         # create item
        #         item = QGraphicsRectItem(rect)
        #         # set pen
        #         item.setPen(QPen(self.color_dark, 1))
        #         # set brush
        #         if x % (self.grid_size * self.grid_square_size) == 0:
        #             item.setBrush(self.color_light)
        #         elif y % (self.grid_size * self.grid_square_size) == 0:
        #             item.setBrush(self.color_light)
        #         else:
        #             item.setBrush(self.color_dark)
        #         # add item to scene
        #         self.addItem(item)

    # def create_ui(self):
    #     # create background
    #     self.background = QGraphicsRectItem()
    #     self.background.setRect(0, 0, 10000, 10000)
    #     self.background.setBrush(self.color_background)
    #     self.background.setZValue(-1)
    #     self.addItem(self.background)
    #
    #     # create grid
    #     self.grid = QGraphicsRectItem()
    #     self.grid.setRect(-5000, -5000, 10000, 10000)
    #     self.grid.setPen(QPen(QColor(80, 80, 80), 0.5, Qt.SolidLine))
    #     self.grid.setZValue(-1)
    #     self.addItem(self.grid)
    #
    #     # create grid lines
    #     self.grid_lines = []
    #     for i in range(0, 10001, 50):
    #         line = QGraphicsLineItem()
    #         line.setLine(i, -5000, i, 5000)
    #         line.setPen(QPen(QColor(80, 80, 80), 0.5, Qt.SolidLine))
    #         line.setZValue(-1)
    #         self.addItem(line)
    #         self.grid_lines.append(line)
    #
    #     for i in range(-9950, 5001, 50):
    #         line = QGraphicsLineItem()
    #         line.setLine(-5000, i, 5000, i)
    #         line.setPen(QPen(QColor(80, 80, 80), 0.5, Qt.SolidLine))
    #         line.setZValue(-1)
    #         self.addItem(line)
    #         self.grid_lines.append(line)


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)  # for Python2.7 use construction VSEScene.__init__(self, parent)

        # settings
        self.grid_size = 20
        self.grid_squares = 5
        self._color_background = QColor('#2f2f2f')
        self._color_light = QColor('#353535')
        self._color_dark = QColor('#1a1a1a')

        self._color_axis_z = QColor('#7876ff')
        self.color_axis_y = QColor('#00c800')

        self.color_main_line = QColor('#5e5e5e')

        self._pen_light = QPen(self._color_light)
        self._pen_dark = QPen(self._color_dark)
        self._pen_z_axis = QPen(self._color_axis_z)
        self._pen_y_axis = QPen(self.color_axis_y)
        self._pen_main = QPen(self.color_main_line)

        self._pen_light.setWidth(1)
        self._pen_dark.setWidth(2)
        self._pen_main.setWidth(2)

        self.setBackgroundBrush(self._color_background)

        # self.selectionChanged.connect(self.on_selection_changed)

    # def on_selection_changed(self):
    #     view = self.views()[0]

    def set_graphics_scene(self, width, height):
        self.setSceneRect(-width / 2, -height / 2, width, height)

    def grid_lines(self, painter, rect):
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        lines_light, lines_dark = [], []
        for x in range(left, int(rect.right()), self.grid_size):
            if x % (self.grid_size * self.grid_squares) == 0:
                lines_dark.append(QLineF(x, rect.top(), x, rect.bottom()))
            else:
                lines_light.append(QLineF(x, rect.top(), x, rect.bottom()))

        for y in range(top, int(rect.bottom()), self.grid_size):
            if y % (self.grid_size * self.grid_squares) == 0:
                lines_dark.append(QLineF(rect.left(), y, rect.right(), y))
            else:
                lines_light.append(QLineF(rect.left(), y, rect.right(), y))

        painter.setPen(self._pen_light)
        painter.drawLines(lines_light)
        painter.setPen(self._pen_dark)
        painter.drawLines(lines_dark)

        main_lines = [QLine(0, rect.top(), 0, rect.bottom()), QLine(rect.left(), 0, rect.right(), 0)]
        painter.setPen(self._pen_main)
        painter.drawLines(main_lines)

    # def axis_group_transform(self, factor, position):
    #     self.axis_group.setScale(factor)
    #     self.axis_group.setPos(position.x() + 20, position.y() - 20)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        self.grid_lines(painter, rect)
