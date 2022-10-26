import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 59

checkLabel = "5.1 Vertex  Normal Method"

def main():
    print('<< ' + checkLabel.upper() + ' >>')
    objMatData = vl_objMaterialsData()
    returnList = []

    #allObj = cmds.listRelatives(cmds.ls(type="mesh", l=1), p=1, f=1)
    allMeshes = cmds.ls(type="mesh", l=1, fl=1)
    if allMeshes:
        for i in allMeshes:
            parent  = cmds.listRelatives(i, p=1, f=1)[0]
            vmn = cmds.getAttr(i + ".vertexNormalMethod")
            if not vmn == 3:
                tmp = []
                tmp.append(parent)
                tmp.append(parent)
                returnList.append(tmp)



    return  returnList
