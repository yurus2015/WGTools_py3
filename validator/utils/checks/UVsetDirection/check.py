import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import re
from validator.utils.validator_API import *

checkId = 56
checkLabel = "8.9 Check direction of map1(track) "


def getDagPath(name):
    selectionList = OpenMaya.MSelectionList()
    selectionList.add(name)
    dagPath = OpenMaya.MDagPath()
    selectionList.getDagPath(0, dagPath)
    return dagPath


def intersect_ray(mesh, source, direction, maxDist=9999999999):
    meshFn = OpenMaya.MFnMesh(getDagPath(mesh))
    # Get source point
    sourcePt = OpenMaya.MPoint(source[0] * 100, source[1] * 100, source[2] * 100)
    # Get direction vector
    directionVec = OpenMaya.MVector(direction[0], direction[1], direction[2])

    # Calculate intersection
    hitPtArray = OpenMaya.MPointArray()
    facesIDs = OpenMaya.MIntArray()
    meshFn.intersect(sourcePt, directionVec, hitPtArray, 0.0001, OpenMaya.MSpace.kWorld, facesIDs)

    # Return intersection hit point
    return [(hitPtArray[i][0], hitPtArray[i][1], hitPtArray[i][2]) for i in range(hitPtArray.length())], facesIDs


def bboxCenter(obj):
    center = cmds.getAttr(obj + '.center')[0]
    return center


def uvCheck(object):
    UV_vectorPoints = []
    VTS_vectorPoints = []
    errorList = []

    center = bboxCenter(object)
    intersection, face = intersect_ray(object, [center[0], center[1], center[2]], [0, 1, 0])
    # print 'INTER', intersection, face
    for x in face:

        face = object + ".f[" + str(x) + "]"
        uvs_list = cmds.ls(cmds.polyListComponentConversion(face, ff=True, tuv=True), fl=True)
        for x in uvs_list:
            UV_vectorPoints.append([x, round(cmds.polyEditUV(x, q=True)[1], 3)])

        UV_vectorPoints.sort(key=lambda c: c[1])
        print('VECTORS ', UV_vectorPoints)

        if len(UV_vectorPoints) == 3:
            UV_vectorPoints = [UV_vectorPoints[0], UV_vectorPoints[2]]

        if len(UV_vectorPoints) == 4:
            UV_vectorPoints = [UV_vectorPoints[0], UV_vectorPoints[3]]

        UV_vector = UV_vectorPoints[1][1] - UV_vectorPoints[0][1]

        for x in UV_vectorPoints:
            vtsName = cmds.ls(cmds.polyListComponentConversion(x[0], fuv=True, tv=True), fl=True)
            VTS_vectorPoints.append(round(cmds.xform(vtsName, q=True, ws=True, t=True)[2], 3))
        VTS_vector = VTS_vectorPoints[1] - VTS_vectorPoints[0]
        if VTS_vector < 0:
            errorList.append(object)

    return list(set(errorList))


def opposite(tracks):
    for track in tracks:
        opposite = cmds.getAttr(track + ".opposite")
        if opposite:
            cmds.setAttr(track + ".opposite", False)


def main():
    tracks_R, tracks_L = vl_findTracksInLods()
    tracks_R.extend(tracks_L)

    # check opposite
    opposite(tracks_R)

    returnList = []
    for x in tracks_R:
        uvSets = cmds.polyUVSet(x, query=True, allUVSets=True)
        cmds.polyUVSet(x, currentUVSet=True, uvSet=uvSets[0])
        temp = uvCheck(x)
        if len(temp) != 0:
            for y in temp:
                tmp = []
                tmp.append(y)
                tmp.append(y)
                returnList.append(tmp)

    # for x in tracks_L:
    #     uvSets = cmds.polyUVSet (x, query = True, allUVSets=True)
    #     cmds.polyUVSet(x, currentUVSet=True,  uvSet= uvSets[0])
    #     temp = uvCheck(x)
    #     if len(temp) != 0:
    #     	for y in temp:
    #     		tmp = []
    #             tmp.append(y)
    #             tmp.append(y)
    #             returnList.append(tmp)

    return returnList
