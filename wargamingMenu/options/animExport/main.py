import maya.cmds as cmds
from PySide2.QtGui import *
from anim_export.gui import Animation_Export


def main():
    if cmds.window("AnimationExportWindow", q=True, exists=True):
        cmds.deleteUI("AnimationExportWindow")
    try:
        cmds.deleteUI('MayaWindow|AnimationExportWindow')
    except:
        pass
    instance = Animation_Export()
    instance.show()
    pos = QCursor.pos()
    instance.move(pos.x() - (instance.width() / 2), pos.y() - (instance.height() / 2))
