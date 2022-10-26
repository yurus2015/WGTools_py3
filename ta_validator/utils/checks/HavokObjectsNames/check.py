import maya.cmds as cmds
from validator2019.utils.validator_API import *

import json
import os
dir = os.path.dirname(__file__)


checkId = 7155
checkLabel = "Check havok objects name"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    return_list = []
    scene_name_havok = vl_scene_name()
    scene_name = scene_name_havok[:-6]
    if scene_name_havok[-6:] != "_havok":
        return_list.append(['wrong scene name - "_havok missing: "%s' %(scene_name), []])

    reg_exp_names = []
    reg_exp_names.append(re.compile(("%s%s") % (scene_name, "\\Z")))
    reg_exp_names.append(re.compile(("%s%s") % (scene_name, "_havok\\Z")))
    reg_exp_names.append(re.compile("^(n_|d_)(wood|stone|metal)\\Z"))
    reg_exp_names.append(re.compile("work"))


    list_havok_groups = set()
    for x in cmds.ls(assemblies=True):
        rel = cmds.listRelatives(x, shapes = True)
        if rel == None:
            rel = []

        rel = [cmds.objectType(t) for t in rel]
        if not rel:
            list_havok_groups.add(x)
        else:
            if "hkNodeRigidBody" and "hkNodeShape" in rel:
                list_havok_groups.add(x)


    for y in list_havok_groups:
        find = False
        for x in reg_exp_names:
            if x.search(y):
                find = True
        if not find:
            return_list.append(["wrong group name %s" %(y), y])

    return return_list

