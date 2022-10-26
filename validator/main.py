from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.cmds as cmds
import sys
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from validator.gui.gui import *
from validator.gui.constants import AUTOLOADOPTION


def delete_ui():
    if cmds.workspaceControl(ValidatorMainWindow.CONTROL_NAME, ex=True):
        cmds.deleteUI(ValidatorMainWindow.CONTROL_NAME)

    if cmds.workspaceControl('Validator 2019', ex=True):
        cmds.deleteUI('Validator 2019')


def main(autoload=True):
    if autoload:
        if cmds.optionVar(exists=AUTOLOADOPTION):
            if cmds.optionVar(q=AUTOLOADOPTION) == 0:
                delete_ui()
                return

    delete_ui()
    cmds.workspaceControl(ValidatorMainWindow.CONTROL_NAME, retain=False, floating=True,
                          uiScript="python(\"import validator.main as vld\\nvld.main(autoload = False)\");")
    control_widget = omui.MQtUtil.findControl(ValidatorMainWindow.CONTROL_NAME)
    control_wrap = wrapInstance(int(control_widget), QWidget)
    control_wrap.setAttribute(Qt.WA_DeleteOnClose)
    cmds.workspaceControl(ValidatorMainWindow.CONTROL_NAME, e=True, label=ValidatorMainWindow.DOCK_LABEL_NAME)
    ValidatorMainWindow(control_wrap)


if __name__ == "__main__":
    packages = ['validator']
    for i in list(sys.modules.keys()):
        for package in packages:
            if i.startswith(package):
                try:
                    del sys.modules[i]
                except:
                    pass

    # import validator.main as vld
	#
    # vld.main(autoload=False)
    main(False)
