import maya.cmds as cmds
import os
import re

dir = os.path.dirname(__file__)
from validator.utils.validator_API import *

checkId = 120
checkLabel = "Check havok objects with non-zero transformations"


def removeList(fromList, thisList):
    resultList = [n for n in fromList if n not in thisList]
    resultList = list(resultList)
    return resultList


def main():
    objList = cmds.ls(l=True, type="transform")
    returnList = []
    hpList = []

    names = vl_read_json(dir, "havokFreezeNames.json")
    reg_exp = []
    for x in names["names"]:
        reg_exp.append(re.compile(x))

    if objList:
        for m in objList:
            if 'HP' in m:
                hpList.append(m)
        objList = removeList(objList, hpList)

        # Check for objects with non-zero transformations
        for obj in objList:
            find = False
            for r in reg_exp:
                if r.search(obj.split("|")[1]):
                    find = True
            if not find:
                continue

            objTranslate = cmds.xform(obj, q=1, t=1)
            objRotate = cmds.xform(obj, q=1, ro=1)
            objScale = cmds.xform(obj, q=1, r=1, s=1)
            if (objTranslate != [0, 0, 0] or objRotate != [0, 0, 0] or objScale != [1, 1, 1]):
                tmp = []
                tmp.append(obj)
                tmp.append(obj)
                returnList.append(tmp)

    return returnList
