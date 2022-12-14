import sys
from maya import cmds

from skinning_tools.gui.vs_main_window import STMainWindow


def reload_all_modules():
    for m in list(sys.modules):
        if 'skinning_tools' in m:
            print(m)
            del (sys.modules[m])


def main():
    if cmds.window('SkinningToolsWindow', q=True, exists=True):
        cmds.deleteUI('SkinningToolsWindow')

    window = STMainWindow()
    window.show()


if __name__ == '__main__':
    reload_all_modules()
    main()
