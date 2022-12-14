import maya.cmds as cmds

checkLabel = "Check havok decomposition node"
NODE = 'hkdConvexDecompositionAction'


def main():
    #

    return_list = []

    decomps = cmds.ls(type=NODE)
    for node in decomps:
        tmp = []
        tmp.append("Scene contains Decomposition Node")
        tmp.append(node)
        return_list.append(tmp)

    return return_list
