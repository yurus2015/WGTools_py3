import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 9

checkLabel = "8.3 Check faces without of material"


def main_old():
    #

    returnList = []
    dagIter = OpenMaya.MItDag(OpenMaya.MItDag.kBreadthFirst, OpenMaya.MFn.kInvalid)
    while not dagIter.isDone():
        dagPath = OpenMaya.MDagPath()
        stat = dagIter.getPath(dagPath)

        if not stat:
            dagNode = OpenMaya.MFnDagNode(dagPath)
            if dagNode.isIntermediateObject() == False \
                    and dagPath.hasFn(OpenMaya.MFn.kMesh) == True \
                    and dagPath.hasFn(OpenMaya.MFn.kTransform) == False:

                # Horrible Dirty Shit for havok preset
                if "havok" in cmds.file(q=1, sn=1):
                    if "havok" not in dagPath.fullPathName():
                        next(dagIter)

                array_shaded_polygons = []
                fnMesh = OpenMaya.MFnMesh(dagPath)
                instanceNumber = dagPath.instanceNumber()
                sets = OpenMaya.MObjectArray()
                comps = OpenMaya.MObjectArray()

                fnMesh.getConnectedSetsAndMembers(instanceNumber, sets, comps, True)
                for i in range(sets.length()):
                    set = OpenMaya.MObject(sets[i])
                    comp = OpenMaya.MObject(comps[i])
                    fnset = OpenMaya.MFnSet(set)
                    dnset = OpenMaya.MFnDependencyNode(set)
                    ssatr = OpenMaya.MObject(dnset.attribute("surfaceShader"))
                    ssplug = OpenMaya.MPlug(set, ssatr)
                    srcplugarray = OpenMaya.MPlugArray()
                    ssplug.connectedTo(srcplugarray, True, False)
                    if (srcplugarray.length() == 0):
                        polyIter = OpenMaya.MItMeshPolygon(dagPath, comp);
                        while not polyIter.isDone():
                            objectTransform = cmds.listRelatives(dagNode.fullPathName(), p=True, f=True)
                            tmp = []
                            tmp.append(str(objectTransform[0]) + ".f[" + str(polyIter.index()) + "]")
                            tmp.append(str(objectTransform[0]) + ".f[" + str(polyIter.index()) + "]")
                            returnList.append(tmp)
                            next(polyIter)

        next(dagIter)
    return returnList


def main():
    returnList = []
    all_meshes = cmds.ls(type="mesh", l=1, fl=1)
    # allFaces = cmds.ls(cmds.polyListComponentConversion(allMesh, tf=1), l=1, fl=1)
    shader_engine = cmds.ls(type="shadingEngine", l=1, fl=1)

    for mesh in all_meshes:
        mesh_faces = cmds.ls(cmds.polyListComponentConversion(mesh, tf=1), l=1, fl=1)
        nonshading_faces = mesh_faces
        history_nodes = cmds.listHistory(mesh, f=1, ag=1)
        shader_engine = []
        for nodes in history_nodes:
            if cmds.nodeType(nodes) == "shadingEngine":
                shader_engine.append(nodes)
        for shader in shader_engine:
            # if shader == "initialParticleSE":
            # 	continue

            material = cmds.listConnections(shader + ".surfaceShader")
            if material:
                cmds.hyperShade(o=shader)
                shading_faces = cmds.ls(cmds.polyListComponentConversion(tf=1), l=1, fl=1)
                nonshading_faces = list(set(nonshading_faces) - set(shading_faces))
                cmds.select(d=1)

        if len(nonshading_faces):
            # for i in allFaces:
            tmp = []
            transform = cmds.listRelatives(mesh, p=1, type='transform', f=1)[0]
            tmp.append(transform)
            print('NON ', len(nonshading_faces))
            print('MESH ', len(mesh_faces))
            if len(nonshading_faces) == len(mesh_faces):
                nonshading_faces = transform
            tmp.append(nonshading_faces)
            returnList.append(tmp)

    return returnList
