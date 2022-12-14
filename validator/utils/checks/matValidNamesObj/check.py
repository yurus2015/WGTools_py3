import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 280
checkLabel = "3.1 Check names of materials"

# import os
import re


# dir = os.path.dirname(__file__)
# dir = "D:\\art_branch\\devtools\\scripts\\validator\\resources\\WoT\\Checks\\matValidNamesObj"

def removeDupplicateList(currentList):
    resultList = list(set(currentList))
    return resultList


def removeList(fromList, thisList):
    resultList = [n for n in fromList if n not in thisList]
    resultList = list(resultList)
    return resultList


def main():
    validMatName = ['s_wall_', 's_ramp_', 's_nd', 'n_wood', 'n_stone', 'n_metal', 'd_wood', 'd_stone', 'd_metal']
    exeptMatName = ['lambert1', 'particleCloud1']
    returnList = []

    # Horrible Dirty Shit for havok preset
    if "havok" in cmds.file(q=1, sn=1):
        return returnList

    allSceneMaterials = cmds.ls(mat=1)

    for mat in allSceneMaterials:
        for name in validMatName:
            if re.search(name + '[0-9]$', mat):
                exeptMatName.append(mat)
            if re.findall('\d_\d+', mat) and re.findall('_\d$', mat):
                exeptMatName.append(mat)
    invalidMat = removeList(allSceneMaterials, exeptMatName)
    for mat in invalidMat:
        tmp = []
        tmp.append(mat + " incorrect material`s name")
        tmp.append(mat)
        returnList.append(tmp)

    return returnList
