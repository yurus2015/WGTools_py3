import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 13
checkLabel = "Check Gun, Gun_bsp pivots match"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []

    listGuns = []
    listGuns_bsp = []

    gun_expression = re.compile("gun_0\d");
    gun_bsp = re.compile("_bsp")

    for z in vl_listLodsGroups():     #For each group found in vl_listLodsGroups()
        #List only track objects
        listObjects = cmds.listRelatives (z, c=True, f=True, ad=True)
        for x in listObjects:         #traversing lod group and trying to find track and hull objects
            if gun_expression.search(x):
                if not gun_bsp.search(x):
                    if cmds.listRelatives(x, s=True) != None:   #if transform have connections it's mean it's mesh
                        listGuns.append(x)

        for x in listObjects:
            if gun_expression.search(x):
                if gun_bsp.search(x):
                    if cmds.listRelatives(x, s=True) != None:   #if transform have connections it's mean it's mesh
                        listGuns_bsp.append(x)

    for x in listGuns_bsp:
        for y in listGuns:
            if x.find(y) != -1:
                gP = cmds.xform(y, q= True, ws=True, rp=True)
                gBspP = cmds.xform(x, q= True, ws=True, rp=True)

                gP[0] = round(gP[0], 3); gP[1] = round(gP[1], 3); gP[2] = round(gP[2], 3);
                gBspP[0] = round(gBspP[0], 3); gBspP[1] = round(gBspP[1], 3); gBspP[2] = round(gBspP[2], 3)

                if gP[0] != gBspP[0] or gP[1] != gBspP[1] or gP[2] != gBspP[2]:
                    tmp = []
                    tmp.append(x)
                    tmp.append(x)

                    tmp2 = []
                    tmp2.append(y)
                    tmp2.append(y)

                    returnList.append(tmp)
                    returnList.append(tmp2)

    return  returnList




