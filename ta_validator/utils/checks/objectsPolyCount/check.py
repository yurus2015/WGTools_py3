import maya.cmds as cmds
from validator2019.utils.validator_API import *
import os
import math
dir = os.path.dirname(__file__)

checkId = 705
checkLabel = "3.5 Check objects polycount"

def filter_auxiliary_obejcts(obj):
    filtered_list = []
    for x in obj:
        if x.find("bsp") == -1 and\
           x.find("wall") == -1 and\
           x.find("ramp") == -1:
           filtered_list.append(x)
    return filtered_list

def main():
    print('<< ' + checkLabel.upper() + ' >>')
    return_list = []

    for x in vl_listRootGroups():
#get lod0 of each group:
        lod0 =  cmds.ls(x + "|lod0", l = True)
        if not lod0:
#if group doesn't have lod0 just pass it:
            continue
#get all objects in lod
        obj_in_lod = cmds.listRelatives(lod0, f=True)
#filter all auxiliary geometry such as ramp, bsp, etc
        obj_in_lod = filter_auxiliary_obejcts(obj_in_lod)
#find all unique objects in the lod0 and set the polycount
        unique_objects = {}
        for n in obj_in_lod: unique_objects[n] = cmds.polyEvaluate(n)["triangle"]
        settings = vl_read_json(dir, "objectsPolyCount.json")

#for each setting in dictionary:
        for l in settings:
#check if this lod exist in a group
            lod = cmds.ls(x + "|" + l, l=True)
            if not lod:
                continue
#check each uniqe object for this group

            for obj in unique_objects:
                obj_instance = ("%s%s%s") % (lod[0], "|", obj.split("|")[-1])
                initial_polycount = unique_objects[obj]
                max_polycount = int(math.ceil(settings[l] * initial_polycount))
                obj_polycount = cmds.polyEvaluate(obj_instance)["triangle"]

                if obj_polycount > max_polycount:
                    return_list.append(
                        ["%s Out of range with  %i tris > max polycount: %i" % (obj_instance, obj_polycount, max_polycount), obj_instance])

    return return_list



