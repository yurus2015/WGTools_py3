import maya.cmds as cmds
from validator.utils.validator_API import *

import json
import os

dir = os.path.dirname(__file__)

checkId = 714
checkLabel = "5.2 Check bsp position"


def check_out_of_bbox(obj):
    x, y, z = cmds.xform(obj, q=True, rp=True, ws=True)
    x_min, y_min, z_min, x_max, y_max, z_max = cmds.xform(obj, q=True, bb=True)

    E = 0.01

    if x > x_max + E or x < x_min - E:
        return True
    if y > y_max + E or y < y_min - E:
        return True
    if z > z_max + E or z < z_min - E:
        return True


def main():
    #

    json_file = open(("%s//%s") % (dir, "BSPPositionSettings.json"))
    json_string = json_file.read()
    settings = json.loads(json_string)

    return_list = []

    pairs = {}

    for x in vl_listAllTransforms():
        if x.find("_bsp") != -1:
            for y in vl_listAllTransforms():
                if x[:-4] == y:
                    pairs[y] = x

    t = settings["tolerance"]
    for i in pairs:
        x, y, z = cmds.xform(i, q=True, rp=True, ws=True)
        x_bsp, y_bsp, z_bsp = cmds.xform(pairs[i], q=True, rp=True, ws=True)

        mistake = False

        if check_out_of_bbox(i):
            return_list.append([("pivot of %s out of bounding box") % (i), i])
            mistake = True
        if check_out_of_bbox(pairs[i]):
            return_list.append([("pivot of %s out of bounding box") % (pairs[i]), pairs[i]])
            mistake = True
        if mistake:
            continue

        if x_bsp > x + t or x_bsp < x - t:
            mistake = True
        if y_bsp > y + t or y_bsp < y - t:
            mistake = True
        if z_bsp > z + t or z_bsp < z - t:
            mistake = True

        if mistake:
            return_list.append([("bsp of %s has wrong position") % (i), pairs[i]])

    return return_list
