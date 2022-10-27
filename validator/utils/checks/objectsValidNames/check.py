import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

from validator.utils.validator_API import *

checkId = 34
checkLabel = "8.6 Check names of objects"


def checkSide(obj, side):
    if obj:
        selectionList = OpenMaya.MSelectionList()
        selectionList.clear()
        selectionList.add(obj)

        dagPath = OpenMaya.MDagPath()
        selectionList.getDagPath(0, dagPath)

        dagNodeFn = OpenMaya.MFnDagNode(dagPath)
        bbox = dagNodeFn.boundingBox()

        if side == "R":
            if bbox.min().x > 0:
                return 1
        elif side == "L":
            if bbox.max().x < 0:
                return 1


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    groupList = vl_listAllGroups()
    validNamesList = vl_tanksValidNames()
    groupValidNamesList = vl_tankGroupsValidNames()
    objectData = vl_objMeshData()
    returnList = []

    # dom didom dom dom - KOSTIL'
    rawFilePath = cmds.file(q=True, exn=True)
    if "G_Tiger" in rawFilePath or "G45_G_Tiger" in rawFilePath:
        return returnList

    for x in range(len(objectData)):
        valid = 0
        for y in validNamesList:
            temp = y.search(objectData[x][3])
            if temp != None:
                valid = 1
        if valid == 0:
            tmp = []
            tmp.append(objectData[x][1])
            tmp.append(objectData[x][1])
            returnList.append(tmp)

    for x in groupList:
        valid = 0
        for y in groupValidNamesList:
            temp = y.search(x)
            if temp != None:
                valid = 1
        if valid == 0:
            tmp = []
            tmp.append(x)
            tmp.append(x)
            returnList.append(tmp)

    patterns = ["wd_L", "wd_R", "w_L", "w_R", "track_L", "track_R", "chassis_L", "chassis_R"]

    if objectData:
        for i in objectData:
            for pat in patterns:
                if pat in i[3]:
                    if "_R" in pat and not checkSide(i[1], "R"):
                        tmp = []
                        tmp.append(i[1] + " located on a wrong side of the scene")
                        tmp.append(i[1])
                        returnList.append(tmp)
                    elif "_L" in pat and not checkSide(i[1], "L"):
                        tmp = []
                        tmp.append(i[1] + " located on a wrong side of the scene")
                        tmp.append(i[1])
                        returnList.append(tmp)

    for x in validNamesList:
        pattern = x.pattern
        try:
            pattern = pattern.replace('\d', '#')
        except:
            pass
        try:
            pattern = pattern.replace('\Z', '')
        except:
            pass
        try:
            pattern = pattern.replace('^', '')
        except:
            pass

        # helpStringList.append(pattern)

    for x in groupValidNamesList:
        pattern = x.pattern
        try:
            pattern = pattern.replace('\d', '#')
        except:
            pass
        try:
            pattern = pattern.replace('\Z', '')
        except:
            pass
        try:
            pattern = pattern.replace('^', '')
        except:
            pass
        try:
            pattern = pattern.replace('[|]', '')
        except:
            pass

        # helpStringList.append(pattern)

    return returnList
