import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 4201

checkLabel = "Check Scene Materials"

import re


def removeDupplicateList(currentList):
    resultList = list(set(currentList))
    return resultList


def removeList(fromList, thisList):
    resultList = [n for n in fromList if n not in thisList]
    resultList = list(resultList)
    return resultList


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


def objectMaterialCheck():
    validMatName = ['s_wall_', 's_ramp_', 's_nd', 'n_wood', 'n_stone', 'n_metal', 'n_glass', 'd_wood', 'd_stone',
                    'd_metal', 'd_glass']
    exeptMatName = ['lambert1', 'particleCloud1']
    returnList = []

    allSceneMaterials = cmds.ls(mat=1)

    for mat in allSceneMaterials:
        for i in range(2):
            if re.search(validMatName[i] + '\d+$', mat):
                # print 'VALID MATERIAL RAMP AND WALL: ', mat
                exeptMatName.append(mat)

        for i in range(2, len(validMatName)):
            if re.search(validMatName[i] + '\d+$', mat) or re.search(validMatName[i] + '\d+_\d+$', mat):
                # print 'VALID MATERIAL EXCEPT RAMP&WALL', mat
                exeptMatName.append(mat)

    invalidMat = removeList(allSceneMaterials, exeptMatName)
    for mat in invalidMat:
        tmp = []
        tmp.append(mat + " wrong material`s name - correct it and re-check")
        tmp.append(mat)
        returnList.append(tmp)

    # check assigned mat
    '''
    for mat in allSceneMaterials:
        tmp = []
        cmds.select(mat)
        cmds.hyperShade(objects =mat)
        faces = cmds.filterExpand(sm=34)

        if faces:
            tmp.append(mat + " assigned to faces, need assign to object")
            tmp.append(faces)
            returnList.append(tmp)
            cmds.select(cl=1)
    '''

    # compare materials name with mesh`s
    shapesInSel = cmds.ls(dag=1, type='mesh')
    # truble - transform may have more then one shape
    transformMesh = cmds.listRelatives(shapesInSel, p=1, type='transform', f=1)
    transformMesh = removeDupplicateList(transformMesh)
    for transform in transformMesh:
        if 'HP' not in transform:
            shapes = cmds.listRelatives(transform, s=1, f=1)
            # switcher for multyshape connection
            check_mat = 0
            for shape in shapes:
                shadingGrp = cmds.listConnections(shape, type='shadingEngine')
                shader = cmds.ls(cmds.listConnections(shadingGrp), materials=1)
                if shadingGrp:
                    check_mat = 1
                    break

            if check_mat == 1:

                # shader_short = None
                # try:
                #	shader_short = (re.findall('\w\d', shader[0]))[0][-1]
                # except:
                #	pass

                # transform_short = None
                # try:
                #	transform_short = (re.findall('[a-z]\d', transform.split('|')[-1]))[0][-1]
                # except:
                #	pass

                if shader[0] in exeptMatName:

                    if 's_ramp' in transform.split('|')[-1] and 's_ramp' not in shader[0]:
                        tmp = []
                        tmp.append(
                            transform + " incorrect assigned material for current type (to ramp-object assigned non ramp-material)")
                        tmp.append(transform)
                        returnList.append(tmp)

                    if (re.search('^\w', transform.split('|')[-1])).group() != (re.search('^\w', shader[0])).group():
                        tmp = []
                        tmp.append(transform + " incorrect assigned material for current type (check first letter)")
                        tmp.append(transform)
                        returnList.append(tmp)

                    if 'ramp0' in transform.split('|')[-1] or 'wall0' in transform.split('|')[-1]:
                        if (re.findall('s_wall_\d+$', shader[0])) and (
                                re.findall('s_wall0_\d+$', transform.split('|')[-1])):

                            if (re.findall('\d+$', shader[0]))[0][-1] != \
                                    (re.findall('\d+$', transform.split('|')[-1]))[0][-1]:
                                tmp = []
                                tmp.append(
                                    transform + " incorrect assigned material for current type (check last digits - must be the same)")
                                tmp.append(transform)
                                returnList.append(tmp)

                    if transform.split('|')[-1][0] == shader[0][0] and transform.split('|')[-1][1::] in shader[0]:

                        pass
                    elif 'ramp' not in transform.split('|')[-1] and 'wall' not in transform.split('|')[
                        -1] and 'bsp' not in transform.split('|')[-1]:
                        tmp = []
                        tmp.append(transform + " incorrect assigned material for current type")
                        tmp.append(transform)
                        returnList.append(tmp)

            else:
                # print (transform + ' has not assigned material')
                tmp = []
                tmp.append(transform + ' has not assigned material')
                tmp.append(transform)
                returnList.append(tmp)

    bsp_list = BSPmaterialsCheck()
    if bsp_list:
        returnList.extend(bsp_list)
    return returnList
