import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from validator.utils.validator_API import *

checkId = 54
checkLabel = "1.6 Check non-stretched UV sets"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    objMatList = vl_objMaterialsData()

    returnList = []

    emptySpacePercentage = 0.4

    fileNodeList = cmds.ls(type="file", l=1)
    for i in fileNodeList:
        size = cmds.getAttr(i + ".outSize")[0]

        if not size[0] == 0:
            proportion = size[0] / size[1]
            if proportion > 1:
                # outAlpha = []
                # outColor = []
                # outTransparency = []
                outAlpha = cmds.listConnections(i + ".outAlpha", d=1, p=0)
                outColor = cmds.listConnections(i + ".outColor", d=1, p=0)
                outTransparency = cmds.listConnections(i + ".outTransparency", d=1, p=0)
                # print outAlpha, outColor, outTransparency

                if outColor or outAlpha or outTransparency:
                    fileNodeConnections = cmds.listConnections(i)
                    for j in fileNodeConnections:
                        if cmds.nodeType(j) == "lambert" or cmds.nodeType(j) == "blinn" or cmds.nodeType(
                                j) == "phong":  # or other material types

                            # cmds.hyperShade(o = j)
                            # objByMaterial = cmds.ls(sl=1, l=1)

                            # ----------------------------------
                            objByMaterial = []
                            for x in objMatList:
                                if j in x:
                                    objByMaterial.append(x[1])
                            # ----------------------------------

                            if len(objByMaterial) > 0:
                                for obj in objByMaterial:
                                    objName = None
                                    if obj.find("Shape") != -1:
                                        objName = cmds.listRelatives(obj, p=1, f=1)[0]
                                    elif obj.find(".f["):
                                        objName = obj.split(".")[0]

                                    util = OpenMaya.MScriptUtil()
                                    selectionList = OpenMaya.MSelectionList()
                                    selectionList.add(objName)
                                    OpenMaya.MGlobal.setActiveSelectionList(selectionList)

                                    DagPath = OpenMaya.MDagPath()
                                    selectionList.getDagPath(0, DagPath)

                                    component = OpenMaya.MObject()

                                    fnMesh = OpenMaya.MFnMesh(DagPath)
                                    uArray = OpenMaya.MFloatArray()
                                    vArray = OpenMaya.MFloatArray()

                                    fnMesh.getUVs(uArray, vArray)

                                    if len(vArray) > 0:
                                        minV = vArray[0]
                                        maxV = vArray[0]

                                        minU = uArray[0]
                                        maxU = uArray[0]

                                        for i in range(1, len(vArray)):
                                            if vArray[i] < minV:
                                                minV = vArray[i]
                                            if vArray[i] > maxV:
                                                maxV = vArray[i]

                                            if uArray[i] < minU:
                                                minU = uArray[i]
                                            if uArray[i] > maxU:
                                                maxU = uArray[i]

                                        diffV = 1 - (maxV - minV)
                                        diffU = 1 - (maxU - minU)

                                        if diffV > emptySpacePercentage:
                                            tmp = []
                                            tmp.append(objName)
                                            tmp.append(objName)
                                            returnList.append(tmp)

    OpenMaya.MGlobal.clearSelectionList()

    return returnList
