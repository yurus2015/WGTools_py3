import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 37
checkLabel = "3.26 Check Rotate Pivot and Scale Pivot values"


def main():
    objList = vl_listAllTransforms()
    returnList = []

    shapeArray = cmds.ls(type='mesh', dag=1, l=True)
    if shapeArray:
        polyArray = list(set(cmds.listRelatives(shapeArray, p=1, type="transform", f=True)))

        for obj in polyArray:
            obj_pivot = cmds.xform(obj, q=1, ws=1, rp=1)
            obj_scalePivot = cmds.xform(obj, q=1, ws=1, sp=1)

            obj_pivot[0] = round(obj_pivot[0], 5)
            obj_pivot[1] = round(obj_pivot[1], 5)
            obj_pivot[2] = round(obj_pivot[2], 5)
            obj_scalePivot[0] = round(obj_scalePivot[0], 5)
            obj_scalePivot[1] = round(obj_scalePivot[1], 5)
            obj_scalePivot[2] = round(obj_scalePivot[2], 5)

            if obj_pivot != obj_scalePivot:
                tmp = []
                tmp.append(obj)
                tmp.append(obj)
                returnList.append(tmp)

    return returnList
