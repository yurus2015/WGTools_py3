import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 216
checkLabel = "GB Check invalid normals"


def main():
    returnList = []

    allTransforms = cmds.ls(tr=1, l=1, fl=1)
    for i in allTransforms:
        cmds.makeIdentity(i, apply=1, t=1, r=1, s=1, n=0, jointOrient=1)

    allMeshes = cmds.ls(type="mesh", l=1, fl=1)

    for i in allMeshes:
        cmds.setAttr(i + ".doubleSided", 0)
        opposite = cmds.getAttr(i + ".opposite")
        if opposite:
            print(i)
            cmds.setAttr(i + ".opposite", 0)
            tmp = []
            tmp.append(i)
            tmp.append(i)
            returnList.append(tmp)

    return returnList
