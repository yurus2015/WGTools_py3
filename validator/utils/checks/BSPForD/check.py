import maya.cmds as cmds
import re
from validator.utils.validator_API import *


def removeDupplicateList(currentList):
    resultList = list(set(currentList))
    return resultList


def checkBSP_GRP(lod):
    result = None

    lod0_rels = []
    if cmds.listRelatives(lod, c=1, ad=1, type="mesh"):
        lod0_rels = cmds.listRelatives(cmds.listRelatives(lod, ad=1, c=1, type="mesh", f=1), p=1, type="transform", f=1)
        lod0_rels = removeDupplicateList(lod0_rels)
    for i in lod0_rels:
        if i.find("bsp") != -1:
            result = lod
            break
    return result


def main(objType, lod):
    result = None
    numlist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # find all by objType

    lod0_rels = []
    if cmds.listRelatives(lod, c=1, ad=1, type="mesh"):
        lod0_rels = cmds.listRelatives(cmds.listRelatives(lod, ad=1, c=1, type="mesh", f=1), p=1, type="transform", f=1)
        lod0_rels = removeDupplicateList(lod0_rels)

    # filter by objType
    objType_list = []
    if lod0_rels:
        for i in lod0_rels:
            iShort = i.split("|")[-1]
            # if iShort[0] == objType:
            if (re.findall(objType, iShort)):
                print('<<FIND >>', objType, iShort)
                objType_list.append(iShort)

    # get bsp from this listRelatives
    objType_bsp_list = []
    objType_notBsp_list = []
    if objType_list:
        # objType_notBsp_list = objType_list
        for i in objType_list:
            if i.find("bsp") != -1 and i.find("wall") == -1 and i.find("ramp") == -1:
                print('<<HAVE BSP >>', i)
                objType_bsp_list.append(i)
            elif i.find("bsp") == -1 and i.find("wall") == -1 and i.find("ramp") == -1:
                print('<<NOT HAVE BSP >>', i)
                objType_notBsp_list.append(i)

    # check
    if objType_notBsp_list:  # only if we have non-BSP object list - do comparison
        print('<<NOT BSP LIST >>', objType_notBsp_list, len(objType_notBsp_list))
        print('<<BSP LIST >>', objType_bsp_list, len(objType_bsp_list))
        # reorganize non-bsp list by last digit
        notBsp_formatted = []
        for i in objType_notBsp_list:
            notBsp_formatted.append(i[-1])  # 1 1 2 2 3 3 4 4
        notBsp_formatted = list(set(notBsp_formatted))  # 1 2 3 4
        # print '<<BSP LIST FORM >>', notBsp_formatted

        # if bsp_list not empty
        if objType_bsp_list:
            if len(notBsp_formatted) != len(objType_bsp_list):
                result = lod

    return result


def check_S_WALL_RAMP(lod, objType):
    result = None

    # find all by objType

    lod0_rels = []
    if cmds.listRelatives(lod, c=1, ad=1, type="mesh"):
        lod0_rels = cmds.listRelatives(lod, ad=1, c=1, type="transform", f=1)

    # filter by objType
    objType_list = []
    if lod0_rels:
        for i in lod0_rels:
            iShort = i.split("|")[-1]  # short object name
            if iShort.find(objType) != -1 and not cmds.listRelatives(i, c=1, type="transform", f=1):
                objType_list.append(iShort)

    # get bsp from this listRelatives
    objType_bsp_list = []
    objType_notBsp_list = []

    if objType_list:
        # objType_notBsp_list = objType_list
        for i in objType_list:

            if i.find("bsp") != -1:
                objType_bsp_list.append(i)
            else:
                objType_notBsp_list.append(i)

    # check
    if objType_notBsp_list:  # only if we have non-BSP object list - do comparison

        # reorganize non-bsp list by last digit
        notBsp_formatted = []
        for i in objType_notBsp_list:
            notBsp_formatted.append(i[-1])  # 1 1 2 2 3 3 4 4
        notBsp_formatted = list(set(notBsp_formatted))  # 1 2 3 4

        # if bsp_list not empty
        if objType_bsp_list:
            if len(notBsp_formatted) != len(objType_bsp_list):
                result = lod

    return result


def BSPForDCheck():
    #

    returnList = []

    lod0List = cmds.ls("*lod0*", type="transform", l=1)
    for lod in lod0List:
        stage_1 = True  # check bsp in groups
        stage_2 = False  # check S N D
        stage_3 = False  # check bsp for s_wall and s_ramp

        if stage_1:
            result = checkBSP_GRP(lod)
            if result:
                stage_2 = True
                stage_3 = True

        if stage_2:
            n_result = checkBSP("^n", lod)
            if n_result:
                tmp = []
                tmp.append(n_result + " - amount of N and N_bsp is different")
                tmp.append(n_result)
                returnList.append(tmp)

            d_result = checkBSP("^d", lod)
            if d_result:
                tmp = []
                tmp.append(d_result + " - amount of D and D_bsp is different")
                tmp.append(d_result)
                returnList.append(tmp)

            s_result = checkBSP("^s0$", lod)
            if s_result:
                tmp = []
                tmp.append(s_result + " - amount of S0 and S0_bsp is different")
                tmp.append(s_result)
                returnList.append(tmp)

            s_d_result = checkBSP("^s\d+_\d+$", lod)
            if s_result:
                tmp = []
                tmp.append(s_result + " - amount of S(d)_(d) and S(d)_(d)_bsp is different")
                tmp.append(s_result)
                returnList.append(tmp)

        if stage_3:
            # check s_ramp and s_wall
            s_ramp_result = check_S_WALL_RAMP(lod, "s_ramp")
            if s_ramp_result:
                tmp = []
                tmp.append(s_ramp_result + " - amount of s_ramp and s_ramp_bsp is different")
                tmp.append(s_ramp_result)
                returnList.append(tmp)

            s_wall_result = check_S_WALL_RAMP(lod, "s_wall")
            if s_wall_result:
                tmp = []
                tmp.append(s_wall_result + " - amount of s_wall and s_wall_bsp is different")
                tmp.append(s_wall_result)
                returnList.append(tmp)

    return returnList
