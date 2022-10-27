import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 205
checkLabel = "GB Check invalid layer names"


def main():
    returnList = []
    fileName = cmds.file(q=1, sn=1)

    if "collision" in fileName:
        availableLayers = ["defaultLayer", "Hull", "Chassis", "Turret_01", "Turret_02", "Gun_01", "Gun_02", "Gun_03",
                           "Gun_04", "Gun_05", "Gun_06", "Gun_07", "Gun_08", "Gun_09", "Gun_10", "Gun_11", "Gun_12",
                           "Gun_13", "Gun_14"]
        layers = cmds.ls(type="displayLayer")
        for i in layers:
            if i not in availableLayers:
                tmp = []
                tmp.append(i)
                tmp.append(i)
                returnList.append(tmp)

    return returnList
