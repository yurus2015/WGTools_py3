from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import shiboken2
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omu
import maya.cmds as cmds
import os

ATTRIBUTES = ['Animated (Skined)', 'Static', 'Static with hierarchy']


def main_window_pointer():
    ptr = omu.MQtUtil.mainWindow()  # pointer for the main window
    return wrapInstance(long(ptr), QWidget)


class BW_Export_Wnd(QDialog):
    def __init__(self, parent=main_window_pointer()):
        QDialog.__init__(self, parent)

        self.setWindowTitle("Export Visual")
        self.setModal(False)
        self.setMinimumWidth(300)
        self.setMinimumHeight(250)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setObjectName("ExportVisual")

        self.option_vars_init('bw_export')
        self.option_vars_init('bw_attr')

        self.layouts()

    def layouts(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 5, 20, 5)
        self.main_layout.setSpacing(20)  # layout
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)

        self.main_layout.addWidget(self.type_layout_ui())
        self.main_layout.addWidget(self.attributes_layout_ui())
        self.main_layout.addWidget(self.button_layout_ui())

    def type_layout_ui(self):
        self.type_frame = self.frame_box(height=50)
        self.type_layout = QHBoxLayout(self.type_frame)
        self.type_layout.setContentsMargins(20, 5, 5, 5)
        self.type_layout.setSpacing(50)
        self.type_label = QLabel('Export')
        self.visual_radio = QRadioButton("Visual")
        self.visual_radio.setChecked(True)
        self.visual_radio.clicked.connect(lambda: self.option_vars_type(active=True))
        self.animation_radio = QRadioButton("Animation")
        self.animation_radio.clicked.connect(lambda: self.option_vars_type(active=False))
        self.type_layout.addWidget(self.type_label)
        self.type_layout.addWidget(self.visual_radio)
        self.type_layout.addWidget(self.animation_radio)

        cmds.optionVar(iv=('bw_export', 1))
        return self.type_frame

    def attributes_layout_ui(self):
        self.attributes_frame = self.frame_box(height=100)
        self.attributes_layout = QVBoxLayout(self.attributes_frame)
        self.attributes_layout.setContentsMargins(20, 5, 5, 5)
        self.attributes_layout.setSpacing(5)
        self.animated_ck = QRadioButton("Animated")
        self.animated_ck.clicked.connect(lambda: self.option_vars_set('bw_attr', 0))
        self.static_ck = QRadioButton("Static")
        self.static_ck.setChecked(True)
        self.static_ck.clicked.connect(lambda: self.option_vars_set('bw_attr', 1))
        self.hierarchy_ck = QRadioButton("Static with hierarchy")
        self.hierarchy_ck.clicked.connect(lambda: self.option_vars_set('bw_attr', 2))

        self.attributes_layout.addWidget(self.animated_ck)
        self.attributes_layout.addWidget(self.static_ck)
        self.attributes_layout.addWidget(self.hierarchy_ck)

        cmds.optionVar(iv=('bw_attr', 1))

        return self.attributes_frame

    def button_layout_ui(self):
        self.buttonbox = QDialogButtonBox(self)
        self.buttonbox.setOrientation(Qt.Horizontal)
        self.export_btn = QPushButton("&Export")
        self.export_btn.clicked.connect(self.export_command)
        self.buttonbox.addButton(self.export_btn, QDialogButtonBox.ActionRole)
        self.cancel_btn = QPushButton("&Cancel")
        self.cancel_btn.clicked.connect(self.close_window)
        self.buttonbox.addButton(self.cancel_btn, QDialogButtonBox.ActionRole)

        return self.buttonbox

    def trank_layout_ui(self):
        self.trank_layout = QHBoxLayout(self)
        self.trank_combo = QComboBox()
        self.trank_combo.setFixedHeight(22)
        self.trank_combo.setObjectName('customTrankCombo')
        self.button_dir = self.initButton(title='Add Branch', command=lambda: self.dir_browser())
        self.button_dir.setFixedWidth(65)
        self.button_dir.setFixedHeight(20)

        self.trank_layout.addWidget(self.trank_combo)
        self.trank_layout.addWidget(self.button_dir)

        return self.trank_layout

    def initButton(self, parent=None, title="", command=None):
        self._button = QPushButton(title)
        if command:
            self._button.clicked.connect(command)

        return self._button

    def frame_box(self, parent=None, title="", width=None, height=None):
        self.sg_frame = QFrame()
        self.sg_frame.setStyleSheet("#addElementFrame{background-white;}")
        self.sg_frame.setFrameShape(QFrame.Box)
        self.sg_frame.setFrameShadow(QFrame.Sunken)
        self.sg_frame.setMinimumHeight(height)
        self.sg_frame.setMaximumHeight(height)

        return self.sg_frame

    def dir_browser(self):  # open browser to set export path
        bpath = None
        try:
            bpath = cmds.fileDialog2(fm=3, dialogStyle=1)[0]
        except:
            pass

        if bpath and 'vehicles' in bpath.split('/', -1):
            if bpath not in self.pathes:
                self.trank_combo.addItem(bpath)
                self.trank_combo.setCurrentIndex(self.trank_combo.count() - 1)
                self.pathes.append(bpath)

                utils.editXML(bpath)
        else:
            cmds.confirmDialog(title='Warning', message='Select "vehicles" dir in your trank', button=['   OK   '],
                               defaultButton='   OK   ')

    def option_vars_type(self, active=True):
        # if active:
        self.animated_ck.setEnabled(active)
        self.static_ck.setEnabled(active)
        self.hierarchy_ck.setEnabled(active)

        if active:
            self.option_vars_set('bw_export', 1)
        else:
            self.option_vars_set('bw_export', 2)

    def option_vars_init(self, bw_type):
        if cmds.optionVar(exists=bw_type):
            self.bw_type = cmds.optionVar(q=bw_type)
        else:
            cmds.optionVar(iv=(bw_type, 1))
            self.bw_type = 1

        return self.bw_type

    def option_vars_set(self, bw_type, value):
        cmds.optionVar(iv=(bw_type, value))

    def export_selection(self, selection=None):
        self.selection = selection

    def close_window(self):
        if cmds.window("ExportVisual", q=True, exists=True):
            cmds.deleteUI("ExportVisual")
        try:
            cmds.deleteUI('MayaWindow|ExportVisual')
        except:
            pass

    def export_command(self):
        self.export_path = Utils.file_dialog()
        print
        'EXPORT', self.export_path, self.selection

        sceneTextures = Utils.clearTextures()
        if cmds.optionVar(q='bw_export') == 1:
            arguments = 'noPrompt=1;exportMode=' + str(
                cmds.optionVar(q='bw_attr')) + ';bumpMapped=1;keep_material=1;copyExternalTextures=1;copyTexturesTo'
            print
            'ARG', arguments
            try:
                if self.selection:
                    cmds.file(self.export_path, force=False, type="BigWorldAsset", pr=True, es=True, options=arguments)
                else:
                    cmds.file(self.export_path, force=False, type="BigWorldAsset", pr=True, ea=True, options=arguments)
            except:
                pass
        else:
            pass
        Utils.reAssignTextures(sceneTextures)

        self.close_window()


class Utils():
    def __init__(self):
        print
        'utils'

    @classmethod
    def clearTextures(cls):
        materialNode = cmds.ls(mat=1)
        nodeMaterialStruct = {}
        for node in materialNode:
            connectedAttrs = cmds.listConnections(node, d=0, s=1, c=1)
            if connectedAttrs:
                connectedAttrs = connectedAttrs[::2]
                for attr in connectedAttrs:
                    plugAttr = cmds.connectionInfo(attr, sfd=True)
                    nodeMaterialStruct[attr] = plugAttr
        if nodeMaterialStruct:
            for i in nodeMaterialStruct:
                cmds.disconnectAttr(nodeMaterialStruct[i], i)
        return nodeMaterialStruct

    @classmethod
    def reAssignTextures(cls, nodeMaterialStruct=None):
        if not nodeMaterialStruct: return
        for i in nodeMaterialStruct:
            cmds.connectAttr(nodeMaterialStruct[i], i)

    @classmethod
    def loadVisualPlugin(cls):
        if not cmds.pluginInfo('visual', query=True, l=True):
            try:
                cmds.loadPlugin('visual')
            except:
                raise MissingPluginError('Unable to load visual.mll!')

    @classmethod
    def file_dialog(cls, mode=0):
        path = None
        path = cmds.fileDialog2(dialogStyle=1,
                                fileMode=mode,
                                # startingDirectory = dir,
                                fileFilter='BigWorld (*.model)')

        return path


def main(export=None):
    if cmds.window("ExportVisual", q=True, exists=True):
        cmds.deleteUI("ExportVisual")
    try:
        cmds.deleteUI('MayaWindow|ExportVisual')
    except:
        pass

    # try:
    # 	dialog = BW_Export_Wnd()
    # 	dialog.close()
    # except:
    # 	pass
    Utils.loadVisualPlugin()
    dialog = BW_Export_Wnd()
    dialog.export_selection(export)
    dialog.show()
