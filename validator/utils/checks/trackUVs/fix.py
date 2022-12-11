import maya.cmds as cmds
import maya.OpenMaya as OpenMaya


def main(*args):
    print('arguments: {}'.format(args[0]))
    if not args:
        return None

    tracks = args
    if isinstance(args[0], list):
        tracks = args[0]
    for track in tracks:
        print('Track : ' + track)
        selection_list = OpenMaya.MSelectionList()
        selection_list.clear()
        selection_list.add(track)
        dag_path = OpenMaya.MDagPath()
        selection_list.getDagPath(0, dag_path)
        fn_mesh = OpenMaya.MFnMesh(dag_path)
        u_array = OpenMaya.MFloatArray()
        v_array = OpenMaya.MFloatArray()
        fn_mesh.getUVs(u_array, v_array)

        min_v = min(v_array)
        max_v = max(v_array)

        max_border = 0
        min_border = 0

        if abs(int(abs(max_v)) - abs(max_v)) < 0.5:
            max_border = int(max_v)
        else:
            max_border = int(max_v) + (max_v / abs(max_v))

        if abs(int(abs(min_v)) - abs(min_v)) < 0.5:
            min_border = int(min_v)
        else:
            min_border = int(min_v) + (min_v / abs(min_v))

        scale_approx = max_border - min_border

        # Add check division by zero
        if scale_approx == 0 or (max_v - min_v) == 0:
            return None
        scale_factor = scale_approx / (max_v - min_v)
        cmds.polyEditUV(track + ".map[*]", pu=0, pv=0, su=1, sv=scale_factor)
