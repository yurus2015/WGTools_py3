import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 45
checkLabel = "3.25 Check for track pivots"


def main():
    objList = vl_listAllTransforms()
    returnList = []
    chassisObj = cmds.ls("*track_*", r=1, l=True, type='transform')
    for obj in chassisObj:
        obj_pivot = cmds.xform(obj, q=1, ws=1, rp=1)
        obj_scalePivot = cmds.xform(obj, q=1, ws=1, sp=1)

        obj_pivot[0] = round(obj_pivot[0], 5)
        obj_pivot[1] = round(obj_pivot[1], 5)
        obj_pivot[2] = round(obj_pivot[2], 5)
        obj_scalePivot[0] = round(obj_scalePivot[0], 5)
        obj_scalePivot[1] = round(obj_scalePivot[1], 5)
        obj_scalePivot[2] = round(obj_scalePivot[2], 5)

        if obj_pivot != [0, 0, 0] or obj_scalePivot != [0, 0, 0]:
            tmp = []
            tmp.append(obj)
            tmp.append(obj)
            returnList.append(tmp)

    return returnList
