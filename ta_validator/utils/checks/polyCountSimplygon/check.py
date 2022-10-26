import maya.cmds as cmds
import math
import validator2019.utils.validator_API as vl
checkId = 100
checkLabel = "1.2.1 Check simplygon polycount"



def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []
    transforms = vl.vl_listAllTransforms()
    transforms.sort()

    lod0_hull_turret =[]
    lod0_gun_chassis = []

    lod1_hull_turret =[]
    lod1_gun_chassis = []

    lod2_hull_turret =[]
    lod2_gun_chassis = []

    lod3_hull_turret =[]
    lod3_gun_chassis = []

    lod4 = []


    for x in transforms:

        if x.find("lod0") != -1:
            if x.find("chassis") != -1 or  x.find("gun") != -1:
                lod0_gun_chassis.append(x)
            else:
                lod0_hull_turret.append(x)

        elif x.find("lod1") != -1:
            if x.find("chassis") != -1 or  x.find("gun") != -1:
                lod1_gun_chassis.append(x)
            else:
                lod1_hull_turret.append(x)

        elif x.find("lod2") != -1:
            if x.find("chassis") != -1 or  x.find("gun") != -1:
                lod2_gun_chassis.append(x)
            else:
                lod2_hull_turret.append(x)

        elif x.find("lod3") != -1:
            if x.find("chassis") != -1 or  x.find("gun") != -1:
                lod3_gun_chassis.append(x)
            else:
                lod3_hull_turret.append(x)

        elif x.find("lod4") != -1:
            lod4.append(x)


    lod0_hull_turret_polycount = cmds.polyEvaluate(lod0_hull_turret, t=1)
    lod0_gun_chassis_polycount = cmds.polyEvaluate(lod0_gun_chassis, t=1)

    lod1_hull_turret_polycount = cmds.polyEvaluate(lod1_hull_turret, t=1)
    lod1_gun_chassis_polycount = cmds.polyEvaluate(lod1_gun_chassis, t=1)

    lod2_hull_turret_polycount = cmds.polyEvaluate(lod2_hull_turret, t=1)
    lod2_gun_chassis_polycount = cmds.polyEvaluate(lod2_gun_chassis, t=1)

    lod3_hull_turret_polycount = cmds.polyEvaluate(lod3_hull_turret, t=1)
    lod3_gun_chassis_polycount = cmds.polyEvaluate(lod3_gun_chassis, t=1)

    lod4_polycount = cmds.polyEvaluate(lod4, t=1)


    if lod0_hull_turret_polycount + lod0_gun_chassis_polycount > 50000:
        message = "lod0 out of range with " +  str(lod0_hull_turret_polycount + lod0_gun_chassis_polycount) + " tris > max polycount: " + str(50000) + "\n"
        tmp = []
        tmp.append(message)
        tmp.append(lod0_hull_turret + lod0_gun_chassis )
        returnList.append(tmp)



    if lod1_hull_turret_polycount > 0.2 * lod0_hull_turret_polycount:
        message = "lod1 hull & turret out of range with " +  str(lod1_hull_turret_polycount) + " tris > max polycount: " + str(int(math.ceil(0.2 * lod0_hull_turret_polycount))) + "\n"
        tmp = []
        tmp.append(message)
        tmp.append(lod1_hull_turret)
        returnList.append(tmp)

    if lod1_gun_chassis_polycount > 0.3 * lod0_gun_chassis_polycount:
        message = "lod1 gun & chassis out of range with " +  str(lod1_gun_chassis_polycount) + " tris > max polycount: " + str(int(math.ceil(0.3 * lod0_gun_chassis_polycount))) + "\n"
        tmp = []
        tmp.append(message)
        tmp.append(lod1_gun_chassis)
        returnList.append(tmp)






    if lod2_hull_turret_polycount > 0.1 * lod0_hull_turret_polycount:
        message = "lod2 hull & turret out of range with " +  str(lod2_hull_turret_polycount) + " tris > max polycount: " + str(int(math.ceil(0.1 * lod0_hull_turret_polycount))) + "\n"
        tmp = []
        tmp.append(message)
        tmp.append(lod2_hull_turret)
        returnList.append(tmp)

    if lod2_gun_chassis_polycount > 0.15 * lod0_gun_chassis_polycount:
        message = "lod2 gun & chassis out of range with " +  str(lod2_gun_chassis_polycount) + " tris > max polycount: " + str(int(math.ceil(0.15 * lod0_gun_chassis_polycount))) + "\n"
        tmp = []
        tmp.append(message)
        tmp.append(lod2_gun_chassis)
        returnList.append(tmp)






    if lod3_hull_turret_polycount > 0.05 * lod0_hull_turret_polycount:
        message = "lod3 hull & turret out of range with " +  str(lod3_hull_turret_polycount) + " tris > max polycount: " + str(int(math.ceil(0.05 * lod0_hull_turret_polycount))) + "\n"
        tmp = []
        tmp.append(message)
        tmp.append(lod3_hull_turret)
        returnList.append(tmp)

    if lod3_gun_chassis_polycount > 0.075 * lod0_gun_chassis_polycount:
        message = "lod3 gun & chassis out of range with " +  str(lod3_gun_chassis_polycount) + " tris > max polycount: " + str(int(math.ceil(0.075 * lod0_gun_chassis_polycount))) + "\n"
        tmp = []
        tmp.append(message)
        tmp.append(lod3_gun_chassis)
        returnList.append(tmp)







    if lod4_polycount > 500:
        message = "lod4 out of range with " +  str(lod4_polycount) + " tris > max polycount: " + str(500) + "\n"
        tmp = []
        tmp.append(message)
        tmp.append(lod4)
        returnList.append(tmp)

    return returnList

