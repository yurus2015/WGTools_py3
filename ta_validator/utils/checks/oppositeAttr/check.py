
import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 36
checkLabel = "3.8 Check Objects with attribute 'Opposite' turned on"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    objList = vl_listAllTransforms()
    returnList = []

    shapeArray = cmds.ls(type='mesh', dag=1, l = True)
    if shapeArray:
        polyArray = list(set(cmds.listRelatives(shapeArray, p=1, type="transform", f = True)))

        for obj in polyArray:
            try:
                OppositeStatus = cmds.getAttr(obj + ".opposite")
                if OppositeStatus == 1:
                    tmp = []
                    tmp.append(obj)
                    tmp.append(obj)
                    returnList.append(tmp)
            except:
                pass


    return  returnList
