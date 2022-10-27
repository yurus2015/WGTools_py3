import maya.cmds as cmds

from validator.utils.validator_API import *

checkId = 210

checkLabel = "GB Check missing objects"


def main():
    returnList = []

    objectsPatterns = ["Engine", \
                       "Radio", \
                       "FuelTank", \
                       "AmmoBay", \
                       "Commander", \
                       "Driver", \
                       "track_L", \
                       "track_R", \
                       "chassis", \
                       "hull", \
                       "turret_01", \
                       "Radioman_1", \
                       "Radioman_2", \
                       "Gunner_1", \
                       "Gunner_2", \
                       "Loader_1", \
                       "Loader_2", \
                       "TurretRotator", \
                       "Transmission", \
                       "gun_01"]

    allObjects = cmds.ls(type="mesh", l=1)
    if not allObjects:
        return returnList

    allTransforms = list(set(cmds.listRelatives(allObjects, p=1, type="transform")))
    chassis = cmds.ls("*chassis*")
    if chassis:
        allTransforms.append(chassis[0])

    for i in objectsPatterns:
        if i not in allTransforms:
            tmp = []
            tmp.append(i + " is absent")
            tmp.append(i)
            returnList.append(tmp)

    return returnList
