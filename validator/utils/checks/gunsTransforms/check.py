import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 15
checkLabel = "8.8 Check transformations of guns"


def main():
    returnList = []
    gunList = []

    objList = cmds.ls("*gun*", type="mesh", l=1)
    if objList:
        gunList = list(set(cmds.listRelatives(objList, p=1, f=1)))

        if gunList:
            for x in gunList:
                if cmds.getAttr((x + '.tx'), l=True) or \
                        cmds.getAttr((x + '.ty'), l=True) or \
                        cmds.getAttr((x + '.tz'), l=True) or \
 \
                        cmds.getAttr((x + '.rx'), l=True) or \
                        cmds.getAttr((x + '.ry'), l=True) or \
                        cmds.getAttr((x + '.rz'), l=True) or \
 \
                        cmds.getAttr((x + '.sx'), l=True) or \
                        cmds.getAttr((x + '.sy'), l=True) or \
                        cmds.getAttr((x + '.sz'), l=True):
                    tmp = []
                    tmp.append(x)
                    tmp.append(x)
                    returnList.append(tmp)

    return returnList

    # returnList = []
    # listGuns = []
    # listGuns_bsp = []
    # gun_expression = re.compile("gun_0\d");
    # gun_bsp = re.compile("_bsp")

    # for z in vl_listLodsGroups():     #For each group found in vl_listLodsGroups()
    #     #List only track objects
    #     listObjects = cmds.listRelatives (z, c=True, f=True, ad=True)
    #     for x in listObjects:         #traversing lod group and trying to find track and hull objects
    #         if gun_expression.search(x):
    #             if not gun_bsp.search(x):
    #                 if cmds.listRelatives(x, s=True) != None:   #if transform have connections it's mean it's mesh
    #                     listGuns.append(x)

    #     for x in listObjects:
    #         if gun_expression.search(x):
    #             if gun_bsp.search(x):
    #                 if cmds.listRelatives(x, s=True) != None:   #if transform have connections it's mean it's mesh
    #                     listGuns_bsp.append(x)

    # def checkLock(array):
    #     for x in array:
    #         if cmds.getAttr((x +'.tx'), l=True) or\
    #            cmds.getAttr((x +'.ty'), l=True) or\
    #            cmds.getAttr((x +'.tz'), l=True) or\
    #            \
    #            cmds.getAttr((x +'.rx'), l=True) or\
    #            cmds.getAttr((x +'.ry'), l=True) or\
    #            cmds.getAttr((x +'.rz'), l=True) or\
    #            \
    #            cmds.getAttr((x +'.sx'), l=True) or\
    #            cmds.getAttr((x +'.sy'), l=True) or\
    #            cmds.getAttr((x +'.sz'), l=True):
    #             returnList.append(x)

    # checkLock(listGuns_bsp)
