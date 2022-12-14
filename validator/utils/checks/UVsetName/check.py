import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 57
checkLabel = "4.16 Check name of UV sets"


def main():
    objList = vl_listAllTransforms()
    returnList = []
    for x in objList:
        uvSets = cmds.polyUVSet(x, query=True, allUVSets=True)
        if uvSets:
            if len(uvSets) == 1 and uvSets[0] != 'map1':
                tmp = []
                tmp.append(x)
                tmp.append(x)
                returnList.append(tmp)

            else:
                if len(uvSets) == 2:
                    if uvSets[0] != 'map1' or uvSets[1] != 'map2':
                        tmp = []
                        tmp.append(x)
                        tmp.append(x)
                        returnList.append(tmp)

    return returnList
