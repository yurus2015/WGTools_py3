import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 202
checkLabel = "GB Check invalid mesh names"


def main():
    returnList = []

    availableNames = ["hull", "chassis_0", "turret_01", "turret_02", "gun_01", "gun_02", "gun_03", "gun_04", "gun_05",
                      "gun_06", "gun_07", "gun_08", "gun_09", "gun_10", "gun_11", "gun_12", "gun_13", "gun_14", \
                      "track_L", "track_R", "chassis_L", "chassis_R", \
                      "Engine", "AmmoBay", "TurretRotator", "SurveyingDevice", "FuelTank", "Radio", "Commander",
                      "Driver", "Radioman_1", "Radioman_2", "Gunner_1", "Gunner_2", "Loader_1", "Loader_2",
                      "Transmission"]

    allObjects = cmds.listRelatives(cmds.ls(type="mesh"), p=1)
    if not allObjects:
        return returnList
    allObjects = list(set(allObjects))

    for x in allObjects:
        if x not in availableNames:
            tmp = []
            tmp.append(x)
            tmp.append(x)
            returnList.append(tmp)

    return returnList
