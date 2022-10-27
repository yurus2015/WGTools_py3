import maya.cmds as cmds
from maya.mel import eval as meval

checkLabel = "Check correct smooth group for map borders"


def remove_list(from_list, this_list):
    result_list = [n for n in from_list if n not in this_list]
    result_list = list(result_list)
    return result_list


def intersection_list(one_list, second_list):
    intersect = set(one_list).intersection(set(second_list))
    intersect = list(intersect)
    return intersect


def remove_duplicate_list(current_list):
    result_list = list(set(current_list))
    return result_list


def load_plugin():
    try:
        cmds.loadPlugin('techartAPI')
    except OSError:
        print("Can`t load techartAPI plugin")


def main():
    load_plugin()
    mesh_list = cmds.ls(type="mesh", l=1)
    poly_obj_list = []
    if mesh_list:
        poly_obj_list = cmds.listRelatives(mesh_list, p=1, f=1)
        poly_obj_list = remove_duplicate_list(poly_obj_list)

    return_list = []
    if poly_obj_list:

        for obj in poly_obj_list:
            cmds.select(obj)

            # fix two uv-sets bag
            uv_sets = cmds.polyUVSet(obj, query=True, allUVSets=True)  # get all uvSets
            if uv_sets:
                if len(uv_sets) > 1:
                    cmds.polyUVSet(obj, currentUVSet=True, uvSet='map1')

            # fix none polygons in current uv-set
            uvs = cmds.ls(obj + '.map[*]', fl=True)
            uv_set_faces = cmds.polyListComponentConversion(uvs, fuv=True, tf=True)
            uv_set_faces = cmds.ls(uv_set_faces, fl=1)
            real_faces = cmds.ls(obj + '.f[*]', fl=True)

            if len(uv_set_faces) != len(real_faces):
                continue

            # border edges
            border_edges = []
            # borderEdges = meval('selectUVBorderEdge -uve')

            try:
                border_edges = meval('selectUVBorderEdge -uve')
            except ValueError:
                return return_list

            cmds.polySelectConstraint(m=3, t=0x8000, sm=2)  # to get soft edges
            soft_edges = cmds.ls(sl=True, fl=1)
            cmds.polySelectConstraint(sm=0)
            cmds.polySelectConstraint(m=0)
            # cmds.polySelectConstraint(disable =1)

            cmds.polySelectConstraint(m=3, t=0x8000, sm=1, w=2)  # to get hard edges
            hard_edges = cmds.ls(sl=True, fl=1)

            cmds.polySelectConstraint(sm=0, w=0)
            cmds.polySelectConstraint(m=0)
            # cmds.polySelectConstraint(disable =1)
            if border_edges:
                must_hard = intersection_list(soft_edges, border_edges)

            if hard_edges:
                must_split = remove_list(hard_edges, border_edges)
                if must_split:
                    tmp = [obj + " - hard edges should be split in UV (not always)", must_split]
                    return_list.append(tmp)
    cmds.select(d=1)
    return return_list
