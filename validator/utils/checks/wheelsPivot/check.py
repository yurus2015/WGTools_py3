import maya.cmds as cmds
import re
from validator.utils.checks.wheelsPivot.utilites import *


def main():
    return_list = []
    # All scene objects
    all_objects = cmds.ls(type='transform', l=True)

    # All wheels in lod0
    wheels = [obj for obj in all_objects if re.search(r"lod0.*(wd_|w_)", obj)]

    # All wheels in other lods
    lods_wheels = [obj for obj in all_objects if re.search(r"lod[^0].*(wd_|w_)", obj)]

    for w in wheels:
        if validation_bounding_box(w):
            continue
        else:
            centroid = mesh_baricentric(w)  # convert to list?
            if cmds.currentUnit(q=True, linear=True) == 'cm':
                centroid = [item / 100 for item in centroid]

            pivot = cmds.xform(w, q=1, ws=1, rp=1)
            if ("%.4f" % pivot[0]) != ("%.4f" % centroid[0]) or ("%.4f" % pivot[1]) != (
                    "%.4f" % centroid[1]) or ("%.4f" % pivot[2]) != ("%.4f" % centroid[2]):
                tmp = [w + " - the pivot is not in center of wheel", w]
                return_list.append(tmp)

    return return_list
