import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 21

checkLabel = "1.18 Check lambert1"


def main_old():
    objMatData = vl_objMaterialsData()
    returnList = []

    for x in range(len(objMatData)):
        if objMatData[x][0] != 0:
            if objMatData[x][0] == 1 and objMatData[x][3] == "noMaterial!":
                pass

            elif len(objMatData[x]) < 5:
                check = objMatData[x][3].find('lambert1')
                if check != -1:
                    tmp = []
                    tmp.append(objMatData[x][1])
                    tmp.append(objMatData[x][1])
                    returnList.append(tmp)

            else:
                for y in range(3, len(objMatData[x]) - 1):
                    check = objMatData[x][y].find('lambert1')
                    if check != -1:
                        tmp = []
                        tmp.append(objMatData[x][1])
                        tmp.append(objMatData[x][1])
                        returnList.append(tmp)

    return returnList


def main():
    returnList = []
    # allMesh = cmds.ls(type="mesh", l=1, fl=1)
    # allFaces = cmds.ls(cmds.polyListComponentConversion(allMesh, tf=1), l=1, fl=1)
    # allShading = cmds.ls(type="shadingEngine", l=1, fl=1)

    lambert_shading = cmds.ls("initialShadingGroup")[0]
    cmds.hyperShade(o=lambert_shading)
    lambert_faces = cmds.ls(sl=1, l=1)
    cmds.select(d=1)

    if lambert_faces:
        tmp = []
        tmp.append('Select faces with lambert1')
        tmp.append(lambert_faces)
        returnList.append(tmp)
    # shaderFaces = cmds.ls(cmds.polyListComponentConversion(tf=1), l=1)

    # for shader in allShading:
    # 	if shader == "initialParticleSE": continue

    # 	if shader == "initialShadingGroup":
    # 		print 'Lambert'

    # 	ruf_temp = cmds.listConnections(shader + ".surfaceShader")
    # 	if ruf_temp:

    # 		cmds.hyperShade(o=shader)
    # 		shaderFaces = cmds.ls(cmds.polyListComponentConversion(tf=1), l=1, fl=1)
    # 		allFaces = list(set(allFaces) - set(shaderFaces))

    # if len(allFaces):
    # 	#for i in allFaces:
    # 	tmp = []
    # 	tmp.append('Select faces without shader: ')
    # 	tmp.append(allFaces)
    # 	returnList.append(tmp)

    return returnList
