import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 211

checkLabel = "8.12 Check forbidden symbols in names Tanks"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    #find double __ in all transforms
    objectList = vl_listAllTransforms()
    returnList = []

    #find all shapes which dont have "_" before Shape
    meshList = cmds.ls(type="mesh", l=1)
    for i in meshList:
        meshName = i.split("|")[-1]
        if meshName.find("_Shape") == -1:
            tmp = []
            tmp.append(i)
            tmp.append(i)
            returnList.append(tmp)

    for x in objectList:
        check = x.find("__")
        if check != -1:
            errorMessage = x
            tmp = []
            tmp.append(x)
            tmp.append(x)
            returnList.append(tmp)

    listPolyMeshes = cmds.ls (type='mesh', l=True)
    for x in listPolyMeshes:
        check = x.find("__")
        if check != -1:
            tmp = []
            tmp.append(x)
            tmp.append(x)
            returnList.append(tmp)


    for x in objectList:
        shape = cmds.listRelatives(x)
        fullShape = cmds.listRelatives(x, f=True)
        error = False
        for x in range(len(shape)):
            check = shape[x].count("_")
            if check >2:
                errorMessage = fullShape[x]
                tmp = []
                tmp.append(fullShape[x])
                tmp.append(fullShape[x])
                returnList.append(tmp)

    allNames = []
    for x in listAllMat():
        allNames.append(x)

    for x in vl_listAllTransforms():
        allNames.append(x)

    for x in vl_listAllGroups():
        allNames.append(x)

    for x in allNames:
        for y in x:
            ord(y)
            if ord(y) < 48 or ord(y) > 124:
                tmp = []
                tmp.append(x)
                tmp.append(x)
                returnList.append(tmp)



    return  returnList
