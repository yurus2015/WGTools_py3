import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

checkId = 105
checkLabel = "Check non-triangulated objects"


def main():
    returnList = []

    meshList = cmds.ls(type="mesh", l=1)
    polyObjList = []
    if meshList:
        polyObjList = cmds.listRelatives(meshList, p=1, f=1)

    for i in polyObjList:
        selectionList = OpenMaya.MSelectionList()
        selectionList.clear()
        selectionList.add(i)

        # get dag and mobject
        DagPath = OpenMaya.MDagPath()
        mObj = OpenMaya.MObject()
        selectionList.getDagPath(0, DagPath, mObj)

        component = OpenMaya.MObject()

        # iterate
        geomIter = OpenMaya.MItMeshPolygon(DagPath, component)
        numTri = OpenMaya.MScriptUtil()
        numTri.createFromInt(0)
        numTriPtr = numTri.asIntPtr()

        triangleCount = 0

        while not geomIter.isDone():

            geomIter.numTriangles(numTriPtr)
            realNumTri = OpenMaya.MScriptUtil(numTriPtr).asInt()
            if realNumTri != 1:
                triangleCount = triangleCount + 1
            # get face id
            # faceId = geomIter.index()
            # tmp = []
            # tmp.append(i + ".f[" + str(faceId) + "]")
            # tmp.append(i + ".f[" + str(faceId) + "]")
            # returnList.append(tmp)
            next(geomIter)

        if triangleCount:
            tmp = []
            tmp.append(i)
            tmp.append(i)
            returnList.append(tmp)

    return returnList
