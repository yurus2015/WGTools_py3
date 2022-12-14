import maya.cmds as cmds

from validator.utils.validator_API import *

checkId = 215

checkLabel = "GB Check unshaded faces"


def main():
    returnList = []
    allMesh = cmds.ls(type="mesh", l=1, fl=1)
    allFaces = cmds.ls(cmds.polyListComponentConversion(allMesh, tf=1), l=1, fl=1)
    allShading = cmds.ls(type="shadingEngine", l=1, fl=1)

    for shader in allShading:
        if shader == "initialParticleSE": continue

        if shader == "initialShadingGroup":
            print('Lambert')

        ruf_temp = cmds.listConnections(shader + ".surfaceShader")
        if ruf_temp:
            cmds.hyperShade(o=shader)
            shaderFaces = cmds.ls(cmds.polyListComponentConversion(tf=1), l=1, fl=1)
            allFaces = list(set(allFaces) - set(shaderFaces))

    if len(allFaces):
        # for i in allFaces:
        tmp = []
        tmp.append('Select faces without shader: ')
        tmp.append(allFaces)
        returnList.append(tmp)

    return returnList
