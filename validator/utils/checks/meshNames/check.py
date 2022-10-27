import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 32

checkLabel = "1.10 Check names of meshes"


def main():
    objectData = vl_objMeshData()
    returnList = []

    for x in range(len(objectData)):
        shape = cmds.listRelatives(objectData[x][1], shapes=True)
        print('Shape', shape[0], objectData[x][3])
        if objectData[x][3] == shape[0]:
            tmp = []
            tmp.append(objectData[x][1])
            tmp.append(objectData[x][1])
            returnList.append(tmp)

    return returnList
