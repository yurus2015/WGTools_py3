import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

checkId = 109
checkLabel = "Check shape count of each object"


def main_2():
    returnList = []

    itDag = OpenMaya.MItDag(OpenMaya.MItDag.kDepthFirst, OpenMaya.MFn.kTransform)
    while not itDag.isDone():

        DP = OpenMaya.MDagPath()
        itDag.getPath(DP)
        DagNode = OpenMaya.MFnDagNode(DP)
        childTypes = []
        if DP.childCount() > 1:
            for idx in range(DP.childCount()):
                child = DagNode.child(idx)
                if child.apiTypeStr() == "kMesh":
                    childTypes.append(child.apiType)

        if len(childTypes) > 1:
            tmp = []
            tmp.append(str(DagNode.fullPathName()) + " has " + str(len(childTypes)) + " shape nodes.")
            tmp.append(DagNode.fullPathName())
            returnList.append(tmp)

        next(itDag)

    return returnList


def main():
    returnList = []
    mesh_list = cmds.filterExpand(cmds.ls(tr=1), sm=12)
    for i in mesh_list:
        shapes = cmds.listRelatives(i, s=1, f=1)
        if len(shapes) > 1:
            tmp = []
            tmp.append(i + ' has ' + str(len(shapes)) + ' shape nodes')
            tmp.append(i)
            returnList.append(tmp)

    return returnList
