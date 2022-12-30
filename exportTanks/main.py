# create dock window using workspace control
import inspect

from maya import OpenMayaUI as omu
import traceback
import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
from maya import cmds
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui
from exportTanks.gui.mainWindow import TankExportMainWindow
from exportTanks.gui.session import Session
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# Compatibility with Maya 2018
try:
    long
except NameError:
    long = int


# maya pointer function
def get_maya_window():
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QMainWindow)


def delete_workspace_control(control_name: str):
    if cmds.workspaceControl(control_name, q=True, exists=True):
        cmds.workspaceControl(control_name, e=True, close=True)
        cmds.deleteUI(control_name, control=True)


class TankExporterDockableWindow(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=None):
        delete_workspace_control(Session.control_name)
        super(TankExporterDockableWindow, self).__init__(parent=parent)
        self.setWindowFlags(Qt.Window)
        self.setObjectName(Session.name_window)
        self.setWindowTitle(Session.name_window)
        self.resize(300, 300)

        # Set central layout
        self.central_layout = QVBoxLayout()
        self.setLayout(self.central_layout)

    def closeEvent(self, event):
        pass

    def add_external_widget(self, widget):
        self.central_layout.addWidget(widget)


def restore():
    '''Called when Maya opens to restore the Shadeset UI.'''
    workspace_control = omui.MQtUtil.getCurrentParent()
    Session.mixin_window = TankExporterDockableWindow()
    pointer = omui.MQtUtil.findControl(Session.mixin_window.objectName())
    omui.MQtUtil.addWidgetToMayaLayout(long(pointer), long(workspace_control))


def show():
    if Session.mixin_window is None:
        Session.mixin_window = TankExporterDockableWindow()

    ### Get class name of widget
    # class_name = instance.__class__.__name__
    ### Get module name of widget
    # module_name = inspect.getmodule(instance).__name__

    # Session.mixin_window.show(dockable=True, area='right',
    #                           uiScript='import {0}\n{0}.{1}.restore_from_close()'.format(module_name, class_name))

    # Add widget to dockable window
    Session.main_window = TankExportMainWindow()
    Session.mixin_window.add_external_widget(Session.main_window)

    # Show dockable window
    Session.mixin_window.show(dockable=True,
                              uiScript='import exportTanks.main\nexportTanks.main.restore()')


# class MyDockableWidget(MayaQWidgetDockableMixin, QDialog):
#     def __init__(self, parent=get_maya_window()):
#         super(MyDockableWidget, self).__init__(parent=parent)
#         self.vertical_layout = QVBoxLayout(self)
#         self.vertical_layout.setContentsMargins(0, 0, 0, 0)
#         self.button = QPushButton("Click me")
#         self.button_ = QPushButton("Click me")
#         self.button__ = QPushButton("Click me")
#         self.vertical_layout.addWidget(self.button)
#         self.vertical_layout.addWidget(self.button_)
#         self.vertical_layout.addWidget(self.button__)
#         self.setWindowTitle("WTF")
#         self.setObjectName('TankExporterDockWindow')
#         self.resize(300, 300)
#         # self.show()
#
#     def closeEvent(self, event):
#         cmds.workspaceControl('TankExporterDockWindow', e=True, close=True)
#         delete_window('TankExporterDockWindow')


# class TestDockableWindow(QDialog):
#     def __init__(self, parent=None):
#         super(TestDockableWindow, self).__init__(parent=parent)
#         self.vertical_layout = QVBoxLayout(self)
#         self.vertical_layout.setContentsMargins(0, 0, 0, 0)
#         self.button = QPushButton("Click me")
#         self.button_ = QPushButton("Click me")
#         self.button__ = QPushButton("Click me")
#         self.vertical_layout.addWidget(self.button)
#         self.vertical_layout.addWidget(self.button_)
#         self.vertical_layout.addWidget(self.button__)
#         self.setWindowTitle("WTF")
#         self.setObjectName('TankExporterDockWindow')
#         self.resize(300, 300)
#         # self.show()
#
#     def closeEvent(self, event):
#         cmds.workspaceControl('TankExporterDockWindow', e=True, close=True)
#         delete_window('TankExporterDockWindow')
#
#
# def run():
#     win = TestDockableWindow()
#     win.show()


def reload_all_modules(package_name: str):
    for m in list(sys.modules):
        if package_name in m:
            del (sys.modules[m])


# delete window if exists
# def delete_window(window_name: str):
#     try:
#         cmds.deleteUI(window_name)
#     except Exception:
#         traceback.print_exc()


def main():
    reload_all_modules('exportTanks')
    # delete_workspace_control('Tank Common ExporterWorkspaceControl')
    show()
    # name = 'TankExporterDockWindow'
    # delete_window(name)
    # delete_window('TankExporterDockWindowWorkspaceControl')
    # d_w = MyDockableWidget()
    # d_w.show(dockable=True, floating=True, area='right')
    # wnd = TankExportMainWindow()
    # wnd.show()
    # cmds.workspaceControl(name, retain=False, floating=True, label='Tank Exporter 2023',
    #                       uiScript='run()')
    # cmds.workspaceControl(name, retain=False, floating=True, label='Tank Exporter 2023')

    # Session.mixin_window = TankExporterDockableWindow()

    # mixin_window.show(dockable=True, floating=True, area='right')


if __name__ == '__main__':
    main()
