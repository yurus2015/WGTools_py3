import maya.cmds as cmds


def main():
    return_list = []
    all_meshes = cmds.ls(type="mesh", l=1, fl=1)
    if all_meshes:
        for i in all_meshes:
            parent = cmds.listRelatives(i, p=1, f=1)[0]
            vmn = cmds.getAttr(i + ".vertexNormalMethod")
            if not vmn == 3:
                tmp = [parent, parent]
                return_list.append(tmp)

    return return_list
