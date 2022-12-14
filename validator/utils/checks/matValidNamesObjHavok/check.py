import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 1115
checkLabel = "Check names of materials for 'havok' group"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []

    """   example:    [2, |env039_EngineerBridge_unique|lod0|n_0,   n_0,   n_wood_0,  n_metal_0, ...]   """
    materials = vl_objMaterialsData()

    for i in materials:
        objName = i[1]
        objShortName = i[2]
        objGroup = objName.split("|")[1]

        error = 0
        if "havok" in objGroup:
            materialList = i[3:]
            if materialList:
                for i in materialList:
                    if i[0] != "n":
                        error = 1

        if error:
            returnList.append([objShortName + " has materials which names doesn't start with 'n_'", objName])

    return returnList
