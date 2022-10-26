from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import weakref
from maya.mel import eval as meval
import maya.cmds as cmds
from .constants import *
from .buttonPresetWidget import PresetButton, MenuBar, CheckButton, ProgressBar
from validator.utils.jsonPreset import PresetsJson
from .checkItemWidget import CheckWidget
from collections import OrderedDict


class ValidatorMainWindow(QDialog):
    instances = list()
    CONTROL_NAME = VERSION
    DOCK_LABEL_NAME = LABEL

    def __init__(self, parent=None):
        super(ValidatorMainWindow, self).__init__(parent)
        # self.__class__.instances.append(weakref.proxy(self))
        self.window_name = self.CONTROL_NAME
        self.setSizeGripEnabled(False)

        self.centralWidget = parent.layout()
        self.centralWidget.setContentsMargins(0, 0, 0, 0)
        self.centralLayout = QVBoxLayout()
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setAlignment(Qt.AlignTop)

        self.menuBar = MenuBar()

        self.check_tab_widget = QWidget()
        self.check_tab_layout = QVBoxLayout()
        self.check_tab_layout.setAlignment(Qt.AlignTop)
        self.check_tab_layout.setContentsMargins(0, 0, 0, 0)
        self.check_tab_layout.setSpacing(0)
        self.check_tab_widget.setLayout(self.check_tab_layout)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("QScrollArea {border: 0px; border-top : 1px solid; border-color: rgb(60,60,60);}")
        self.scrollArea.setAlignment(Qt.AlignTop)

        self.scrollAreaWidget = QWidget()
        # very important value - align to top
        self.scrollAreaWidget.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))

        self.scrollAreaLayout = QVBoxLayout()
        self.scrollAreaLayout.setAlignment(Qt.AlignTop)
        self.scrollAreaLayout.setContentsMargins(1, 1, 0, 0)
        self.scrollAreaLayout.setSpacing(0)
        self.scrollAreaWidget.setLayout(self.scrollAreaLayout)

        # CHECK BUTTON
        self.checkButton = CheckButton()
        self.checkButton.clicked.connect(lambda: self.check_all())

        self.presetButton = PresetButton(parent=self)
        self.action_group = self.presetButton.create_action()
        self.action_group.triggered.connect(self.append_preset_check)

        # PROGRESS BAR (hidden)
        self.progress_bar = ProgressBar()

        self.scrollArea.setWidget(self.scrollAreaWidget)

        self.centralWidget.addLayout(self.centralLayout)
        self.centralLayout.addWidget(self.menuBar)
        self.centralLayout.addWidget(self.presetButton)
        self.centralLayout.addWidget(self.check_tab_widget)

        self.check_tab_layout.addWidget(self.checkButton)
        self.check_tab_layout.addWidget(self.progress_bar)  # progress bar
        self.check_tab_layout.addWidget(self.scrollArea)

        self.append_preset_check()

    # self.checkButton.setText("Check: " + str(self.scrollAreaLayout.count()))

    def load_options(self):

        if not cmds.optionVar(ex=PRESETOPTION):
            cmds.optionVar(sv=(PRESETOPTION, PRESETS[0]))

        if not cmds.optionVar(ex=ISOLATEOPTION):
            cmds.optionVar(iv=(ISOLATEOPTION, 1))

        if not cmds.optionVar(ex=AUTOLOADOPTION):
            cmds.optionVar(iv=(AUTOLOADOPTION, 0))

        preset = cmds.optionVar(q=PRESETOPTION)
        self.presetButton.set_preset(preset)
        self.menuBar.set_isolate(cmds.optionVar(q=ISOLATEOPTION))
        self.menuBar.set_autoload(cmds.optionVar(q=AUTOLOADOPTION))

        return preset

    def append_preset_check(self):
        self.current_preset = self.load_options()
        if self.scrollAreaLayout.count() != 0:
            for x in range(self.scrollAreaLayout.count()):
                item = self.scrollAreaLayout.itemAt(x)
                item.widget().deleteLater()
        # add
        data = PresetsJson.read_json()

        for x in data:
            if x == self.current_preset:
                sorted_data = OrderedDict(sorted(data[x].items()))
                for y in sorted_data:
                    type_error = sorted_data[y][0]
                    label = sorted_data[y][1]
                    action = sorted_data[y][2]
                    fixed = sorted_data[y][3]

                    checkWidget = CheckWidget(type_error, label, action,
                                              fixed)  # create checkWidget instance from checkWidget.py
                    self.scrollAreaLayout.addWidget(checkWidget)  # scrollArea add 1 check

                break
        # print "sorted_data ", len(sorted_data)
        self.checkButton.setText("Checks: " + str(len(sorted_data)))
        self.checkButton.clicked.disconnect()
        self.checkButton.clicked.connect(lambda: self.check_all())

    def check_all(self):
        if self.scrollAreaLayout.count() != 0:
            isolate = cmds.optionVar(q=ISOLATEOPTION)
            check_for_run = self.visible_check()
            if check_for_run:

                self.progress_bar.setVisible(True)
                QApplication.processEvents()
                self.progress_bar.setMaximum(len(check_for_run))
                for item in range(len(check_for_run)):
                    try:
                        if check_for_run[item].runCheck():
                            pass
                        elif isolate:
                            check_for_run[item].setVisible(False)
                    except:
                        pass
                    self.progress_bar.update_bar()
                    QApplication.processEvents()
                self.progress_bar.setVisible(False)
                self.progress_bar.reset()
            # chahge check button
            check_for_run = self.visible_check()
            if not check_for_run:
                self.checkButton.setText("Reload Checks")
                self.checkButton.clicked.disconnect()
                self.checkButton.clicked.connect(lambda: self.append_preset_check())

    def visible_check(self):
        visibleItems = []
        for x in range(self.scrollAreaLayout.count()):
            item = self.scrollAreaLayout.itemAt(x)
            if item.widget().isVisible():
                visibleItems.append(item.widget())
        return visibleItems

    def closeEvent(self, event):
        # restore position window
        self.settings.setValue("geometry", self.saveGeometry())

    @staticmethod
    def delete_instances():
        for ins in ValidatorMainWindow.instances:
            print('Delete {}'.format(ins))
            try:
                ins.setParent(None)
                ins.deleteLater()
            except:
                pass

            ValidatorMainWindow.instances.remove(ins)
            del ins

    def run(self):
        cmd = 'global proc layerEditorLayerButtonVisibilityChange(string $layer)'
        cmd += '{'
        cmd += 'int $layerVisibility = getDisplayLayerVisibility($layer);'
        cmd += 'setDisplayLayerVisibility($layer, !$layerVisibility);'
        cmd += ' string $currLayer = `editDisplayLayerGlobals -q -currentDisplayLayer`;'
        cmd += ' layerEditorLayerButtonSelect 0 $currLayer;'
        cmd += '}'
        meval(cmd)

        return self
