import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 16
checkLabel = "1.14 Check Objects with history"


def main():
    objList = vl_listAllTransforms()
    returnList = []

    inputStd = ["joint", "tweak", "skinCluster", "mesh", "displayLayer"]

    shapeArray = cmds.ls(type='mesh', dag=1, l=True)
    if shapeArray:
        polyArray = list(set(cmds.listRelatives(shapeArray, p=1, type="transform", f=True)))

        for obj in polyArray:
            tmpListOfinputs = cmds.listHistory(obj, lf=1, il=1)  # List objects which have inputs
            for i in tmpListOfinputs:
                type = cmds.nodeType(i)
                # if type != "joint" and type != "tweak" and type != "skinCluster" and type != "mesh" and type != "displayLayer":
                if type not in inputStd:
                    tmp = []
                    tmp.append(obj + " has an input node of type: " + type)
                    tmp.append(obj)
                    returnList.append(tmp)
                    break

    errorMessage = "Next objects still have a construction history:"

    return returnList
