import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 206
checkLabel = "GB Check invalid lambert name"


def main():
    returnList = []

    ISG = cmds.hyperShade(o="initialShadingGroup")
    selected = cmds.ls(sl=1, l=1)
    if selected:
        for i in selected:
            tmp = []
            tmp.append(i)
            tmp.append(i)
            returnList.append(tmp)

    return returnList
