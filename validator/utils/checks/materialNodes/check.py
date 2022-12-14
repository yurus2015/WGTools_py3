import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 27
checkLabel = "8.4 Check nodes of materials"


def listAllMat():
    listAllMat = []
    allSurfaceShaders = cmds.listNodeTypes("shader/surface")
    objMat = cmds.ls(mat=True)
    for x in objMat:
        for y in allSurfaceShaders:
            if cmds.nodeType(x).find(y) != -1:
                listAllMat.append(x)

    return listAllMat


def main():
    returnList = []
    for x in listAllMat():
        bug = 0
        allConnections = cmds.listConnections(x, p=True, d=False)
        if allConnections != None:
            for y in allConnections:
                connection = cmds.listConnections(y, p=True)
                if connection[0].find(".color") == -1:
                    bug = 1

            if bug == 1:
                tmp = []
                tmp.append(x)
                tmp.append(x)
                returnList.append(tmp)

    return returnList
