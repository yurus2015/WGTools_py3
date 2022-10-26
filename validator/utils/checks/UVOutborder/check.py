import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from validator2019.utils.validator_API import *
checkId = 53
checkLabel = "8.13 Check UVs out of range"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    objList = vl_listAllTransforms()
    objList = cmds.filterExpand(objList, sm=12, fp=1)
    #objList = cmds.ls(objList, l=1)

    track_L, track_R = vl_findTracksInLods()
    trackList = track_L + track_R
    trackList = cmds.filterExpand(trackList, sm=12, fp=1)
    #trackList = cmds.ls(trackList, l=1)

    returnList = []

    if len(objList) > 0:
        #remove track objects from the objList
        if len(trackList) > 0:
            for i in trackList:
                objList.remove(i)


        #for all objs in objList get its uv coordinates
        for i in objList:
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
                    tmp = []
                    tmp.append(DagPath.fullPathName())
                    tmp.append(DagPath.fullPathName())
                    returnList.append(tmp)

        if len(trackList) > 0:
            for i in trackList:
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
                        tmp = []
                        tmp.append(DagPath.fullPathName())
                        tmp.append(DagPath.fullPathName())
                        returnList.append(tmp)

        OpenMaya.MGlobal.clearSelectionList()


    return  returnList
