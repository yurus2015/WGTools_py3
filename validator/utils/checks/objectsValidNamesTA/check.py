import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 34
checkLabel = "8.6 Check names of objects TechArt"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    groupList = vl_listAllGroups()
    validNamesList = vl_tanksValidNames_techArt()
    groupValidNamesList = vl_tankGroupsValidNames_techArt()
    objectData = vl_objMeshData()
    returnList = []

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
            # 10 - index of "lod" re.compile name in validator_API
            temp = y.search(x)
            if temp != None:
                valid = 1
        if valid == 0:
            tmp = []
            tmp.append(x)
            tmp.append(x)
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
