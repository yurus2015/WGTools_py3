import maya.cmds as cmds

checkId = 6001
checkLabel = "6.11 Check object history"


def removeDupplicateList(currentList):
    resultList = list(set(currentList))
    return resultList


def main():
    returnList = []

    listAllMesh = cmds.ls(type='transform')
    listAllMesh = cmds.filterExpand(listAllMesh, sm=12)
    if not listAllMesh:
        return returnList
    listAllMesh = removeDupplicateList(listAllMesh)

    exeptType = ['displayLayer', 'shadingEngine', 'groupId', 'objectSet']

    for mesh in listAllMesh:
        countNodes = 0
        noDAGNodes = cmds.listHistory(mesh, pdo=1)
        # print 'NODES', noDAGNodes

        if noDAGNodes:
            countNodes = len(noDAGNodes)
            for node in noDAGNodes:
                currentType = cmds.nodeType(node)
                for typ in exeptType:
                    if currentType == typ:
                        countNodes = countNodes - 1

        if countNodes > 0:
            tmp = []
            tmp.append(mesh + " has undeleted history")
            tmp.append(mesh)
            returnList.append(tmp)

    return returnList
