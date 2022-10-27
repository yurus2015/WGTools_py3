import maya.cmds as cmds
import maya.OpenMaya as OpenMaya


def main_2():
    return_list = []

    it_dag = OpenMaya.MItDag(OpenMaya.MItDag.kDepthFirst, OpenMaya.MFn.kTransform)
    while not it_dag.isDone():

        dp = OpenMaya.MDagPath()
        it_dag.getPath(dp)
        dag_node = OpenMaya.MFnDagNode(dp)
        child_types = []
        if dp.childCount() > 1:
            for idx in range(dp.childCount()):
                child = dag_node.child(idx)
                if child.apiTypeStr() == "kMesh":
                    child_types.append(child.apiType)

        if len(child_types) > 1:
            tmp = [str(dag_node.fullPathName()) + " has " + str(len(child_types)) + " shape nodes.",
                   dag_node.fullPathName()]
            return_list.append(tmp)

        next(it_dag)

    return return_list


def main():
    return_list = []
    mesh_list = cmds.filterExpand(cmds.ls(tr=1), sm=12)
    if mesh_list:
        for i in mesh_list:
            shapes = cmds.listRelatives(i, s=1, f=1)
            if len(shapes) > 1:
                tmp = [i + ' has ' + str(len(shapes)) + ' shape nodes', i]
                return_list.append(tmp)

    return return_list
