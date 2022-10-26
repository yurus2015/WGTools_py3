
import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 48
checkLabel = "3.21 Check for turret pivots"

def getLODList(): #return list of lods in the scene
    lodList = []
    lodList = cmds.ls("*lod*", type="transform", l=1)
    tmp = []
    for i in lodList:
        if cmds.listRelatives(i, c=1, type="transform", f=1):
            tmp.append(i)
    return lodList

def main():
    print('<< ' + checkLabel.upper() + ' >>')
    objList = vl_listAllTransforms()
    returnList = []

    lodList = getLODList()
    if lodList:
        for lod in lodList:
            turretList = []
            relatives = cmds.listRelatives(lod, c=1, f=1)
            if relatives:
                for rel in relatives:
                    if rel.find("turret")!= -1:
                        turretList.append(rel)

            if turretList:
                for t in turretList:
                    #if t - just a polygonal object
                    if cmds.listRelatives(t, type="mesh", f=1):
                        pivotPositionThreshold = 30
                        turretPivot = cmds.xform(t, q=1, ws=1, rp=1)
                        boundingBox = cmds.xform(t, q=1, bb=1, ws =1)
                        xDist = boundingBox[3] - boundingBox[0]; XPercentage = (xDist/100) * pivotPositionThreshold;
                        zDist = boundingBox[5] - boundingBox[2]; ZPercentage = (zDist/100) * pivotPositionThreshold;
                        if turretPivot[0] < (boundingBox[0] + XPercentage) or turretPivot[0] > (boundingBox[3] - XPercentage):
                            tmp = []
                            tmp.append(t)
                            tmp.append(t)
                            returnList.append(tmp)
                        elif turretPivot[2] < (boundingBox[2] + ZPercentage) or turretPivot[2] > (boundingBox[5] - ZPercentage):
                            tmp = []
                            tmp.append(t)
                            tmp.append(t)
                            returnList.append(tmp)
                    else:
                        #if it's turret_0X group
                        grp = t
                        grpRelatives = cmds.listRelatives(grp, c=1, type="transform", f=1)
                        if grpRelatives:
                            #check pivot placement for each object
                            for gRel in grpRelatives:
                                if gRel.find("havok") == -1:
                                    pivotPositionThreshold = 30
                                    turretPivot = cmds.xform(gRel, q=1, ws=1, rp=1)
                                    boundingBox = cmds.xform(gRel, q=1, bb=1, ws=1)
                                    # print boundingBox, gRel
                                    xDist = boundingBox[3] - boundingBox[0]; XPercentage = (xDist/100) * pivotPositionThreshold;
                                    zDist = boundingBox[5] - boundingBox[2]; ZPercentage = (zDist/100) * pivotPositionThreshold;
                                    if turretPivot[0] < (boundingBox[0] + XPercentage) or turretPivot[0] > (boundingBox[3] - XPercentage):
                                        tmp = []
                                        tmp.append(gRel)
                                        tmp.append(gRel)
                                        returnList.append(tmp)
                                    elif turretPivot[2] < (boundingBox[2] + ZPercentage) or turretPivot[2] > (boundingBox[5] - ZPercentage):
                                        tmp = []
                                        tmp.append(gRel)
                                        tmp.append(gRel)
                                        returnList.append(tmp)
                            #check hawok has the same pivot coords as orig
                            origRel = None
                            origPivot = None
                            havok = None
                            havokPivot = None
                            for gRel in grpRelatives:
                                if gRel.find("havok") == -1:
                                    origRel = gRel
                                    origPivot = cmds.xform(gRel, q=1, ws=1, rp=1)
                                    origPivot[0] = round(origPivot[0],4)
                                    origPivot[1] = round(origPivot[1],4)
                                    origPivot[2] = round(origPivot[2],4)
                                else:
                                    havok = gRel
                                    havokPivot = cmds.xform(gRel, q=1, ws=1, rp=1)
                                    havokPivot[0] = round(havokPivot[0],4)
                                    havokPivot[1] = round(havokPivot[1],4)
                                    havokPivot[2] = round(havokPivot[2],4)
                            if origPivot and havokPivot:
                                if not origPivot[0] == havokPivot[0] or not origPivot[1] == havokPivot[1] or not origPivot[2] == havokPivot[2]:
                                    tmp = []
                                    tmp.append(t + " - has havok with different pivot coordinates")
                                    tmp.append(t)
                                    returnList.append(tmp)



    return  returnList
