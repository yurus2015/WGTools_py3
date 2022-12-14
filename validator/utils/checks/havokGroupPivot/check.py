import maya.cmds as cmds
import re

checkId = 371
checkLabel = "Check Havok Group Pivot"


def removeDupplicateList(currentList):
    resultList = list(set(currentList))
    return resultList


def pivotTransform(transform):
    obj_rotatePivot = cmds.xform(transform, q=1, ws=1, rp=1)
    obj_scalePivot = cmds.xform(transform, q=1, ws=1, sp=1)
    if obj_rotatePivot != [0.0, 0.0, 0.0] or obj_scalePivot != [0.0, 0.0, 0.0]:
        return True
    return None


def main():
    validNames = ['^d_wood', '^d_stone', '^d_metal', '_havok']
    # objList = vl_listAllTransforms()
    objList = cmds.ls(tr=1)
    returnList = []
    resultList = []

    for obj in objList:
        for name in validNames:
            if re.findall(name, obj):
                resultList.append(cmds.ls(obj, l=1)[0])
    # print 'Check Group', obj
    if resultList:
        children = cmds.listRelatives(resultList, ad=1, type="transform", f=True)
        # print 'Children Check ', children
        if children:
            for child in children:
                resultList.append(child)

        resultList = removeDupplicateList(resultList)
        for res in resultList:
            if pivotTransform(res):
                tmp = []
                tmp.append(res)
                tmp.append(res)
                returnList.append(tmp)

    return returnList
