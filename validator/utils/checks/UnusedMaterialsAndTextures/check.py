
import maya.cmds as cmds
import maya.mel as mel
from validator2019.utils.validator_API import *
checkId = 49
checkLabel = "1.12 Check for unused materials and textures"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    objList = vl_listAllTransforms()
    returnList = []
    shapeArray = cmds.ls(type='mesh', dag=1, l = True)

    if shapeArray:
        #unused materials
        shadingGroupList = cmds.ls(type="shadingEngine", l=1, fl=1)
        shadingGroupList.remove("initialParticleSE")
        shadingGroupList.remove("initialShadingGroup")
        try:
            shadingGroupList.remove("lambert1SG")
        except:
            pass

        for i in shadingGroupList:
            itsConnections =  cmds.listConnections(i + ".dagSetMembers")
            if itsConnections == None:
                itsMaterial = cmds.listConnections(i + ".surfaceShader")
                if itsMaterial:
                    tmp = []
                    tmp.append(itsMaterial[0])
                    tmp.append(itsMaterial[0])
                    returnList.append(tmp)


        #unused textures
        errorMessage = "\nUnused textures:"

        textArray = cmds.ls(type="file")
        unusedFileNodes = []

        for i in textArray:
            outAlpha = cmds.listConnections(i+".outAlpha", d=1,p=1)
            outColor = cmds.listConnections(i+".outColor", d=1, p=1)
            outTransparency = cmds.listConnections(i+".outTransparency", d=1, p=1)

            if not outAlpha and not outColor and not outTransparency:
                unusedFileNodes.append(i)

        for i in unusedFileNodes:
            tmp = []
            tmp.append(i)
            tmp.append(i)
            returnList.append(tmp)


    return  returnList


