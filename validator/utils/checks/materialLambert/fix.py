import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 26
checkLabel = "3.3 Check Objects with material type different from Lambert"


def correctMat(obj, matName):
    existingMatList = cmds.ls(mat=1)
    correctMatName = matName

    if obj.find("turret") != -1 or obj.find("Turret") != -1:
        num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        if obj[-1] in num:
            correctMatName = correctMatName.replace(correctMatName[-1], obj[-1])

    if correctMatName in existingMatList:
        # if material exists
        cmds.select(obj)
        cmds.hyperShade(assign=correctMatName)
    else:
        # create new material and assign it
        newMat = cmds.shadingNode('lambert', n=correctMatName, asShader=1)
        cmds.select(obj)
        cmds.hyperShade(assign=newMat)


def main(*args):
    if args:
        for i in args:
            if i.find("gun") != -1 or i.find("Gun") != -1:
                correctMat(i, "tank_guns")
            elif i.find("turret") != -1 or i.find("Turret") != -1:
                correctMat(i, "tank_turret_01")
            elif i.find("hull") != -1 or i.find("Hull") != -1:
                correctMat(i, "tank_hull_01")
            elif i.find("track_L") != -1 or i.find("Track_L") != -1:
                correctMat(i, "track_mat_L")
            elif i.find("track_R") != -1 or i.find("Track_R") != -1:
                correctMat(i, "track_mat_R")
            elif i.find("chassis") != -1 or i.find("Chassis") != -1 or i.find("w_") != -1 or i.find(
                    "W_") != -1 or i.find("wd_") != -1 or i.find("Wd_") != -1:
                correctMat(i, "tank_chassis_01")
    return []
