import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import math
from validator.utils.validator_API import *

checkId = 42
checkLabel = "Check for Tank Direction"


def main():
    listTransforms = vl_listAllTransforms()
    returnList = []

    if len(listTransforms) > 0:
        gunList = cmds.ls("*gun*", type="transform", l=1)
        turretList = cmds.ls("*turret*", type="transform", l=1)

        if len(gunList) > 0:
            gunObj = gunList[0]

            zeroPoint = [0.0, 0.0, 0.0]
            turretPivot = [0.0, 0.0, 0.0]

            if len(turretList) > 0:
                turretPivotTmp = cmds.xform(turretList[0], q=1, rp=1, a=1)
                # print turretList[0]
                # print turretPivotTmp

            objList = OpenMaya.MSelectionList()
            objList.add(gunObj)

            minZ_offset = 0
            maxZ_offset = 0

            objIter = OpenMaya.MItSelectionList(objList, OpenMaya.MFn.kGeometric)
            while not objIter.isDone():
                dagPath = OpenMaya.MDagPath()
                objIter.getDagPath(dagPath)
                xNode = OpenMaya.MFnDagNode(dagPath)
                bbox = xNode.boundingBox()
                minZ_offset_abs = abs(bbox.min().z) / 100
                maxZ_offset_abs = abs(bbox.max().z) / 100
                minZ_offset = bbox.min().z / 100
                maxZ_offset = bbox.max().z / 100
                # print "min ", minZ_offset
                # print "max ", maxZ_offset
                next(objIter)

            if len(turretList) > 0:
                if abs(turretPivotTmp[2] - minZ_offset) < abs(turretPivotTmp[2] - maxZ_offset):
                    message = "Tank has incorrect direction"
                    tmp = []
                    tmp.append(message)
                    tmp.append("")
                    returnList.append(tmp)

            elif minZ_offset_abs < maxZ_offset_abs:
                message = "Tank has incorrect direction"
                tmp = []
                tmp.append(message)
                tmp.append("")
                returnList.append(tmp)

    return returnList
