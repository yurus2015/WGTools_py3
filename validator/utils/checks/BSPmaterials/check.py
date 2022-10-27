#########################################################################################################
# """                                      matDataList[]                                              """#
# """   splited list format [materials_count, full_path, obj_name, material, material, ... ]          """#
# """                                                                                                 """#
# """   example:    [2, |env039_EngineerBridge_unique|lod0|n_0,   n_0,   n_wood_0,  n_metal_0, ...]   """#
# """                |                     |                       |        |           |             """#
# """        materials count         obj full path              obj name   mat         mat            """#
# """               [0]                   [1]                     [2]      [3]         [4]            """#
#########################################################################################################

import maya.cmds as cmds
from validator.utils.validator_API import *
import re

checkId = 6
checkLabel = "6.14 Check BSP correct materials"


def checkLambert(obj):
    result = None
    msg = None
    shortName = obj[1].split("|")[-1]

    # check if it has lambert material
    if shortName.find("bsp") != -1:
        for x in range(2, len(obj)):
            # if obj[x].find('lambert') != -1:
            if "lambert" in obj[x]:
                result = obj[1]
                msg = obj[1] + " - has a material named " + obj[x]
                return result, msg

    # check if s_wall has s_wall material
    if shortName.find("s_wall") != -1:
        status = 0
        for x in range(3, len(obj)):
            if obj[x].find("s_wall") != -1:
                status = 1
        if status == 0:
            result = obj[1]
            msg = obj[1] + " - has a material(s) with a wrong name "

    # check s_0 n_0 d_0 for s_nd, s/n/d_wood/stone/metal
    searchList = []
    searchList.append(re.compile("^s_\d"))
    searchList.append(re.compile("^d_\d"))
    searchList.append(re.compile("^n_\d"))
    searchList.append(re.compile("^s\d"))
    searchList.append(re.compile("^d\d"))
    searchList.append(re.compile("^n\d"))

    def check_snd(obj, type):
        for x in range(3, len(obj)):
            if obj[x].find(type + "_nd") != -1 or obj[x].find(type + "_wood") != -1 or obj[x].find(
                    type + "_stone") != -1 or obj[x].find(type + "_metal") != -1:
                return 0
            else:
                return 1

    status = 0
    for i in searchList:
        # print "BABAA:  ", shortName[:3], shortName[:2]
        if i.search(shortName[:3]) or i.search(shortName[:2]):
            status = 1
    if status == 1:
        if shortName[0] == "s":
            if check_snd(obj, "s"):
                result = obj[1]
                msg = obj[1] + " - has a material(s) with a wrong name "
        if shortName[0] == "d":
            if check_snd(obj, "d"):
                result = obj[1]
                msg = obj[1] + " - has a material(s) with a wrong name "
        if shortName[0] == "n":
            if check_snd(obj, "n"):
                result = obj[1]
                msg = obj[1] + " - has a material(s) with a wrong name "

    return result, msg


def check_bsp_mat(obj):
    result = None
    msg = None
    shortName = obj[1].split("|")[-1]
    bspType = shortName[0]
    bspIdx = shortName.split("_")[-2]
    numOfMat = len(obj) - 3
    obj_materials = obj[3:]

    # find all objects by type (d|n) in the same lod with the same index (first digit)
    tmpPath = obj[1].split("lod")[0][:-1]
    lodPath = tmpPath + "|lod0|" if tmpPath else "|lod0|"

    def get_obj_by_type_for_bsp(path):
        relatives = cmds.listRelatives(path, f=1, c=1)
        obj_by_type = None
        for rel in relatives:
            relShort = rel.split("|")[-1]

            if relShort[0] == bspType and relShort.find("bsp") == -1 and relShort == shortName[:-4]:
                materials = []
                # get Materials
                rel_shapeNod = cmds.listRelatives(rel, c=1, type="mesh", f=1)[0]
                # get history
                tmp = cmds.listHistory(rel_shapeNod, f=1, ag=1)
                temp = []
                for hstr in tmp:
                    if cmds.nodeType(hstr) == "shadingEngine":
                        temp.append(hstr)
                if temp != None:
                    SG = temp
                    SG = list(set(SG))
                    for i in range(len(SG)):
                        temp1 = cmds.listConnections(SG[i] + ".surfaceShader")
                        if temp1 != None:
                            for y in temp1:
                                if y != None:
                                    materials.append(y)
                                else:
                                    pass
                        else:
                            pass
                else:
                    pass
                numOfMat_rel = len(materials)

                # comparison
                if numOfMat_rel == numOfMat:
                    for i in range(numOfMat):
                        if materials[i] != obj_materials[i]:
                            obj_by_type = obj
                            break

        return obj_by_type

    result = get_obj_by_type_for_bsp(lodPath)
    if result:
        msg = obj[1] + " - has diffrent from original object material(s) "

    return result, msg


def main():
    #

    returnList = []

    polyObj_matlist = []
    polyObj_matlist = vl_objMaterialsData()

    if polyObj_matlist:
        bsp_list = []
        for i in polyObj_matlist:
            result = None
            result, msg = checkLambert(i)
            if result:
                tmp = []
                tmp.append(msg)
                tmp.append(result)
                returnList.append(tmp)

            if i[1].find("_bsp") != -1 and i[1].split("|")[-1][0] != "s":
                bsp_list.append(i)

        result = None
        if bsp_list:
            for i in bsp_list:
                result, msg = check_bsp_mat(i)  # send one object descriptor
                if result:
                    tmp = []
                    tmp.append(msg)
                    tmp.append(result)
                    returnList.append(tmp)

    return returnList
