import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 20
checkLabel = "Check orientation of joints"


def main():
    returnList = []
    LIST_joints = cmds.ls(type="joint")
    for x in LIST_joints:
        orient_X = cmds.getAttr(x + ".jointOrientX")
        orient_Y = cmds.getAttr(x + ".jointOrientX")
        orient_Z = cmds.getAttr(x + ".jointOrientX")
        if orient_X != 0.0 or orient_Y != 0.0 or orient_Z != 0.0:
            tmp = []
            tmp.append(x + " has non-zero orientation")
            tmp.append(x)
            returnList.append(tmp)

    return returnList
