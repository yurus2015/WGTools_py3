import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 7
checkLabel = "3.23 Check for chassis pivots"


def main():
    #

    # objList = vl_listAllTransforms()
    returnList = []

    chassisObj = cmds.ls("*chassis_*", r=1, l=True, type='transform')
    if (chassisObj):
        for obj in chassisObj:
            rotatePivot = cmds.xform(obj, q=1, ws=1, rp=1)
            scalePivot = cmds.xform(obj, q=1, ws=1, sp=1)
            rotatePivot[0] = round(rotatePivot[0], 3)
            rotatePivot[1] = round(rotatePivot[1], 3)
            rotatePivot[2] = round(rotatePivot[2], 3)
            scalePivot[0] = round(scalePivot[0], 3)
            scalePivot[1] = round(scalePivot[1], 3)
            scalePivot[2] = round(scalePivot[2], 3)

            if rotatePivot != [0, 0, 0] or scalePivot != [0, 0, 0]:
                tmp = []
                tmp.append(obj + " has incorrect pivots world coordinates")
                tmp.append(obj)
                returnList.append(tmp)

    return returnList
