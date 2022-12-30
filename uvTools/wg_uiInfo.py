import numpy as np
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

from shiboken2 import wrapInstance
import maya.OpenMayaUI as omu

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import os

dir = str(os.path.dirname(__file__))


def main_window_pointer():
    # Get a pointer to the main window
    ptr = omu.MQtUtil.mainWindow()

    # Return a QWidget instance wrapping the pointer
    return wrapInstance(int(ptr), QWidget)


class UIInfo(QDialog):
    def __init__(self, size, parent=main_window_pointer()):
        super().__init__(parent)
        self.setWindowTitle("UI Info")

        # Set the dimensions of the UI based on the size parameter
        width_ui = 300
        height_ui = 170
        if size > 100:
            width_ui = 200 + size
            height_ui = 70 + size

        self.setFixedSize(width_ui, height_ui)
        self.setObjectName("id_UI_Info")

        # Initialize variables for drawing
        self.pixmap = QPixmap(QSize(size, size))
        self.painter = QPainter()
        self.colorWhite = QColor()
        self.colorBlack = QColor()
        self.colorRed = QColor()

        # Set the layout of the UI
        self.setLayout(self.create_layout(size))

        # Connect the UI elements to their respective functions
        self.connections(size)

        # Update the information displayed in the UI
        self.update_info(size)

    def create_layout(self, size):
        self.label1_0 = QLabel("Region:")
        self.label1_0.setFixedWidth(100)
        self.label1_1 = QLabel("[0:1]")
        self.label2_0 = QLabel("Current UV Set:")
        self.label2_0.setFixedWidth(100)
        self.label2_1 = QLabel("map1")
        self.label3_0 = QLabel("UV Area:")
        self.label3_0.setFixedWidth(100)
        self.label3_1 = QLabel("0%")
        self.label4_0 = QLabel("Number of UV Shells:")
        self.label4_1 = QLabel("0")
        self.label5_0 = QLabel("Out of region shells:")
        self.label5_1 = QLabel("0")

        self.btn_ok = QPushButton("Close")
        self.btn_update = QPushButton("Update")

        self.layoutMain = QVBoxLayout()
        self.layoutBtn = QHBoxLayout()
        self.layoutContent = QHBoxLayout()
        self.layoutText = QVBoxLayout()
        self.layoutText.setContentsMargins(0, 10, 0, 0)

        self.layoutInfo_01 = QHBoxLayout()
        self.layoutInfo_02 = QHBoxLayout()
        self.layoutInfo_03 = QHBoxLayout()
        self.layoutInfo_04 = QHBoxLayout()
        self.layoutInfo_05 = QHBoxLayout()

        self.imgLabel = QLabel()
        self.imgLabel.setFixedSize(size + 20, size + 10)

        # Set the colors for drawing
        self.colorWhite.setRgb(255, 255, 255, 255)
        self.colorBlack.setRgb(0, 0, 0, 255)
        self.colorRed.setRgb(255, 0, 0, 255)
        self.pixmap.fill(self.colorBlack)

        self.imgLabel.setPixmap(self.pixmap)

        # Set the alignment of the layout containers
        self.layoutContent.setAlignment(Qt.AlignTop)

        # Add the labels and their corresponding values to the layout
        self.layoutInfo_01.addWidget(self.label1_0)
        self.layoutInfo_01.addWidget(self.label1_1)

        self.layoutInfo_02.addWidget(self.label2_0)
        self.layoutInfo_02.addWidget(self.label2_1)

        self.layoutInfo_03.addWidget(self.label3_0)
        self.layoutInfo_03.addWidget(self.label3_1)

        self.layoutInfo_04.addWidget(self.label4_0)
        self.layoutInfo_04.addWidget(self.label4_1)

        self.layoutInfo_05.addWidget(self.label5_0)
        self.layoutInfo_05.addWidget(self.label5_1)

        # Add the layout containers to the main layout
        self.layoutText.addLayout(self.layoutInfo_01)
        self.layoutText.addLayout(self.layoutInfo_02)
        self.layoutText.addLayout(self.layoutInfo_03)
        self.layoutText.addLayout(self.layoutInfo_04)
        self.layoutText.addLayout(self.layoutInfo_05)

        self.layoutContent.addWidget(self.imgLabel)
        self.layoutContent.addLayout(self.layoutText)

        self.layoutBtn.addWidget(self.btn_ok)
        self.layoutBtn.addWidget(self.btn_update)

        self.layoutMain.addLayout(self.layoutContent)
        self.layoutMain.addLayout(self.layoutBtn)

        # self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.layoutText.addItem(self.verticalSpacer)

        return self.layoutMain

    def connections(self, size):
        # Connect the buttons to their respective functions
        self.btn_ok.clicked.connect(self.close_window)
        self.btn_update.clicked.connect(lambda: self.update_info(size))

    def close_window(self):
        self.close()

    def check_selected(self, size):
        selected = cmds.ls(sl=1, l=1)
        object_to_process = None
        if selected:
            for i in selected:
                if cmds.ls(cmds.listRelatives(i, c=1, type="mesh", f=1)):
                    object_to_process = i
                    break
            if object_to_process:
                self.update_info(size)

    def update_info(self, size):
        self.pixmap.fill(self.colorBlack)
        obj = cmds.filterExpand(sm=12)
        if obj:
            for o in obj:
                # start processing object
                # 1 - get current uv set
                current_uv_set = cmds.polyUVSet(o, q=1, cuv=1)
                if current_uv_set:
                    self.label2_1.setText(current_uv_set[0])

                # check if the object has some uvs
                num_uvs = cmds.polyEvaluate(o, uv=1)

                if num_uvs > 0:
                    # 2 - drawing uv shells
                    selection_list = OpenMaya.MSelectionList()
                    selection_list.add(o)
                    dag_path = OpenMaya.MDagPath()
                    m_object = OpenMaya.MObject()

                    selection_list.getDagPath(0, dag_path, m_object)

                    iter = OpenMaya.MItMeshPolygon(dag_path)
                    while not iter.isDone():
                        u_coord = OpenMaya.MFloatArray()
                        v_coord = OpenMaya.MFloatArray()
                        iter.getUVs(u_coord, v_coord, current_uv_set[0])
                        uv_count = u_coord.length()

                        q_array = QPolygonF()
                        for i in range(len(u_coord)):
                            cur_u = int(u_coord[i] * size)
                            cur_v = size - int(v_coord[i] * size)
                            point = QPointF(cur_u, cur_v)
                            q_array.append(point)

                        self.painter.begin(self.pixmap)
                        self.painter.setBrush(QBrush(self.colorWhite))
                        self.painter.setPen(self.colorWhite)
                        self.painter.drawConvexPolygon(q_array)
                        self.painter.end()
                        self.imgLabel.setPixmap(self.pixmap)
                        iter.next()

            # 3 - get black pixels and get area = 10000 - len(blackPixels)
            black_pixel_count = 0
            # Convert the pixmap to an image for easier pixel access
            self.result_image = self.pixmap.toImage()

            # Iterate over the pixels and count the number of black ones
            black_pixel_count = self.black_pixel_count(size)
            # black_pixel_numpy = self.black_pixel_numpy()
            # black_pixel_gpt = self.black_pixel_gpt()

            # Calculate and set the percentage of white pixels
            percentage = 100 - float(black_pixel_count) / (size * size) * 100
            self.label3_1.setText(str(percentage) + "%")

    def black_pixel_count(self, size):
        black_pixel_count = 0

        # Iterate over the pixels and count the number of black ones
        for i in range(0, size):
            for j in range(0, size):
                color = QColor.fromRgb(self.result_image.pixel(i, j))
                if color == Qt.black:
                    black_pixel_count += 1

        return black_pixel_count

    def black_pixel_numpy(self):
        # # Convert the pixmap to an image for easier pixel access
        # self.result_image = self.pixmap.toImage()

        # Convert the image to a numpy array
        self.result_array = np.array(self.result_image)
        # print(self.result_array)

        # Create a mask for the black pixels
        black_mask = np.all(self.result_array == [255, 255, 255], axis=-1)
        print(black_mask)
        # Count the number of black pixels
        black_pixel_count = np.count_nonzero(black_mask)

        return black_pixel_count

    def black_pixel_gpt(self):
        # Convert the image to a numpy array
        self.result_array = np.array(self.result_image)

        # Set the color you want to count
        target_color = (0, 0, 0)  # Black

        # # Count the number of black pixels
        # black_pixel_count = np.count_nonzero(black_mask)

        # Find the indices of the pixels that match the target color
        indices = np.where((self.result_array[:, :, 0] == target_color[0]) &
                           (self.result_array[:, :, 1] == target_color[1]) &
                           (self.result_array[:, :, 2] == target_color[2]))

        # Get the number of pixels of the target color
        pixel_count = len(indices[0])
        return pixel_count


def main(size):
    if cmds.window("id_UI_Info", q=True, exists=True):
        cmds.deleteUI("id_UI_Info")

    try:
        ui.close()
        ui.deleteLater()
    except:
        pass

    ui = UIInfo(size)
    ui.show()
