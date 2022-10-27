import maya.cmds as cmds


def removeDupplicateList(currentList):
    resultList = list(set(currentList))
    return resultList


def listTransform():
    objsTransform = cmds.ls(type='transform', l=1, sl=1)
    objsTransform = cmds.filterExpand(objsTransform, sm=12)
    objsTransform = removeDupplicateList(objsTransform)
    return objsTransform


def swapUV(objList):
    for obj in objList:

        uvSets = cmds.polyUVSet(obj, query=True, allUVSets=True)  # get all uvSets
        if uvSets:
            if len(uvSets) == 2:
                currentSet = cmds.polyUVSet(obj, q=1, currentUVSet=1)
                cmds.polyUVSet(obj, copy=True, uvSet=uvSets[0], nuv='temp')
                cmds.polyUVSet(obj, currentUVSet=True, uvSet=uvSets[1])
                cmds.delete(obj, ch=1)
                cmds.polyCopyUV(obj, uvi=uvSets[1], uvs=uvSets[0])
                cmds.delete(obj, ch=1)
                cmds.polyCopyUV(obj, uvi='temp', uvs=uvSets[1])
                cmds.delete(obj, ch=1)
                cmds.polyUVSet(obj, delete=True, uvSet='temp')
                cmds.delete(obj, ch=1)
                cmds.polyUVSet(obj, currentUVSet=True, uvSet=currentSet[0])

    cmds.select(objList)


def main():
    swapUV(listTransform())
