import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 715
checkLabel = "3.0 Check objects name"


def removeDupplicateList(currentList):
    resultList = list(set(currentList))
    return resultList


def main():
    print('<< 3.0 CHECK OBJECTS NAME >>')
    validNamesList = vl_objectsValidNames()
    returnList = []

    listAllMesh = cmds.ls(type='transform')
    listAllMesh = cmds.filterExpand(listAllMesh, sm=12)
    if listAllMesh:
        listAllMesh = removeDupplicateList(listAllMesh)
        listAllMesh = cmds.ls(listAllMesh, l=1)

        for hp in listAllMesh:
            valid = 0
            hp_shortName = hp.split('|')[-1]

            for y in validNamesList:
                temp = y.search(hp_shortName)
                if temp != None:
                    valid = 1
                    break
            if valid == 0:
                tmp = []
                tmp.append(hp)
                tmp.append(hp)
                returnList.append(tmp)
    return returnList
