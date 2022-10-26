import maya.cmds as cmds


def component_selected():
    if cmds.filterExpand(sm=(31, 32, 34)):
        return True
    else:
        return False


def align_x():
    cmds.scale(0, 1, 1)


def align_y():
    cmds.scale(1, 0, 1)


def align_z():
    cmds.scale(1, 1, 0)


def main(axis):
    if component_selected():
        if axis == 'x':
            align_x()
        if axis == 'y':
            align_y()
        if axis == 'z':
            align_z()
