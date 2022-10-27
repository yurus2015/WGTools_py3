import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 25

checkLabel = "8.2 Check hierarchy of materials"


def main():
    objMatData = vl_objMaterialsData()

    returnList = []

    hull = re.compile('hull');
    hull_list = []
    hull_inside = re.compile('inside');
    hull_inside_list = []
    gun = re.compile('gun');
    gun_list = []
    turret = re.compile('turret');
    turret_list = []
    chassis = re.compile('chassis');
    chassis_list = []
    track = re.compile('track');
    track_list = []

    for x in objMatData:
        if 'proxy' in x[3]:
            continue

        if hull.search(x[1]) is not None:
            if hull_inside.search(x[1]) is not None:
                hull_inside_list.append(x)
            else:
                hull_list.append(x)

        if gun.search(x[1]) is not None:
            gun_list.append(x)
        if turret.search(x[1]) is not None:
            turret_list.append(x)
        if chassis.search(x[1]) is not None and track.search(x[1]) is None:
            chassis_list.append(x)
        if track.search(x[1]) is not None:
            track_list.append(x)

    def searchFunction(array, searchName):
        if len(array) > 0:
            for z in array:
                result = False
                if z[0] != 0:
                    if searchName.search(z[3]) is not None:
                        result = True
                if not result:
                    tmp = []
                    tmp.append(z[1])
                    tmp.append(z[1])
                    returnList.append(tmp)

    searchFunction(track_list, track)
    searchFunction(hull_list, hull)
    searchFunction(hull_inside_list, hull_inside)
    searchFunction(gun_list, gun)
    searchFunction(turret_list, turret)
    searchFunction(chassis_list, chassis)

    return returnList
