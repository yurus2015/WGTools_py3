import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

checkId = 106
checkLabel = "Check polygons with zero Area"


def main():
    returnList = []

    meshList = cmds.ls(type="mesh", l=1)
    polyObjList = []
    if meshList:
        polyObjList = cmds.listRelatives(meshList, p=1, f=1)

    areaTolerance = 0.0

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

            geomIter.getArea(numPointer, OpenMaya.MSpace.kWorld)

            resultArea = OpenMaya.MScriptUtil(numPointer).asDouble()
            if resultArea <= areaTolerance:
                # get face id
                faceId = geomIter.index()
                tmp = []
                tmp.append(i + ".f[" + str(faceId) + "]")
                tmp.append(i + ".f[" + str(faceId) + "]")
                returnList.append(tmp)

            next(geomIter)

    return returnList
