import maya.cmds as cmds

from validator.utils.validator_API import *

checkId = 415

checkLabel = "6.5 Check layers of BSP "


def removeDupplicateList(currentList):
    resultList = list(set(currentList))
    return resultList


def main():
    #

    all_additional = []
    returnList = []

    bsp = cmds.ls('*_bsp', tr=1, l=1)
    ramp = cmds.ls('*_ramp', tr=1, l=1)
    wall = cmds.ls('s_wall0*', tr=1, l=1)

    if bsp:
        all_additional.extend(bsp)
    if ramp:
        all_additional.extend(ramp)
    if wall:
        all_additional.extend(wall)

    if all_additional:
        all_additional = removeDupplicateList(all_additional)

        for obj in all_additional:
            layer = cmds.listConnections(obj, type='displayLayer')
            if layer == None:
                tmp = []
                tmp.append(obj + " - attached to a wrong layer")
                tmp.append(obj)
                returnList.append(tmp)

            elif layer[0] != 'BSP':
                tmp = []
                tmp.append(obj + " - attached to a wrong layer")
                tmp.append(obj)
                returnList.append(tmp)

    return returnList
