from maya.OpenMaya import *
import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 707
checkLabel = "Fix locked normals"


def main(*args):

    all_meshes = cmds.ls(type="mesh", l = True)
    sel_list = MSelectionList()

    if args:
        for i in args:
        	sel_list.add(i)

    dag_path = MDagPath()
    for x in range(sel_list.length()):
        sel_list.getDagPath(x, dag_path)
        mesh = MFnMesh(dag_path)
        array = MIntArray(mesh.numNormals(), 0)
        for i in range(mesh.numNormals()):
            array.set(i, i)
        mesh.unlockVertexNormals(array)

    return []





