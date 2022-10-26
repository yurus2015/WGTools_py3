
import maya.cmds as cmds

from validator2019.utils.validator_API import *
checkId = 2
checkLabel = "3.6 Check Objects with backface culling"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    objList = vl_listAllTransforms()
    returnList = []

    shapeArray = cmds.ls(type='mesh', dag=1, l = True)
    if shapeArray:
        polyArray = list(set(cmds.listRelatives(shapeArray, p=1, type="transform", f = True)))

        for obj in polyArray:
            try:
                BCStatus  = cmds.getAttr(obj+".backfaceCulling")
                if BCStatus != 0:
                    tmp = []
                    tmp.append(obj + " has the .backfaceCulling argument turned on")
                    tmp.append(obj)
                    returnList.append(tmp)
            except:
                pass


    return  returnList