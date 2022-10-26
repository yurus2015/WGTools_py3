import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 46

checkLabel = "Check hierarchy of tracks and chassis (Normal only)"

def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []
    lodArray = cmds.ls("*lod*", type="transform")

    def findChassis(childArray):
        chassis_R = False
        chassis_L = False
        for y in childArray:
            if y.find("chassis_R") != -1:
                chassis_R = True
            if y.find("chassis_L") != -1:
                chassis_L = True
        if  not chassis_R or not chassis_L:
            tmp = []
            tmp.append(x + " - doesn't have chassis")
            tmp.append(x)
            returnList.append(tmp)

    def findTracks(childArray):
        track_R = False
        track_L = False
        for y in childArray:
            if y.find("track_R") != -1:
                track_R = True
            if y.find("track_L") != -1:
                track_L = True
        if 	not track_R or not track_L:
            tmp = []
            tmp.append(x + " - doesn't have tracks")
            tmp.append(x)
            returnList.append(tmp)

    def findWheels(childArray):
        w_Right = 0
        w_Left = 0

        for y in childArray:
            if y.find("wd_R") != -1 or y.find("w_R") != -1:
                w_Right += 1

            if y.find("wd_L") != -1 or y.find("w_L") != -1:
                w_Left += 1

        if  w_Right != w_Left:
            tmp = []
            tmp.append(x + " - different wheels count or wrong name of wheels on the sides")
            tmp.append(x)
            returnList.append(tmp)




    if len(lodArray) > 0:
        for x in lodArray:
            if x == "lod0":
                childArray = cmds.listRelatives(x, f=1, ad = True)
                findChassis(childArray)
                findTracks(childArray)
                findWheels(childArray)
            elif x == "lod1":
                childArray = cmds.listRelatives(x, f=1, ad = True)
                findChassis(childArray)
                findTracks(childArray)
                findWheels(childArray)

            elif x == "lod4":
                childArray = cmds.listRelatives(x, f=1, ad = True)
                findChassis(childArray)


    return  returnList



