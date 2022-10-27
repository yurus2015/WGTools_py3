import maya.cmds as cmds
from validator.utils.validator_API import *


def main():
    # find double __ in all transforms
    object_list = vl_listAllTransforms()
    return_list = []

    # find all shapes which dont have "_" before Shape
    mesh_list = cmds.ls(type="mesh", l=1)
    for i in mesh_list:
        mesh_name = i.split("|")[-1]
        if mesh_name.find("_Shape") == -1:
            tmp = [i, i]
            return_list.append(tmp)

    for x in object_list:
        check = x.find("__")
        if check != -1:
            tmp = [x, x]
            return_list.append(tmp)

    list_poly_meshes = cmds.ls(type='mesh', l=True)
    for x in list_poly_meshes:
        check = x.find("__")
        if check != -1:
            tmp = [x, x]
            return_list.append(tmp)

    for x in object_list:
        shape = cmds.listRelatives(x)
        full_shape = cmds.listRelatives(x, f=True)
        error = False
        for x in range(len(shape)):
            check = shape[x].count("_")
            if check > 2:
                tmp = [full_shape[x], full_shape[x]]
                return_list.append(tmp)

    all_names = []
    for x in listAllMat():
        all_names.append(x)

    for x in vl_listAllTransforms():
        all_names.append(x)

    for x in vl_listAllGroups():
        all_names.append(x)

    for x in all_names:
        for y in x:
            ord(y)
            if ord(y) < 48 or ord(y) > 124:
                tmp = [x, x]
                return_list.append(tmp)

    return return_list
