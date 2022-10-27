import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
from validator.utils.validator_API import *

checkId = 41
checkLabel = "3.4 Check centering of the tank"


def traverseMesh():
    storedData = []
    dagIter = OpenMaya.MItDag(OpenMaya.MItDag.kBreadthFirst, OpenMaya.MFn.kInvalid)
    while not dagIter.isDone():
        dagPath = OpenMaya.MDagPath()
        stat = dagIter.getPath(dagPath)
        if not stat:
            dagNode = OpenMaya.MFnDagNode(dagPath)
            if dagNode.isIntermediateObject() == False \
                    and dagPath.hasFn(OpenMaya.MFn.kMesh) == True \
                    and dagPath.hasFn(OpenMaya.MFn.kTransform) == False:
                storedData.append(dagPath)
        next(dagIter)
    return storedData


def findDifference():
    lod0Tracks = []
    storedData = traverseMesh()
    if len(storedData) > 0:
        for x in storedData:
            if x.fullPathName().find("lod0") != -1 and x.fullPathName().find("track") != -1:
                lod0Tracks.append(x);
    if len(lod0Tracks) > 1:
        track_bbox = cmds.polyEvaluate(lod0Tracks[0].fullPathName(), lod0Tracks[1].fullPathName(), b=True)
        # select = OpenMaya.MSelectionList()

        lowestPoints = []

        def getLowestVertices(track):
            dagNode = OpenMaya.MFnDagNode(track)
            bbox = dagNode.boundingBox()
            ground = bbox.min()
            iterVertexes = OpenMaya.MItMeshVertex(track)

            while not iterVertexes.isDone():
                position = OpenMaya.MPoint()
                position = iterVertexes.position(OpenMaya.MSpace.kWorld)
                if round(position.y, 3) >= round(ground.y, 3) - 0.7 and round(position.y, 3) <= round(ground.y,
                                                                                                      3) + 0.7:
                    lowestPoints.append(position)
                    # select.add(track, iterVertexes.currentItem())
                next(iterVertexes)

        # getLowestVertices(lod0Tracks[0])
        # getLowestVertices(lod0Tracks[1])

        for track in lod0Tracks:
            getLowestVertices(track)

        cBbox = OpenMaya.MBoundingBox()
        for x in lowestPoints:
            cBbox.expand(x)
        # OpenMaya.MGlobal.setActiveSelectionList(select)
        return [round(cBbox.center().x, 3), round(cBbox.center().y, 3), round(cBbox.center().z, 3)]

    else:
        return [0, 0, 0]


def main():
    returnList = []

    sceneName = cmds.file(q=1, sn=1, shn=1).split(".")[0]
    if sceneName:
        if sceneName.find("crash") == -1:

            centerTank = findDifference()
            if abs(round(centerTank[0] / 100, 3)) > 0.001 or abs(round(centerTank[2] / 100, 3)) > 0.001:
                errorMessage = "tank not centered. X: " + str(centerTank[0] / 100) + "; Z: " + str(centerTank[2] / 100)
                tmp = []
                tmp.append(errorMessage)
                tmp.append("")
                returnList.append(tmp)

    return returnList
