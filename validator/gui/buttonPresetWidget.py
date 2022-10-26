from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from functools import partial
import maya.cmds as cmds
from .constants import *



# PRESETS, MIN, MAX, MENU, SUBMENU, ISOLATEOPTION, PRESETOPTION


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super(MenuBar, self).__init__()
        self.setObjectName('menu_bar')

        self.options_menu = QMenu(MENU[0], self)
        self.about_menu = QAction(MENU[1], self)

        self.isolate_mistakes = QAction('Isolate mistakes', self.options_menu, triggered=self._save_options)
        self.isolate_mistakes.setCheckable(True)
        self.autoload = QAction('Autoload', self.options_menu, triggered=self._save_options)
        self.autoload.setCheckable(True)
        self.options_menu.addAction(self.isolate_mistakes)
        self.options_menu.addAction(self.autoload)

        # self.about_menu.triggered.connect(lambda: self.showAbout())

        self.addMenu(self.options_menu)
        self.addAction(self.about_menu)

        self.aboutWindow = False

    # def showAbout(self):
    #     if not self.aboutWindow:
    #         self.aboutWindow = aboutWindow()
    #         self.aboutWindow.show()
    #     else:
    #         self.aboutWindow.show()

    def set_isolate(self, value):
        self.isolate_mistakes.setChecked(value)

    def set_autoload(self, value):
        self.autoload.setChecked(value)

    def _save_options(self):
        cmds.optionVar(iv=(ISOLATEOPTION, self.isolate_mistakes.isChecked()))
        cmds.optionVar(iv=(AUTOLOADOPTION, self.autoload.isChecked()))


class PresetButton(QPushButton):
    def __init__(self, parent=None):
        super(PresetButton, self).__init__()
        # self.scrollAreaLayout = scrollArrea
        # self.parnt = parent
        self.setObjectName('project_preset_progress')
        self.setStyleSheet("QPushButton {border:0px; \
							background: rgb(20, 20, 20, 60);\
							height: 30px;\
							}")

        self.setText('Preset: ' + PRESETS[0])
        self.menu = QMenu(self)
        self.setMenu(self.menu)

    def create_action(self):
        self.group = QActionGroup(self)

        self.menu.aboutToShow.connect(self.set_width_menu)
        for preset in PRESETS:
            preset_menu = QAction(preset, self.menu, checkable=True)
            preset_menu.triggered.connect(partial(self.set_preset, preset_menu))
            self.menu.addAction(preset_menu)
            self.group.addAction(preset_menu)

        return self.group

    def set_preset(self, preset):
        name = preset
        try:
            name = preset.text()
        except:
            pass
        self.setText('Preset: ' + name)
        print('test commit')
        cmds.optionVar(sv=(PRESETOPTION, name))

    def set_width_menu(self):
        self.menu.setMinimumWidth(self.width())
        self.menu.setMaximumWidth(self.width())


class CheckButton(QPushButton):
    def __init__(self, parent=None):
        super(CheckButton, self).__init__(parent)
        self.__isolateAction = None
        self.setFixedHeight(30)
        self.setText("Check")


class ProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super(ProgressBar, self).__init__()
        self.setRange(MIN, MAX)
        self.setValue(MIN)
        self.setTextVisible(True)

        self.setObjectName('progressBarObj')
        self.setVisible(False)

    def update_bar(self):
        maxim = self.maximum()
        value = self.value() + 1

        self.setValue(value)
        if value == maxim:
            self.reset()
            self.setValue(0)
            self.setVisible(False)
