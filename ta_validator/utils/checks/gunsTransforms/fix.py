import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 15
checkLabel = "8.8 Check transformations of guns"


def main(*args):

    if args:
        for x in args:
            cmds.setAttr(x + ".tx", l = False)
            cmds.setAttr(x + ".ty", l = False)
            cmds.setAttr(x + ".tz", l = False)
            cmds.setAttr(x + ".rx", l = False)
            cmds.setAttr(x + ".ry", l = False)
            cmds.setAttr(x + ".rz", l = False)
            cmds.setAttr(x + ".sx", l = False)
            cmds.setAttr(x + ".sy", l = False)
            cmds.setAttr(x + ".sz", l = False)

    return []