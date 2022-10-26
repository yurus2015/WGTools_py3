import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 208
checkLabel = "GB Check for absent surveying device"

def checkForSurveyingDevice(mesh):
    result = None

    pattern = "surveyingDevice"

    meshMaterials = []

    cmds.select(mesh)
    cmds.hyperShade(smn=1)
    meshMaterials = cmds.ls(sl=1,l=1,fl=1)

    if pattern in meshMaterials:
        result = pattern
    else:
        result = None

    return result


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []

    hullList = cmds.ls("*hull*", type="transform", l=1)
    turretList = cmds.ls("*turret*", type="transform", l=1)
    gunList = cmds.ls("*gun*", type="transform")

    for i in hullList:
        hasSV = checkForSurveyingDevice(i)

        if not hasSV:
            tmp = []
            tmp.append(i)
            tmp.append(i)
            returnList.append(tmp)

    turretFound = None
    for i in turretList:
        hasSV = checkForSurveyingDevice(i)
        if hasSV:
            turretFound = 1
        else:
            tmp = []
            tmp.append(i)
            tmp.append(i)
            returnList.append(tmp)

    if not turretFound:
        for i in gunList:
            hasSV = checkForSurveyingDevice(i)

            if not hasSV:
                tmp = []
                tmp.append(i)
                tmp.append(i)
                returnList.append(tmp)

    return returnList



