import maya.cmds as cmds
# import maya.api.OpenMaya as OpenMaya
import re
from validator.utils.checks.wheelsPivot.utilites import *


def replacer_pivot(wheel):
    original_wheel = re.sub('lod\d', 'lod0', wheel)
    if cmds.objExists(original_wheel):
        pivot = cmds.xform(original_wheel, q=True, ws=True, piv=True)
        cmds.xform(wheel, ws=True, piv=pivot[0:3])


def main(*args):
    input_list = args
    # All scene objects
    all_objects = cmds.ls(type='transform', l=True)

    # All invalid wheels in lod0
    # wheels = [obj for obj in all_objects if re.search(r"lod0.*(wd_|w_)", obj)]
    wheels = list(input_list)

    # All wheels in other lods
    lods_wheels = [obj for obj in all_objects if re.search(r"lod[^0].*(wd_|w_)", obj)]

    for w in wheels:
        if validation_bounding_box(w):
            cmds.xform(w, cp=1)
        else:
            centroid = mesh_baricentric(w)  # convert to list?
            if cmds.currentUnit(q=True, linear=True) == 'm':
                centroid = [item / 100 for item in centroid]
            cmds.xform(w, ws=1, rp=centroid)
            cmds.xform(w, ws=1, sp=centroid)

    for w in lods_wheels:
        replacer_pivot(w)

    return []
