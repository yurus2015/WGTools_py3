import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

checkId = 107
checkLabel = "4.23 Check polygons with zero UV Map Area"


def zeroUVMapPolygonsCheck():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []

    meshList = cmds.ls(type="mesh", l=1)
    polyObjList = []
    if meshList:
        polyObjList = cmds.listRelatives(meshList, p=1, f=1)

    areaTolerance = 0.00000001

    for i in polyObjList:
        selectionList = OpenMaya.MSelectionList()
        selectionList.clear()
        selectionList.add(i)

        # get dag and mobject
        DagPath = OpenMaya.MDagPath()
        mObj = OpenMaya.MObject()
        selectionList.getDagPath(0, DagPath, mObj)

        # iterator component
        component = OpenMaya.MObject()

        # iterate
        geomIter = OpenMaya.MItMeshPolygon(DagPath, component)

        # create double pointer
        number = OpenMaya.MScriptUtil()
        number.createFromDouble(0.0)
        numPointer = number.asDoublePtr()

        while not geomIter.isDone():

            geomIter.getUVArea(numPointer)

            resultArea = OpenMaya.MScriptUtil(numPointer).asDouble()

            if geomIter.hasUVs():
                if "lod3" not in i and "lod4" not in i:
                    if resultArea <= areaTolerance:
                        # print resultArea, areaTolerance
                        # get face id
                        faceId = geomIter.index()
                        tmp = []
                        tmp.append(i + ".f[" + str(faceId) + "]")
                        tmp.append(i + ".f[" + str(faceId) + "]")
                        returnList.append(tmp)

            else:
                faceId = geomIter.index()
                tmp = []
                tmp.append(i + ".f[" + str(faceId) + "]")
                tmp.append(i + ".f[" + str(faceId) + "]")
                returnList.append(tmp)

            next(geomIter)

    return returnList
