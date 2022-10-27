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
import maya.cmds as cmds
import simplygon_tools.gui.main_window as wnd

print('Simplygon_Tools')


def main():
    if cmds.window('SimplygonTanksWindow', q=True, exists=True):
        cmds.deleteUI('SimplygonTanksWindow')

    window = wnd.TanksWindow()
    window.show()
    print('run')


def reload_all_modules():
    for m in list(sys.modules):
        if 'simplygon_tools' in m:
            print(m)
            del (sys.modules[m])


if __name__ == '__main__':
    reload_all_modules()
    main()
