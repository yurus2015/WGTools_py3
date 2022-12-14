import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 52
checkLabel = "Check AO map of tracks"


def main():
    objList = vl_listAllTransforms()
    track_L, track_R = vl_findTracksInLods()

    returnList = []

    for x in track_L:
        uvSets = cmds.polyUVSet(x, query=True, allUVSets=True)
        if len(uvSets) < 2:
            tmp = []
            tmp.append(x)
            tmp.append(x)
            returnList.append(tmp)
        else:
            cmds.polyUVSet(x, currentUVSet=True, uvSet=uvSets[1])
            numbersUV = cmds.polyEvaluate(x, uv=True)
            for n in range(numbersUV):
                if round(cmds.polyEditUV(x + ".map[" + str(n) + "]", q=True)[1], 3) != 0:
                    tmp = []
                    tmp.append(x)
                    tmp.append(x)
                    returnList.append(tmp)
                    break

    for x in track_R:
        uvSets = cmds.polyUVSet(x, query=True, allUVSets=True)
        if len(uvSets) < 2:
            tmp = []
            tmp.append(x)
            tmp.append(x)
            returnList.append(tmp)
        else:
            cmds.polyUVSet(x, currentUVSet=True, uvSet=uvSets[1])
            numbersUV = cmds.polyEvaluate(x, uv=True)
            for n in range(numbersUV):
                if round(cmds.polyEditUV(x + ".map[" + str(n) + "]", q=True)[1], 3) != 0:
                    tmp = []
                    tmp.append(x)
                    tmp.append(x)
                    returnList.append(tmp)
                    break

    return returnList
