import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 12
checkLabel = "1.13 Check objects with non-zero transformations"


def removeList(fromList, thisList):
    resultList = [n for n in fromList if n not in thisList]
    resultList = list(resultList)
    return resultList


def main():
    objList = vl_listAllTransforms()
    groupList = vl_listAllGroups()
    returnList = []
    hpList = []
    shapeArray = cmds.ls(type='mesh', dag=1, l=True)
    if shapeArray:
        polyArray = list(set(cmds.listRelatives(shapeArray, p=1, type="transform", f=True)))
        for m in polyArray:
            if 'HP' in m:
                hpList.append(m)
        polyArray = removeList(polyArray, hpList)
        polyArray.extend(groupList)

        # Check for objects with non-zero transformations
        for obj in polyArray:
            objTranslate = cmds.xform(obj, q=1, t=1)
            objRotate = cmds.xform(obj, q=1, ro=1)
            objScale = cmds.xform(obj, q=1, r=1, s=1)
            if (objTranslate != [0, 0, 0] or objRotate != [0, 0, 0] or objScale != [1, 1, 1]):
                tmp = []
                tmp.append(obj)
                tmp.append(obj)
                returnList.append(tmp)

    return returnList
