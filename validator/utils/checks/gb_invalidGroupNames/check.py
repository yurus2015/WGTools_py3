import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 203
checkLabel = "GB Check invalid group names"


def getGroups():
    allTransforms = cmds.ls(type="transform", l=1)
    groups = []

    for i in allTransforms:
        if not cmds.listRelatives(i, s=1):
            groups.append(i)

    return groups

def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []

    availableGroups = ["|collision",  "|collision|chassis"]
    groups = getGroups()

    for i in groups:
        if i not in availableGroups:
            tmp = []
            tmp.append(i)
            tmp.append(i)
            returnList.append(tmp)

    return returnList

