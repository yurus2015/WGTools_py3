import maya.cmds as cmds
from validator2019.utils.validator_API import *

import json
import os
dir = os.path.dirname(__file__)


checkId = 712
checkLabel = "5.12 Check objects height"


def get_height(obj):
    xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(obj, q=True, bb=True)
    return round(ymax, 3)


def get_bbox_height(obj):
    xmin, ymin, zmin, xmaz, ymax, zmax = cmds.xform(obj, q=True, bb=True)
    return round((ymax - ymin), 3)


def main():
    print('<< ' + checkLabel.upper() + ' >>')

#read json file
    json_file = open(("%s//%s") % (dir, "objectHeightSettings.json"))
    json_string = json_file.read()
    settings = json.loads(json_string)

    return_list = []

    ramp = []
    wall = []

    for x in vl_listAllTransforms():
        if (x.find("ramp") !=-1 and x.find("bsp") !=-1) or ("ramp" in x):
            ramp.append(x)

        if x.find("wall") !=-1:
            wall.append(x)

    # original
    # for x in ramp:
    #     if get_height(x) > settings["ramp"]:
    #         return_list.append(["%s ramp height is %s > %s" % (x, get_height(x), settings["ramp"]), x])


    for x in ramp:
        if get_height(x) < settings["ramp_min"]:
            return_list.append(["%s ramp height is %s < %s" % (x, get_height(x), settings["ramp_min"]), x])

        elif get_height(x) > settings["ramp_max"]:
            return_list.append(["%s ramp height is %s > %s" % (x, get_height(x), settings["ramp_max"]), x])

    for x in wall:
        if get_height(x) < settings["wall"]:
            return_list.append(["%s wall height is %s < %s" % (x, get_height(x), settings["wall"]), x])

    return return_list

