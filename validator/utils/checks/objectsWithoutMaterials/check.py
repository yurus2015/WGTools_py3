import maya.cmds as cmds
import maya.mel as mel
from validator.utils.validator_API import *

checkId = 35
checkLabel = "3.2 Check objects/faces without materials"


def main_old():
    print('<< ' + checkLabel.upper() + ' >>')
    objMatList = vl_objMaterialsData()
    returnList = []
    if len(objMatList) != 0:
        for x in objMatList:

            if x[0] == 0:
                tmp = []
                tmp.append(x[1])
                tmp.append(x[1])
                returnList.append(tmp)

            if x[0] == 1 and x[3] == "noMaterial!":
                tmp = []
                tmp.append(x[1])
                tmp.append(x[1])
                returnList.append(tmp)

    return returnList


def main():
    returnList = []
    all_meshes = cmds.ls(type="mesh", l=1, fl=1)
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
            material = cmds.listConnections(shader + ".surfaceShader")
            if material:
                cmds.hyperShade(o=shader)
                shading_faces = cmds.ls(cmds.polyListComponentConversion(tf=1), l=1, fl=1)
                nonshading_faces = list(set(nonshading_faces) - set(shading_faces))
                cmds.select(d=1)

        if len(nonshading_faces):
            tmp = []
            transform = cmds.listRelatives(mesh, p=1, type='transform', f=1)[0]
            tmp.append(transform)

            if len(nonshading_faces) == len(mesh_faces):
                nonshading_faces = transform
            tmp.append(nonshading_faces)
            returnList.append(tmp)

    return returnList
