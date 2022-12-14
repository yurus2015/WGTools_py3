import maya.cmds as cmds

checkId = 6002
checkLabel = "1.20 Check untriangulate objects"


def removeDupplicateList(currentList):
    resultList = list(set(currentList))
    return resultList


def removeList(fromList, thisList):
    resultList = [n for n in fromList if n not in thisList]
    resultList = list(resultList)
    return resultList


def main():
    returnList = []

    listAllMesh = cmds.ls(type='transform')
    listAllMesh = cmds.filterExpand(listAllMesh, sm=12)
    if not listAllMesh:
        return returnList
    listAllMesh = removeDupplicateList(listAllMesh)

    for mesh in listAllMesh:
        if 'HP_' in mesh or 's_wall' in mesh or 'n_wall' in mesh or '_bsp' in mesh or 's_ramp' in mesh:
            pass
        else:
            tris = cmds.polyEvaluate(mesh, t=True)
            faces = cmds.polyEvaluate(mesh, f=True)

            if tris == faces:
                tmp = []
                tmp.append(mesh + " fully triangulated. Quadrangulate, please")
                tmp.append(mesh)
                returnList.append(tmp)

    return returnList
