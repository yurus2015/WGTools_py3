import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import re


def main():
    return_list = []
    obj_list = cmds.ls(type='mesh', l=True)
    obj_list = cmds.filterExpand(obj_list, sm=12, fp=1)

    tracks_list = cmds.ls('track_*', type='mesh', l=True)

    # Remove objects in the tracks_list from the obj_list
    obj_list = list(set(obj_list) - set(tracks_list))

    # Delete duplicates from list
    obj_list = list(set(obj_list))

    # Remove any objects from the obj_list that NOT have "lod0" or "lod1" in their name
    obj_list = [obj for obj in obj_list if not re.search(r"lod[^0|1].", obj)]

    for obj in obj_list:
        selection_list = OpenMaya.MSelectionList()
        selection_list.add(obj)
        OpenMaya.MGlobal.setActiveSelectionList(selection_list)

        dag_path = OpenMaya.MDagPath()

        selection_list.getDagPath(0, dag_path)

        fn_mesh = OpenMaya.MFnMesh(dag_path)

        # Arrays to store the U and V UV coordinates
        u_array = OpenMaya.MFloatArray()
        v_array = OpenMaya.MFloatArray()

        fn_mesh.getUVs(u_array, v_array)

        max_u = max(u_array)
        min_u = min(u_array)
        max_v = max(v_array)
        min_v = min(v_array)
        if max_u > 1.0 or min_u < 0.0 or max_v > 1.0 or min_v < 0.0:
            tmp = [obj + ' - UV coordinates out of border', obj]
            return_list.append(tmp)

    # Remove any objects from the tracks_list that NOT have "lod0" in their name
    tracks_list = [obj for obj in tracks_list if not re.search(r"lod[^0].", obj)]
    if tracks_list:
        for i in tracks_list:
            selection_list = OpenMaya.MSelectionList()
            selection_list.add(i)
            OpenMaya.MGlobal.setActiveSelectionList(selection_list)

            dag_path = OpenMaya.MDagPath()

            selection_list.getDagPath(0, dag_path)

            fn_mesh = OpenMaya.MFnMesh(dag_path)
            u_array = OpenMaya.MFloatArray()
            v_array = OpenMaya.MFloatArray()

            fn_mesh.getUVs(u_array, v_array)

            max_u = max(u_array)
            min_u = min(u_array)
            if max_u > 1.0 or min_u < 0.0:
                tmp = [i + ' - UV coordinates out of border', i]
                return_list.append(tmp)

        OpenMaya.MGlobal.clearSelectionList()

    return return_list
