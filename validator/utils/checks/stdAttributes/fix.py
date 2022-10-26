import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 40
checkLabel = "1.19 Check for extra attributes"


def stdAttributesUtil(*args):
    attrArray = ["visibility", "translateX", "translateY", "translateZ", "rotateX", "rotateY","rotateZ", "scaleX","scaleY","scaleZ", "currentUVSet", "UDP3DSMAX", "MaxHandle"]

    if args:
        for obj in args:
            objAttrList = cmds.listAttr(obj, k = True)
            for attr in objAttrList:
                if attr not in attrArray:
                    cmds.deleteAttr(obj, attribute=attr)


	return []