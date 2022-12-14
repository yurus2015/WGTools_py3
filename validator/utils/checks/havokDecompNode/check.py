import maya.cmds as cmds

checkLabel = "Find ConvexDecomposition Nodes"


def main():
    return_list = []

    decomp_node = cmds.ls(type='hkdConvexDecompositionAction')
    if decomp_node:
        for node in decomp_node:
            tolerance = cmds.getAttr(node + '.tolerance')
            tmp = []
            tmp.append(node + ': ' + str(tolerance) + '(the tolerance value')
            tmp.append(node)
            return_list.append(tmp)

    return return_list
