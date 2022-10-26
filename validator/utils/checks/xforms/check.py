import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 62
checkLabel = "1.13 Check Freeze Transformations "


def vl_checkXforms(input, m):
    objectList = eval(input())
    returnList = []
    warn = None
    gun = re.compile("gun_\d")
    for x in objectList:
        if gun.search(x) == None:
            warn = 0
            objTtranslate = cmds.xform (x, q=True, t=True, ws = True) + cmds.xform (x, q=True, ro=True, ws = True)
            objScale = cmds.xform (x, q=True, s=True, r=True)
            for y in range(len(objTtranslate)):
                 objTtranslate[y] = round(objTtranslate[y], 3)
            for i in objTtranslate:
                if i != 0.0:
                    warn = 1
            for i in objScale:
                if i != 1.0:
                    warn = 1
            if warn == 1:
                if m == 1:
                    returnList.append(x)
                else:
                    returnList.append(x)

    return returnList


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []
    return  returnList
