import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 28

checkLabel = "3.30 One material per object"


def main():
    objMatData = vl_objMaterialsData()
    returnList = []

    # allObj = cmds.listRelatives(cmds.ls(type="mesh", l=1), p=1, f=1)
    allMeshes = cmds.ls(type="mesh", l=1, fl=1)

    if allMeshes:

        for i in allMeshes:
            iSG = cmds.listConnections(i, type="shadingEngine")
            try:
                iSG = list(set(cmds.listConnections(i, type="shadingEngine")))
            except:
                pass

            if iSG:
                if len(iSG) > 1:
                    tmp = []
                    tmp.append(cmds.listRelatives(i, p=1, f=1)[0])
                    tmp.append(cmds.listRelatives(i, p=1, f=1)[0])
                    returnList.append(tmp)

    return returnList
