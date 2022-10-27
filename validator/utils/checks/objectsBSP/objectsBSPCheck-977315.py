import maya.cmds as cmds
from validator.resources.validator_API import *
import re

checkId = 706
checkLabel = "3.4 Check objects bsp existance"


def removeDupplicateList(currentList):
    resultList = list(set(currentList))
    return resultList


def removeList(fromList, thisList):
    resultList = [n for n in fromList if n not in thisList]
    resultList = list(resultList)
    return resultList


def objectsNamesCheck():
    validNamesList = vl_objectsValidNames()
    # objectData = vl_objMeshData()
    # hp_object = cmds.ls('HP_*', tr=1, l=1)

    listAllMesh = cmds.ls(type='transform')
    listAllMesh = cmds.filterExpand(listAllMesh, sm=12)
    listAllMesh = removeDupplicateList(listAllMesh)
    listAllMesh = cmds.ls(listAllMesh, l=1)

    invalidNameList = []

    for hp in listAllMesh:
        valid = 0
        hp_shortName = hp.split('|')[-1]
        for y in validNamesList:
            temp = y.search(hp_shortName)
            if temp != None:
                valid = 1
        if valid == 0:
            invalidNameList.append(hp)

    return invalidNameList


def filter_obejcts(obj):
    filtered_list = []
    for x in obj:
        if x.find("bsp") == -1 and x.find("|d") == -1:
            filtered_list.append(x)
    return filtered_list


def filter_bsp(obj):
    filtered_list = []
    for x in obj:
        if '_bsp' in x:
            filtered_list.append(x)
    return filtered_list


def objectsBSPCheck():
    invalidName = objectsNamesCheck()
    return_list = []
    for x in vl_listRootGroups():
        lod0 = cmds.ls(x + "|lod0", l=True)
        obj_in_lod = cmds.listRelatives(lod0, f=True)
        bsp_in_lod = filter_bsp(obj_in_lod)
        obj_in_lod = filter_obejcts(obj_in_lod)

        # print 'INVALID', invalidName
        # print 'BSP    ', obj_in_lod
        # print 'REAL BSP ', bsp_in_lod

        obj_in_lod = removeList(obj_in_lod, invalidName)

        for x in obj_in_lod:
            if (re.findall('s\d+$', x)):
                # print '<<FOUND S*>>', x
                if not cmds.objExists("s0_bsp"):
                    message = x + " object doesn't have _bsp"
                    return_list.append([message, x])
            elif (re.findall('n\d+$', x)):
                # print '<<FOUND N*>>', x
                if not cmds.objExists("n0_bsp"):
                    message = x + " object doesn't have _bsp"
                    return_list.append([message, x])
            else:
                # print '<<FOUND NOT S* NOT N*>>', x
                if not cmds.objExists(x + "_bsp"):
                    message = x + " object doesn't have _bsp"
                    return_list.append([message, x])

        for x in bsp_in_lod:
            non_bsp_name = x.split('_bsp')[0]
            if cmds.objExists(non_bsp_name):
                continue
            else:
                message = x + "  doesn't have appropriate object"
                return_list.append([message, x])

    return return_list
