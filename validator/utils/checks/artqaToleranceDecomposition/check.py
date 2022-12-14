import maya.cmds as cmds

checkLabel = "Check tolerance decomposition node"
NODE = 'hkdConvexDecompositionAction'
TOLERANCE = 0.05


def main():
    return_list = []

    decomps = cmds.ls(type=NODE)
    for node in decomps:
        if cmds.getAttr(node + ".tolerance") < TOLERANCE:
            tmp = []
            tmp.append("Value tolerance less than " + str(TOLERANCE))
            tmp.append(node)
            return_list.append(tmp)

    return return_list
