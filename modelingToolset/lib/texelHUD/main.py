# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaRender as OpenMayaRender
import weakref
import numpy as np
import json
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import os, re, posixpath

current_dir = os.path.dirname(os.path.abspath(__file__))
description = "Texel Computing. Please use options to compute texel"
buttonType = "opt"
beautyName = "Texel Computing"
iconName = "Calculate Texel"

DIMENSION = [256, 512, 1024, 2048, 4096]
OPTIONS = [2048, 0, 12, 40, 0, 0,
           2048]  # 2048 - defout size, 0 - offset type, 12 percent offset, 40 polycount offset, 0 - color
TIPS_WIDTH_DIMENSION = 'Set width dimension'
TIPS_HEIGHT_DIMENSION = 'Set height dimension'
TIPS_COLORIZE_BUTTON = 'Set vertex color'
TIPS_TEXEL = 'Set texel for calculation'
TIPS_RANGE = 'Plus and minus range from color texel'
TIPS_RED_ISOLATE = 'Isolate red color'
TIPS_BLUE_ISOLATE = 'Isolate blue color'
TIPS_STILESHEET = """QToolTip {background-color: gray;color: yellow;border: black solid 1px}"""
CALLBACKS = []


class Utils(object):

    @classmethod
    def getWidgetPointer(cls, widget):

        ptr = OpenMayaUI.MQtUtil.findControl(widget)

        # ptr = OpenMayaUI.MQtUtil.mainWindow()
        return wrapInstance(long(ptr), QWidget)

    @classmethod
    def readJSON(cls):
        # read JSON data and return it
        # currentFolder = cls.getCurrentDir().replace("\\", "\\\\")
        rgb = []
        value = []
        tip = []
        name = []
        jason_read = open(current_dir + '\\detail_data.json', 'r')
        data = json.load(jason_read)
        for i in data:
            rgb.append(i.get('rgb'))
            tip.append(i.get('tip'))
            value.append(int(i.get('value')))
            name.append(i.get('name'))

        return rgb, tip, value, name

    @classmethod
    def load_option_var(cls):
        # resolutions
        # offset type
        # offset value

        options = OPTIONS

        if cmds.optionVar(exists='texel_resolution'):
            options[0] = cmds.optionVar(q='texel_resolution')
        else:
            cmds.optionVar(iv=('texel_resolution', options[0]))

        if cmds.optionVar(exists='texel_offset_type'):
            options[1] = cmds.optionVar(q='texel_offset_type')
        else:
            cmds.optionVar(iv=('texel_offset_type', options[1]))

        if cmds.optionVar(exists='texel_offset_percent'):
            options[2] = cmds.optionVar(q='texel_offset_percent')
        else:
            cmds.optionVar(iv=('texel_offset_percent', options[2]))

        if cmds.optionVar(exists='texel_offset_polygons'):
            options[3] = cmds.optionVar(q='texel_offset_polygons')
        else:
            cmds.optionVar(iv=('texel_offset_polygons', options[3]))

        if cmds.optionVar(exists='texel_neitral_color'):
            options[4] = cmds.optionVar(q='texel_neitral_color')
        else:
            cmds.optionVar(iv=('texel_neitral_color', options[4]))

        if cmds.optionVar(exists='texel_rectangle'):
            options[5] = cmds.optionVar(q='texel_rectangle')
        else:
            cmds.optionVar(iv=('texel_rectangle', options[5]))

        if cmds.optionVar(exists='texel_resolution_vertical'):
            options[6] = cmds.optionVar(q='texel_resolution_vertical')
        else:
            cmds.optionVar(iv=('texel_resolution_vertical', options[6]))

        return options

    @classmethod
    def save_option_var(cls, option, value):
        cmds.optionVar(iv=(option, int(value)))

    @classmethod
    def add_texel_attribute(cls, size, objectName):
        if not cmds.attributeQuery('texeldim', node=objectName, exists=True):
            cmds.addAttr(objectName, longName='texeldim', at='long')
        cmds.setAttr(objectName + '.texeldim', size, e=1, k=False)

    @classmethod
    def loadPlugin(cls):
        if not cmds.pluginInfo('techartAPI2018', query=True, loaded=True):
            try:
                cmds.loadPlugin('techartAPI2018')
            except:
                print('Don`t load plugin')


class ToolOptions(QWidget):
    instances = list()

    def __init__(self, parent=None):

        super(ToolOptions, self).__init__(parent)
        # ToolOptions.delete_instances()
        # self.__class__.instances.append(weakref.proxy(self))

        '''DATA'''
        self.resolutions = DIMENSION
        self.options = Utils.load_option_var()
        cmds.optionVar(iv=('texel_rectangle', 0))
        cmds.optionVar(iv=('texel_resolution_vertical', self.options[0]))
        # self.callback_remove()
        Utils.loadPlugin()
        self.setLayout(self.createUI())
        # self.callback_selection()
        self.setMouseTracking(True)

    # self.main()
    # self.script_jobs()

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainLayout.setSpacing(5)
        self.mainLayout.setContentsMargins(0, 0, 0, 5)

        self.buttonsLayout = QHBoxLayout()

        '''combo button'''
        self.combobox = QComboBox()
        self.combobox.setMaximumWidth(60)
        self.combobox.addItems([str(p) + '' for p in self.resolutions])
        index = self.combobox.findText(str(self.options[0]), Qt.MatchCaseSensitive)
        self.combobox.setCurrentIndex(index)
        self.combobox.currentIndexChanged.connect(self.sender_value)
        self.combobox.setToolTip(TIPS_WIDTH_DIMENSION)
        self.combobox.setStyleSheet(TIPS_STILESHEET)

        self.combobox_2 = QComboBox()
        self.combobox_2.setMaximumWidth(60)
        self.combobox_2.addItems([str(p) + '' for p in self.resolutions])
        index_2 = self.combobox_2.findText(str(self.options[0]), Qt.MatchCaseSensitive)
        self.combobox_2.setCurrentIndex(index_2)
        self.combobox_2.currentIndexChanged.connect(self.reselect)
        self.combobox_2.setEnabled(False)
        self.combobox_2.setToolTip(TIPS_HEIGHT_DIMENSION)
        self.combobox_2.setStyleSheet(TIPS_STILESHEET)

        self.connect_dimensions = QPushButton()
        self.connect_dimensions.setCheckable(True)
        self.connect_dimensions.setChecked(False)
        self.connect_dimensions.setObjectName('texel_dimention_link')
        self.connect_dimensions.setAttribute(Qt.WA_DeleteOnClose)
        self.connect_dimensions.clicked.connect(self.icon_changed)
        self.connect_dimensions.setMaximumWidth(20)
        self.connect_dimensions.setToolTip(TIPS_BLUE_ISOLATE)
        self.connect_dimensions.setStyleSheet(TIPS_STILESHEET)

        self.icon_on = QIcon(current_dir + '/on_button.png')
        self.icon_off = QIcon(current_dir + '/off_button.png')
        self.connect_dimensions.setIcon(self.icon_off)
        self.connect_dimensions.setIconSize(QSize(12, 12))

        self.color_button = QPushButton("Colorize Texel")
        self.color_button.setToolTip(TIPS_COLORIZE_BUTTON)
        self.color_button.setStyleSheet(TIPS_STILESHEET)
        self.color_button.clicked.connect(self.paint_texel)

        self.buttonsLayout.addWidget(self.combobox)
        self.buttonsLayout.addWidget(self.connect_dimensions)
        self.buttonsLayout.addWidget(self.combobox_2)
        self.buttonsLayout.addWidget(self.color_button)

        self.help_text = QLabel('')
        self.help_text.setStyleSheet("""color: yellow;""")

        '''vertex color'''
        self.vertex_color_layout = QVBoxLayout()
        self.dimensions_layout = QHBoxLayout()
        self.offset_layout = QHBoxLayout()

        label_txl = QLabel("Color texel")
        label_txl.setFixedWidth(80)
        label_txl.setToolTip(TIPS_TEXEL)
        label_txl.setStyleSheet(TIPS_STILESHEET)
        self.spinBox_txl = QDoubleSpinBox()
        self.spinBox_txl.setRange(1.0, 1000.0)
        self.spinBox_txl.setSingleStep(10.0)
        self.spinBox_txl.setValue(400.0)
        self.spinBox_txl.setFixedWidth(60)
        self.spinBox_txl.setToolTip(TIPS_TEXEL)
        self.spinBox_txl.setStyleSheet(TIPS_STILESHEET)
        self.slider_txl = QSlider()
        self.slider_txl.setRange(1, 1000)
        self.slider_txl.setValue(400.0)
        self.slider_txl.setSingleStep(1)
        self.slider_txl.setOrientation(Qt.Horizontal)
        self.slider_txl.setToolTip(TIPS_TEXEL)
        self.slider_txl.setStyleSheet(TIPS_STILESHEET)

        self.slider_txl.valueChanged.connect(lambda: self.connections(self.spinBox_txl, self.slider_txl))
        self.spinBox_txl.valueChanged.connect(lambda: self.connections(self.slider_txl, self.spinBox_txl))

        self.dimensions_layout.addWidget(label_txl)
        self.dimensions_layout.addWidget(self.slider_txl)
        self.dimensions_layout.addWidget(self.spinBox_txl)

        self.label_offset = QComboBox()
        self.label_offset.setMaximumWidth(80)
        self.label_offset.addItem("Offset %")
        self.label_offset.addItem("Offset texels")
        self.label_offset.setToolTip(TIPS_RANGE)
        self.label_offset.setStyleSheet(TIPS_STILESHEET)
        self.label_offset.setCurrentIndex(self.options[1])
        self.label_offset.currentIndexChanged.connect(self.offset_change)
        self.spinBox_offset = QDoubleSpinBox()
        self.spinBox_offset.setObjectName('txlOffset')
        self.spinBox_offset.setRange(0.0, 100.0)
        self.spinBox_offset.setSingleStep(1.0)
        self.spinBox_offset.setToolTip(TIPS_RANGE)
        self.spinBox_offset.setStyleSheet(TIPS_STILESHEET)

        if self.options[1] == 0:
            self.spinBox_offset.setValue(self.options[2])
        else:
            self.spinBox_offset.setValue(self.options[3])
        self.spinBox_offset.setFixedWidth(60)
        self.slider_offset = QSlider()
        self.slider_offset.setRange(0, 100)
        self.slider_offset.setSingleStep(1)
        self.slider_offset.setOrientation(Qt.Horizontal)
        self.slider_offset.setToolTip(TIPS_RANGE)
        self.slider_offset.setStyleSheet(TIPS_STILESHEET)

        if self.options[1] == 0:
            self.slider_offset.setValue(self.options[2])
        else:
            self.slider_offset.setValue(self.options[3])

        self.slider_offset.valueChanged.connect(lambda: self.connections(self.spinBox_offset, self.slider_offset))
        self.spinBox_offset.valueChanged.connect(lambda: self.connections(self.slider_offset, self.spinBox_offset))

        self.offset_layout.addWidget(self.label_offset)
        self.offset_layout.addWidget(self.slider_offset)
        self.offset_layout.addWidget(self.spinBox_offset)

        self.image_label = QLabel()
        self.image_label.setScaledContents(True)
        self.pixmap = QtGui.QPixmap(current_dir + '/color_line.png')
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(self.pixmap)

        self.feedback_layout = QHBoxLayout()
        self.feedback_min_layout = QHBoxLayout()
        self.feedback_min_layout.setAlignment(Qt.AlignLeft)
        self.feedback_max_layout = QHBoxLayout()
        self.feedback_max_layout.setAlignment(Qt.AlignRight)

        self.min_label = QLabel('<360')
        self.min_isolate_btn = QPushButton('Isolate')
        self.min_isolate_btn.setCheckable(True)
        self.min_isolate_btn.setChecked(False)
        self.min_isolate_btn.setToolTip(TIPS_RED_ISOLATE)
        self.min_isolate_btn.setStyleSheet(TIPS_STILESHEET)
        self.min_isolate_btn.clicked.connect(self.paint_texel)

        self.current_texel = QLabel('400')
        self.current_texel.setAlignment(Qt.AlignCenter)
        self.current_texel.setFixedWidth(60)
        self.max_label = QLabel('>440')

        self.max_isolate_btn = QPushButton('Isolate')
        self.max_isolate_btn.setCheckable(True)
        self.max_isolate_btn.setChecked(False)
        self.max_isolate_btn.setToolTip(TIPS_BLUE_ISOLATE)
        self.max_isolate_btn.setStyleSheet(TIPS_STILESHEET)
        self.max_isolate_btn.clicked.connect(self.paint_texel)

        self.feedback_min_layout.addWidget(self.min_label)
        self.feedback_min_layout.addWidget(self.min_isolate_btn)
        self.feedback_max_layout.addWidget(self.max_isolate_btn)
        self.feedback_max_layout.addWidget(self.max_label)
        self.feedback_layout.addLayout(self.feedback_min_layout)
        self.feedback_layout.addWidget(self.current_texel)
        self.feedback_layout.addLayout(self.feedback_max_layout)

        self.details_layout = self.detail_layer()

        self.reset_button = QPushButton('Reset colorize')
        self.reset_button.setFixedHeight(16)
        self.reset_button.setMouseTracking(True)
        self.reset_button.clicked.connect(self.reset_color)

        self.vertex_color_layout.addLayout(self.dimensions_layout)
        self.vertex_color_layout.addLayout(self.offset_layout)
        self.vertex_color_layout.addWidget(self.image_label)
        self.vertex_color_layout.addLayout(self.feedback_layout)
        self.vertex_color_layout.addWidget(self.details_layout)
        self.vertex_color_layout.addWidget(self.reset_button)

        '''main layout'''
        self.mainLayout.addLayout(self.buttonsLayout)
        self.mainLayout.addWidget(self.help_text)
        self.mainLayout.addLayout(self.vertex_color_layout)

        self.offset_levels()

        return self.mainLayout

    def detail_layer(self):
        self.labels_array = []
        self.detail_widget = QWidget()

        self.detail_widget.setStyleSheet(TIPS_STILESHEET)
        self.detail_layer = QHBoxLayout()
        self.detail_layer.setContentsMargins(0, 0, 0, 5)
        self.detail_button = QPushButton('Tank detail')
        # self.detail_button.setCheckable(True)
        # self.detail_button.setChecked(False)
        self.detail_button.setMaximumWidth(80)
        self.detail_button.clicked.connect(self.detail_texel)

        self.labels_layer = QVBoxLayout()
        self.color_labels_layer = QHBoxLayout()
        self.text_laybels_layer = QHBoxLayout()
        self.text_laybels_layer.setContentsMargins(5, 0, 0, 0)

        self.RGB, self.TIP, self.VALUE, self.NAME = Utils.readJSON()

        # for color in COLOR_LABELS:
        # 	image_label = QLabel()
        # 	image_label.setEnabled(False)
        # 	image_label.setScaledContents(True)
        # 	#self.pixmap = QtGui.QPixmap(current_dir + '/color_line.png')
        # 	pixmap = QtGui.QPixmap(current_dir + '/' + color + '.png')

        # 	#image_label.setAlignment(Qt.AlignCenter)
        # 	image_label.setPixmap(pixmap)
        # 	self.color_labels_layer.addWidget(image_label)
        # 	self.labels_array.append(image_label)

        for color in self.RGB:
            widget = QPushButton()
            widget.setEnabled(False)
            widget.setStyleSheet("background-color: rgb(" + color + ")");
            widget.setMaximumHeight(5);
            widget.setMinimumHeight(5);
            widget.setMinimumWidth(20)
            self.labels_array.append(widget)
            self.color_labels_layer.addWidget(widget)

        TIPS_DETAILS = ''
        for i in range(len(self.NAME)):
            print(self.NAME[i])
            widget = QLabel(str(self.NAME[i]))
            widget.setEnabled(False)
            TIPS_DETAILS += str(self.NAME[i]) + " " + self.TIP[i] + '\n'
            self.labels_array.append(widget)
            self.text_laybels_layer.addWidget(widget)

        self.detail_widget.setToolTip(TIPS_DETAILS)
        self.labels_layer.addLayout(self.color_labels_layer)
        self.labels_layer.addLayout(self.text_laybels_layer)
        self.detail_layer.addWidget(self.detail_button)
        self.detail_layer.addLayout(self.labels_layer)
        self.detail_widget.setLayout(self.detail_layer)

        return self.detail_widget

    @staticmethod
    def delete_instances():
        print('Lenght: ', len(ToolOptions.instances))
        for ins in ToolOptions.instances:
            print('Delete {}'.format(ins))
            try:
                ins.setParent(None)
                ins.deleteLater()
            except:
                pass

            ToolOptions.instances.remove(ins)
            del ins

    def detail_texel(self):
        # status = self.detail_button.isChecked()
        # for label in self.labels_array:
        # 	label.setEnabled(status)
        # self.reset_color()
        colors = []
        for color in self.RGB:
            color = color.split(',')
            color = [float(i) for i in color]
            colors.append(color)

        # if status:
        resolution = cmds.optionVar(q='texel_resolution')
        best_texel = self.spinBox_txl.value()
        cmds.texelFaces(dtx=self.VALUE, clr=colors, dim=resolution, o=6, txl=best_texel)

        selected = cmds.filterExpand(sm=(12, 34))
        selected = cmds.ls(selected, o=1)
        if selected:
            for sel in selected:
                cmds.setAttr(sel + '.displayColors', 1)
                cmds.setAttr(sel + '.displayColorChannel', "Emission", type="string")

    def script_jobs(self):
        global CALLBACKS
        script_job = cmds.scriptJob(e=["SelectionChanged", self.recomend_dimensions], p="texel_dimention_link")
        CALLBACKS.append(script_job)
        print('script_jobs', script_job)

    def switch_color(self):
        button = self.sender()
        if button.objectName() == 'btn_color_green':
            self.white_button.setChecked(False)
            Utils.save_option_var('texel_neitral_color', 1)

        else:
            self.green_button.setChecked(False)
            Utils.save_option_var('texel_neitral_color', 2)
        if not button.isChecked():
            Utils.save_option_var('texel_neitral_color', 0)
        self.paint_texel()

    def sender_value(self):
        button = self.sender()
        Utils.save_option_var('texel_resolution', button.currentText())
        self.paint_texel()
        self.setValue()

    def reselect(self):
        value = int(self.combobox_2.currentText())
        cmds.optionVar(iv=('texel_resolution_vertical', value))
        selected = cmds.filterExpand(sm=(12, 34))
        if selected:
            cmds.select(selected)

    def icon_changed(self):
        if self.connect_dimensions.isChecked():
            self.connect_dimensions.setIcon(self.icon_on)
            self.combobox_2.setEnabled(True)
            Utils.save_option_var('texel_rectangle', 1)
        else:
            self.connect_dimensions.setIcon(self.icon_off)
            self.combobox_2.setEnabled(False)
            index = self.combobox.currentIndex()
            self.combobox_2.setCurrentIndex(index)
            Utils.save_option_var('texel_rectangle', 0)
        selected = cmds.filterExpand(sm=(12, 34))
        if selected:
            cmds.select(selected)

    def offset_change(self):
        Utils.save_option_var('texel_offset_type', self.label_offset.currentIndex())
        options = Utils.load_option_var()
        if self.label_offset.currentIndex() == 0:
            self.spinBox_offset.setValue(options[2])
            Utils.save_option_var('texel_offset_percent', (options[2]))
        else:
            self.spinBox_offset.setValue(options[3])
            Utils.save_option_var('texel_offset_polygons', (options[3]))

    def connections(self, parent, child):
        parent.setValue(child.value())
        if parent.objectName() == 'txlOffset' or child.objectName() == 'txlOffset':
            if self.label_offset.currentIndex() == 0:
                Utils.save_option_var('texel_offset_percent', (self.spinBox_offset.value()))
            else:
                Utils.save_option_var('texel_offset_polygons', (self.spinBox_offset.value()))
        self.paint_texel()

    def reset_color(self):
        for i in cmds.ls(type='mesh'):
            try:
                cmds.polyColorSet(i, delete=True)
            except:
                pass
            try:
                cmds.deleteAttr(i, at='texeldim')
            except:
                pass

        self.callback_remove()

    def callback_selection(self):
        global CALLBACKS
        self.callback_remove()
        CALLBACKS = []
        selection_changed_callback = OpenMaya.MEventMessage.addEventCallback("SelectionChanged",
                                                                             self.recomend_dimensions)
        print('CALLBACKS ', selection_changed_callback)
        CALLBACKS.append(selection_changed_callback)

    def callback_remove(self):
        global CALLBACKS
        for call in CALLBACKS:
            try:
                OpenMaya.MMessage.removeCallback(call)
            except:
                pass
        try:
            cmds.scriptJob(ka=True, force=True)
            'I Kill All!'
        except:
            pass

    def recomend_dimensions(self, *args):
        print('Interactive color')
        value = DIMENSION
        try:
            objectName = cmds.filterExpand(sm=12)
        except:
            pass

        texel = cmds.texelFaces(avr=1)
        if objectName:

            if cmds.attributeQuery('texeldim', node=objectName[-1], exists=True):
                size = cmds.getAttr(objectName[-1] + '.texeldim')
                index = self.combobox.findText(str(size), Qt.MatchCaseSensitive)
                if self.combobox.currentText() != str(size):
                    self.combobox.setCurrentIndex(index)
                    Utils.save_option_var('texel_resolution', size)
            # else:
            #	self.paint_texel()
            else:
                for x in range(len(DIMENSION)):
                    if value[x] / 128 * texel > 349:
                        self.help_text.setText('Recomend: ' + str(value[x]))
            # return
            try:
                self.distortion_checked()
            # self.texel_to_ui(texel)
            except:
                pass

        else:
            self.help_text.setText('')

    def setValueHUD(self, visible=True):
        Utils.loadPlugin()
        comp = self.get_button_connect()
        if comp > 0.0:

            value = Utils.load_option_var()[0]
            result = value / 128.0 * comp
            return str(int(result))
        else:
            return ''

    def getWidgetByClassName(self, name):
        widgets = QApplication.instance().allWidgets()
        for x in widgets:
            if name in str(x.__class__).replace("<class '", "").replace("'>", ""):
                try:
                    value = x.get_button_connect()
                    if value:
                        return value

                except:
                    pass

    def get_button_connect(self):

        h_dim = cmds.optionVar(q='texel_resolution')
        v_dim = cmds.optionVar(q='texel_resolution_vertical')
        su = sv = 1.0
        count = None
        value = Utils.load_option_var()[5]
        if value and h_dim != v_dim:
            selected = cmds.filterExpand(sm=(12, 34))
            uv = cmds.polyListComponentConversion(selected, tuv=True)
            scale = float(h_dim) / float(v_dim)
            if scale > 0.0:
                sv = scale
            else:
                su = scale
            cmds.polyEditUV(uv, pu=0, pv=0, su=1.0 / su, sv=1.0 / sv)
            count = cmds.texelFaces(avr=1)
            cmds.polyEditUV(uv, pu=0, pv=0, su=su, sv=sv)
        else:
            count = cmds.texelFaces(avr=1)

        return count

    def setValue(self):
        Utils.loadPlugin()
        comp = cmds.texelFaces(avr=1)

        try:
            self.help_text.setText('')
        except:
            pass

        if comp > 0.0:
            value = Utils.load_option_var()[0]
            result = value / 128.0 * comp

            try:
                current = int(self.spinBox_txl.value())
                self.current_texel.setText(str(current) + ' / ' + str(int(result)))
            except:
                pass

            if cmds.headsUpDisplay('HUDtexelMessure', q=1, ex=1):
                cmds.headsUpDisplay('HUDtexelMessure', e=1, label=str(value) + ' ')
            return int(result)

        else:
            self.help_text.setText('')

            return ''

    def texel_to_ui(self, texel):
        if texel:
            value = Utils.load_option_var()[0]
            result = value / 128.0 * texel
            current = int(self.spinBox_txl.value())
            self.current_texel.setText(str(current) + ' / ' + str(int(result)))
            if cmds.headsUpDisplay('HUDtexelMessure', q=1, ex=1):
                cmds.headsUpDisplay('HUDtexelMessure', e=1, label=str(value) + ' ')

    def offset_levels(self):
        best_texel = self.spinBox_txl.value()

        if self.label_offset.currentIndex() == 0:
            min_level = int(best_texel) - int(best_texel) * self.spinBox_offset.value() / 100
            self.min_label.setText('<' + str(int(min_level)))

            max_level = int(best_texel) + int(best_texel) * self.spinBox_offset.value() / 100
            self.max_label.setText('>' + str(int(max_level)))

            offset = self.spinBox_offset.value()

        else:
            min_level = int(best_texel) - self.spinBox_offset.value()
            self.min_label.setText('<' + str(int(min_level)))

            max_level = int(best_texel) + self.spinBox_offset.value()
            self.max_label.setText('>' + str(int(max_level)))

            offset = self.spinBox_offset.value() / int(best_texel) * 100

        return offset

    def distortion_checked(self):

        h_dim = self.combobox.currentText()
        v_dim = self.combobox_2.currentText()
        su = sv = 1.0
        count = None
        # get value from ui
        vertex_color_combobox = cmds.optionVar(q='texel_resolution')
        best_texel = self.spinBox_txl.value()

        min_alpha = self.min_isolate_btn.isChecked()
        max_alpha = self.max_isolate_btn.isChecked()

        # if self.label_offset.currentIndex() == 0:
        # 	min_level = int(best_texel) - int(best_texel)*self.spinBox_offset.value()/100
        # 	self.min_label.setText('<'+str(int(min_level)))

        # 	max_level = int(best_texel) + int(best_texel)*self.spinBox_offset.value()/100
        # 	self.max_label.setText('>'+str(int(max_level)))

        # 	offset = self.spinBox_offset.value()

        # else:
        # 	min_level = int(best_texel) - self.spinBox_offset.value()
        # 	self.min_label.setText('<'+str(int(min_level)))

        # 	max_level = int(best_texel) + self.spinBox_offset.value()
        # 	self.max_label.setText('>'+str(int(max_level)))

        # 	offset = self.spinBox_offset.value()/int(best_texel)*100

        offset = self.offset_levels()

        # checked = self.findChild(QPushButton, "texel_dimention_link")
        # print 'Check', checked

        if self.connect_dimensions.isChecked():
            selected = cmds.filterExpand(sm=(12, 34))
            uv = cmds.polyListComponentConversion(selected, tuv=True)

            scale = float(h_dim) / float(v_dim)
            if scale > 0.0:
                sv = scale
            else:
                su = scale
            cmds.polyEditUV(uv, pu=0, pv=0, su=1.0 / su, sv=1.0 / sv)
            count = cmds.texelFaces(txl=best_texel, dim=vertex_color_combobox, o=offset, rd=min_alpha, bl=max_alpha)
            cmds.polyEditUV(uv, pu=0, pv=0, su=su, sv=sv)
        else:
            count = cmds.texelFaces(txl=best_texel, dim=vertex_color_combobox, o=offset, rd=min_alpha, bl=max_alpha)

        self.texel_to_ui(count)

    def paint_texel(self):
        # self.loadPlugin()

        # get value from ui
        vertex_color_combobox = cmds.optionVar(q='texel_resolution')
        # best_texel = self.spinBox_txl.value()

        # min_alpha = self.min_isolate_btn.isChecked()
        # max_alpha = self.max_isolate_btn.isChecked()

        # if self.label_offset.currentIndex() == 0:
        # 	min_level = int(best_texel) - int(best_texel)*self.spinBox_offset.value()/100
        # 	self.min_label.setText('<'+str(int(min_level)))

        # 	max_level = int(best_texel) + int(best_texel)*self.spinBox_offset.value()/100
        # 	self.max_label.setText('>'+str(int(max_level)))

        # 	offset = self.spinBox_offset.value()

        # else:
        # 	min_level = int(best_texel) - self.spinBox_offset.value()
        # 	self.min_label.setText('<'+str(int(min_level)))

        # 	max_level = int(best_texel) + self.spinBox_offset.value()
        # 	self.max_label.setText('>'+str(int(max_level)))

        # 	offset = self.spinBox_offset.value()/int(best_texel)*100

        # cmds.texelFaces(txl = best_texel, dim = vertex_color_combobox, o = offset, rd = min_alpha, bl = max_alpha)
        self.distortion_checked()

        selected = cmds.filterExpand(sm=(12, 34))
        selected = cmds.ls(selected, o=1)
        if selected:
            for sel in selected:
                cmds.setAttr(sel + '.displayColors', 1)
                if self.min_isolate_btn.isChecked() or self.max_isolate_btn.isChecked():
                    cmds.setAttr(sel + '.displayColorChannel', "Ambient+Diffuse", type="string")
                else:
                    cmds.setAttr(sel + '.displayColorChannel', "Emission", type="string")
                Utils.add_texel_attribute(vertex_color_combobox, sel)

        self.help_text.setText('')

    # self.setValue()

    def main(self, off=None):
        print('HUD')
        Utils.loadPlugin()
        value = DIMENSION
        hud = Utils.load_option_var()

        # remove all huds - fix old version
        for index in range(len(value)):
            if hud[0] == value[index]:
                pass
            elif cmds.headsUpDisplay('HUD' + str(value[index]), q=1, ex=1):
                cmds.headsUpDisplay('HUD' + str(value[index]), rem=True)
        # end remove old huds

        if cmds.headsUpDisplay('HUDtexelMessure', q=1, ex=1):
            if not off:
                cmds.headsUpDisplay('HUDtexelMessure', rem=True)
        # self.hud_button.setChecked(False)
        else:
            nfb = cmds.headsUpDisplay(nfb=0);
            cmds.headsUpDisplay('HUDtexelMessure', section=0,
                                block=nfb,
                                blockSize='small',
                                label=str(hud[0]) + ' ',
                                labelFontSize='large',
                                dfs='large',
                                command=self.setValueHUD,
                                event='SelectionChanged')
