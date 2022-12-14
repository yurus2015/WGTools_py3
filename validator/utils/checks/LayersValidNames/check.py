import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 22
checkLabel = "1.8 Check names of layers"


def main():
    validNamesList = vl_tanksLayersValidNames()

    objectData = cmds.ls(type="displayLayer")
    returnList = []

    for x in range(len(objectData)):
        valid = 0
        for y in validNamesList:
            temp = y.search(objectData[x])
            if temp != None:
                valid = 1
        if valid == 0:
            tmp = []
            tmp.append(objectData[x])
            tmp.append(objectData[x])
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

    return returnList
