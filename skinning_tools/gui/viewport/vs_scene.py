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

        self.z_axis = QColor('#7876ff')
        self.y_axis = QColor('#00c800')

        self.main_line = QColor('#5e5e5e')

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)
        self.setBackgroundBrush(self._color_background)

        self._pen_z_axis = QPen(self.z_axis)
        self._pen_y_axis = QPen(self.y_axis)

        self._pen_main = QPen(self.main_line)
        self._pen_main.setWidth(2)

        z_axis = AxisLine(50, 0, self._pen_z_axis)
        self.addItem(z_axis)
        z_axis.setZValue(-1000)
        y_axis = AxisLine(0, -50, self._pen_y_axis)
        self.addItem(y_axis)

        self.z_letter = AxisLetter('Z', self.z_axis)
        self.addItem(self.z_letter)
        self.z_letter.setPos(50, -15)

        self.y_letter = AxisLetter('Y', self.y_axis)
        self.addItem(self.y_letter)
        self.y_letter.setPos(-15, -65)

        # self.selectionChanged.connect(self.on_selection_changed)

    # def on_selection_changed(self):
    #     view = self.views()[0]

    def set_graphics_scene(self, width, height):
        self.setSceneRect(-width / 2, -height / 2, width, height)

    # todo grid to class
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # here we create our grid
        left = int(math.floor(rect.left()))
        right = int(math.floor(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.floor(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))
        # draw lines
        painter.setPen(self._pen_light)
        painter.drawLines(lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(lines_dark)

        main_lines = [QLine(0, top, 0, bottom), QLine(left, 0, right, 0)]

        painter.setPen(self._pen_main)
        painter.drawLines(main_lines)


class AxisLine(QGraphicsLineItem):
    def __init__(self, start, end, pen, parent=None):
        super().__init__()
        self.setPen(pen)
        self.setLine(0, 0, start, end)


class AxisLetter(QGraphicsTextItem):
    def __init__(self, text, color, parent=None):
        super().__init__(parent)
        self.setPlainText(text)
        self.setDefaultTextColor(color)
        self.setFont(QFont('Arial', AXIS_FONT_SIZE))

    def set_size(self, size):
        self.setFont(QFont('Arial', size))
