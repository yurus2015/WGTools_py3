import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 23
checkLabel = "1.3 Check LOD Existence"


def main():
    objList = vl_listAllTransforms()
    returnList = []

    objectList = []
    objectList = vl_objMeshData()

    for i in objectList:
        if i[-1].find("lod") == -1:
            tmp = []
            tmp.append(i[1])
            tmp.append(i[1])
            returnList.append(tmp)

    return returnList
