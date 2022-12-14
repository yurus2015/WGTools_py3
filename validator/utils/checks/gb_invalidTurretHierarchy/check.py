import maya.cmds as cmds

from validator.utils.validator_API import *

checkId = 209

checkLabel = "GB Check invalid turret hierarchy"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []

    turretList = cmds.ls("*turret*", type="transform", l=1)

    turretList_Size = len(turretList)

    turretList_InnerSize = []

    for i in turretList:
        rels = cmds.listRelatives(i, c=1, f=1, type="transform")
        if rels:
            turretList_InnerSize.append(len(rels))  # append number of inner elements of the current turret
        else:
            turretList_InnerSize.append(0)  # append number of inner elements of the current turret

    if len(turretList_InnerSize) > 0:
        result = list(set(turretList_InnerSize))
        if len(result) > 1:
            for i in turretList:
                tmp = []
                tmp.append(i)
                tmp.append(i)
                returnList.append(tmp)

    return returnList
