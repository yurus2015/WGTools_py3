import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 24
checkLabel = "3.20 Check LOD groups with non-zero pivots"


def main():
    returnList = []

    upLevelObjectsList = cmds.ls("*lod*", tr=1, r=1)

    for obj in upLevelObjectsList:
        rotatePivot = cmds.xform(obj, q=1, ws=1, rp=1)
        scalePivot = cmds.xform(obj, q=1, ws=1, sp=1)
        # Dobavit' okruglenia do 3-4 znakov posle zap9toi
        rotatePivot[0] = round(rotatePivot[0], 5)
        rotatePivot[1] = round(rotatePivot[1], 5)
        rotatePivot[2] = round(rotatePivot[2], 5)
        scalePivot[0] = round(scalePivot[0], 5)
        scalePivot[1] = round(scalePivot[1], 5)
        scalePivot[2] = round(scalePivot[2], 5)
        # print rotatePivot, scalePivot

        if rotatePivot != [0, 0, 0] or scalePivot != [0, 0, 0]:
            tmp = []
            tmp.append(obj)
            tmp.append(obj)
            returnList.append(tmp)

    return returnList
