import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from validator.utils.validator_API import *

checkId = 532
checkLabel = "Check UVs out of 8 textures range"


def main():
    objList = vl_listAllTransforms()
    track_L, track_R = vl_findTracksInLods()
    trackList = track_L + track_R
    returnList = []

    if len(objList) > 0:
        # remove track objects from the objList
        if len(trackList) > 0:
            for i in trackList:
                objList.remove(i)

    for i in objList:
        # print 'OBJECT ', i
        # fix multishape object, example, skinning
        shape = cmds.listRelatives(i, s=True, f=True)[0]
        uvBox = cmds.polyEvaluate(shape, boundingBox2d=True)
        if uvBox[0][0] < -8 or uvBox[0][1] > 8 or uvBox[1][0] < -8 or uvBox[1][1] > 8:
            tmp = []
            tmp.append(i)
            tmp.append(i)
            returnList.append(tmp)

    if len(trackList) > 0:
        for i in trackList:
            shape = cmds.listRelatives(i, s=True, f=True)[0]
            uvBox = cmds.polyEvaluate(shape, boundingBox2d=True)
            if uvBox[0][0] < -8 or uvBox[0][1] > 8:
                tmp = []
                tmp.append(i)
                tmp.append(i)
                returnList.append(tmp)

    return returnList
