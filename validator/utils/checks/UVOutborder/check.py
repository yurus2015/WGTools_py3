import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from validator.utils.validator_API import *

checkId = 53
checkLabel = "8.13 Check UVs out of range"


def main():
    obj_list = vl_listAllTransforms()
    obj_list = cmds.filterExpand(obj_list, sm=12, fp=1)
    # objList = cmds.ls(objList, l=1)

    track_L, track_R = vl_findTracksInLods()
    track_list = track_L + track_R
    track_list = cmds.filterExpand(track_list, sm=12, fp=1)
    # trackList = cmds.ls(trackList, l=1)

    return_list = []

    if obj_list:
        # remove track objects from the objList
        if len(track_list) > 0:
            for i in track_list:
                obj_list.remove(i)

        # for all objs in objList get its uv coordinates
        for i in obj_list:
            if i.find("lod0") != -1 or i.find("lod1") != -1:
                print('Current object ', i)
                util = OpenMaya.MScriptUtil()
                selectionList = OpenMaya.MSelectionList()
                selectionList.add(i)
                OpenMaya.MGlobal.setActiveSelectionList(selectionList)

                DagPath = OpenMaya.MDagPath()
                fullPath = DagPath.fullPathName()

                selectionList.getDagPath(0, DagPath)

                component = OpenMaya.MObject()

                fnMesh = OpenMaya.MFnMesh(DagPath)
                uArray = OpenMaya.MFloatArray()
                vArray = OpenMaya.MFloatArray()

                fnMesh.getUVs(uArray, vArray)

                status = False
                for i in range(0, len(uArray)):
                    if uArray[i] < 0 or uArray[i] > 1 or vArray[i] < 0 or vArray[i] > 1:
                        status = True
                        break
                if status == True:
                    tmp = [DagPath.fullPathName(), DagPath.fullPathName()]
                    return_list.append(tmp)

        if len(track_list) > 0:
            for i in track_list:
                if i.find("lod0") != -1:
                    util = OpenMaya.MScriptUtil()
                    selectionList = OpenMaya.MSelectionList()
                    selectionList.add(i)
                    OpenMaya.MGlobal.setActiveSelectionList(selectionList)

                    DagPath = OpenMaya.MDagPath()
                    fullPath = DagPath.fullPathName()

                    selectionList.getDagPath(0, DagPath)

                    component = OpenMaya.MObject()

                    fnMesh = OpenMaya.MFnMesh(DagPath)
                    uArray = OpenMaya.MFloatArray()
                    vArray = OpenMaya.MFloatArray()

                    fnMesh.getUVs(uArray, vArray)

                    status = False
                    for i in range(0, len(uArray)):
                        if uArray[i] < 0 or uArray[i] > 1:
                            status = True
                            break
                    if status == True:
                        tmp = [DagPath.fullPathName(), DagPath.fullPathName()]
                        return_list.append(tmp)

        OpenMaya.MGlobal.clearSelectionList()

    return return_list
