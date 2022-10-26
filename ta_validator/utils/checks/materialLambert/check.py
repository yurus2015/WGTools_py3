
import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 26
checkLabel = "3.3 Check Objects with material type different from Lambert"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    objList = vl_listAllTransforms()
    returnList = []



    objMatList = vl_objMaterialsData()


    if len(objMatList) != 0:
        for i in objMatList:

            if i[0] == 0:
                continue
            elif i[0] == 1 and i[3] == "noMaterial!":
                continue

            mat = i[3:]
            for j in mat:
                if j != "noMaterial!":
                    if cmds.objectType(j) != 'lambert' and cmds.objectType(j) != 'particleCloud':
                        tmp = []
                        tmp.append(i[1])
                        tmp.append(i[1])
                        returnList.append(tmp)
                        break




    return  returnList
