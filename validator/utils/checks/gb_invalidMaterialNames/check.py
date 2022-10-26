import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 204
checkLabel = "GB Check invalid material names"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []

    availableMaterials = ["lambert1", \
                        "particleCloud1",  \
                        "engine", \
                        "ammoBay", \
                        "leftTrack",\
                        "rightTrack", \
                        "gun", \
                        "turretRotator", \
                        "surveyingDevice", \
                        "fuelTank", \
                        "radio", \
                        "commander", \
                        "driver", \
                        "radioman_1", \
                        "radioman_2", \
                        "gunner_1", \
                        "gunner_2", \
                        "loader_1", \
                        "loader_2",\
                        "chassisPart",\
                        "gunBreech",\
                        "transmission",\
                        "armor_1", \
                        "armor_2", \
                        "armor_3", \
                        "armor_4", \
                        "armor_5", \
                        "armor_6", \
                        "armor_7", \
                        "armor_8", \
                        "armor_9", \
                        "armor_10", \
                        "armor_11", \
                        "armor_12", \
                        "armor_13", \
                        "armor_14", \
                        "armor_15", \
                        "armor_16", \
                        "armor_17", \
                        "armor_18", \
                        "armor_19", \
                        "armor_20", \
                        "armor_21", \
                        "armor_22", \
                        "armor_23", \
                        "armor_24", \
                        "armor_25", \
                        "armor_26", \
                        "armor_27", \
                        "armor_28", \
                        "armor_29", \
                        "armor_30", \
                        "armor_31", \
                        "armor_32"]

    matList = cmds.ls(mat=1)

    for i in matList:
         if i not in availableMaterials:
            tmp = []
            tmp.append(i)
            tmp.append(i)
            returnList.append(tmp)

    return  returnList
