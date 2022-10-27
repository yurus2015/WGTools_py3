from maya.OpenMaya import *
import maya.cmds as cmds

checkId = 708
checkLabel = "9. Check locked vertex normals"


def main():
    all_meshes = cmds.ls(type="mesh", l=True)
    sel_list = MSelectionList()
    for x in all_meshes:
        sel_list.add(x)

    return_list = []

    dag_path = MDagPath()
    for x in range(sel_list.length()):
        sel_list.getDagPath(x, dag_path)

        # Horrible Dirty Shit for havok preset
        if "havok" in cmds.file(q=1, sn=1):
            if "havok" not in dag_path.fullPathName().split("|")[1]:
                continue

        mesh = MFnMesh(dag_path)
        for n in range(mesh.numNormals()):
            if mesh.isNormalLocked(n):

                if cmds.nodeType(dag_path.fullPathName()) == "mesh":
                    transformObj = cmds.listRelatives(dag_path.fullPathName(), p=1, type="transform", f=1)[0]
                    return_list.append([transformObj, transformObj])
                else:
                    return_list.append([dag_path.fullPathName(), dag_path.fullPathName()])
                break

    return return_list
