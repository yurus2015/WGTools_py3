'''
1. re-factory gui
1. edit preset xml
2. run cmd file for every preset

4. check execute cmd file
5. import lods from temp dirs
6. export fbx models to input
7. cmd file with arguments? for example: execute.cmd chassis
'''
import sys
import importlib, types
import maya.cmds as cmds
import simplygon_tools.gui.main_window as wnd
from simplygon_tools.utils.constants import *


def main():
    if cmds.window('SimplygonTanksWindow', q=True, exists=True):
        cmds.deleteUI('SimplygonTanksWindow')

    window = wnd.TanksWindow()
    window.show()

    #  log window: comments after debug
    if cmds.window('SimplygonLog', q=True, exists=True):
        cmds.deleteUI('SimplygonLog')

    # log_window = wnd.LogWindow()
    # log_window.show()
    # log_window.raise_()
    # log_window.log_text_box.emit('Start')
    # Storage.SIMPLYGON_LOG_WINDOW = log_window
    # print('run', log_window)

    # copilot_window = wnd.MainWindow()
    # copilot_window.show()
    # copilot_window.raise_()
    # print('run', copilot_window)


def reload_all_modules():
    for m in list(sys.modules):
        if 'simplygon_tools' in m:
            print(m)
            del (sys.modules[m])


# this code generated ChatGPT
# doesn't work for me
def reload_project_modules(project):
    # Import all modules in the project
    imported_project = __import__(project)

    # Reload all modules in the project
    for module in imported_project.__dict__.values():
        if isinstance(module, types.ModuleType):
            importlib.reload(module)


if __name__ == '__main__':
    reload_all_modules()
    # reload_project_modules('simplygon_tools')
    main()
