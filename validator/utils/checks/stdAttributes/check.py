import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 40
checkLabel = "1.19 Check for extra attributes"


def main():
    objList = vl_listAllTransforms()
    returnList = []

    shapeArray = cmds.ls(type='mesh', dag=1, l=True)
    if shapeArray:
        polyArray = list(set(cmds.listRelatives(shapeArray, p=1, type="transform", f=True)))

        attrArray = ["visibility", "translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ", "scaleX",
                     "scaleY", "scaleZ", "currentUVSet", "UDP3DSMAX", "MaxHandle"]

        for obj in polyArray:

            isntPassed = False
            objAttrList = cmds.listAttr(obj, k=True)
            for attr in objAttrList:
                if attr not in attrArray:
                    tmp = []
                    tmp.append(obj)
                    tmp.append(obj)
                    returnList.append(tmp)

    return returnList
