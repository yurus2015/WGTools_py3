import maya.cmds as cmds
from validator.utils.validator_API import *


def main():
    returnList = []
    chassisList = []
    gunList = []
    hullList = []
    turretList = []
    trackList = []
    lod4list = []

    meshList = cmds.ls(type="mesh", l=1)
    for i in meshList:
        x = i.split(":")[-1]
        if x.find("chassis") != -1:
            chassisList.append(i)
        elif x.find("gun") != -1:
            gunList.append(i)
        elif x.find("hull") != -1:
            hullList.append(i)
        elif x.find("turret") != -1:
            turretList.append(i)
        elif x.find("track") != -1:
            trackList.append(i)
        elif x.find("lod4") != -1:
            lod4list.append(i)

    if chassisList:
        for i in chassisList:
            if i.find("HP") == -1:
                chassisList = i
                break
    if gunList:
        for i in gunList:
            if i.find("HP") == -1:
                gunList = i
                break
    if hullList:
        for i in hullList:
            if i.find("HP") == -1:
                hullList = i
                break
    if turretList:
        for i in turretList:
            if i.find("HP") == -1:
                turretList = i
                break
    if trackList:
        for i in trackList:
            if i.find("HP") == -1:
                trackList = i
                break

    # check hull
    if hullList:
        hullSG = cmds.listConnections(hullList, type="shadingEngine")
        hullTransform = cmds.listRelatives(hullList, p=1, f=1)[0]
        if hullSG:
            for i in hullSG:
                fileNodeColor = None
                fileNodeNormal = None
                try:
                    # here we need to get all file nodes connected with the SG

                    fileNodeColorTmp = cmds.listConnections(i + ".surfaceShader")[0]
                    if fileNodeColorTmp:
                        fileNodeColor = cmds.listConnections(fileNodeColorTmp + ".color")

                    fileNodeNormalTmp = cmds.listConnections(i + ".surfaceShader")[0]
                    if fileNodeNormalTmp:
                        fileNodeNormalTmp = cmds.listConnections(fileNodeNormalTmp + ".normalCamera")
                        if fileNodeNormalTmp:
                            fileNodeNormal = cmds.listConnections(fileNodeNormalTmp, c=0, s=1)
                    # fileNodeColor = cmds.listConnections(cmds.listConnections(i + ".surfaceShader")[0] + ".color")
                    # fileNodeNormal = cmds.listConnections(cmds.listConnections(cmds.listConnections(i + ".surfaceShader")[0] + ".normalCamera"), c=0, s=1)

                    for j in fileNodeNormal:
                        if cmds.nodeType(j) == "file":
                            fileNodeNormal = j
                            break

                except:
                    pass
                if fileNodeColor:
                    sizeX = cmds.getAttr(fileNodeColor[0] + ".outSize")[0][0]
                    sizeY = cmds.getAttr(fileNodeColor[0] + ".outSize")[0][1]
                    if not sizeY <= 4096 and not sizeX <= 4096:
                        tmp = []
                        tmp.append(
                            hullTransform + " - texture res: " + str(sizeX).split(".")[0] + "x" + str(sizeY).split(".")[
                                0] + " is wrong")
                        tmp.append(hullTransform)
                        returnList.append(tmp)
                if fileNodeNormal and not len(fileNodeNormal) > 1:
                    sizeX = cmds.getAttr(fileNodeNormal + ".outSize")[0][0]
                    sizeY = cmds.getAttr(fileNodeNormal + ".outSize")[0][1]
                    if not sizeY <= 4096 and not sizeX <= 4096:
                        tmp = []
                        tmp.append(hullTransform + " - normal texture res: " + str(sizeX).split(".")[0] + "x" +
                                   str(sizeY).split(".")[0] + " is wrong")
                        tmp.append(hullTransform)
                        returnList.append(tmp)

    # check gun
    if gunList:
        gunSG = cmds.listConnections(gunList, type="shadingEngine")
        gunTransform = cmds.listRelatives(gunList, p=1, f=1)[0]
        # print gunSG
        if gunSG:
            for i in gunSG:
                fileNodeColor = None
                fileNodeNormal = None
                try:
                    # fileNodeColor = cmds.listConnections(cmds.listConnections(i + ".surfaceShader")[0] + ".color")
                    # fileNodeNormal = cmds.listConnections(cmds.listConnections(cmds.listConnections(i + ".surfaceShader")[0] + ".normalCamera"), c=0, s=1)
                    fileNodeColorTmp = cmds.listConnections(i + ".surfaceShader")[0]
                    if fileNodeColorTmp:
                        fileNodeColor = cmds.listConnections(fileNodeColorTmp + ".color")

                    fileNodeNormalTmp = cmds.listConnections(i + ".surfaceShader")[0]
                    if fileNodeNormalTmp:
                        fileNodeNormalTmp = cmds.listConnections(fileNodeNormalTmp + ".normalCamera")
                        if fileNodeNormalTmp:
                            fileNodeNormal = cmds.listConnections(fileNodeNormalTmp, c=0, s=1)

                    # print "fileNodeNormal ------ ", fileNodeNormal
                    for j in fileNodeNormal:
                        if cmds.nodeType(j) == "file":
                            fileNodeNormal = j
                            break

                except:
                    pass
                if fileNodeColor:
                    sizeX = cmds.getAttr(fileNodeColor[0] + ".outSize")[0][0]
                    sizeY = cmds.getAttr(fileNodeColor[0] + ".outSize")[0][1]
                    if not sizeY <= 2048 and not sizeX <= 2048:
                        tmp = []
                        tmp.append(
                            gunTransform + " - texture res: " + str(sizeX).split(".")[0] + "x" + str(sizeY).split(".")[
                                0] + " is wrong")
                        tmp.append(gunTransform)
                        returnList.append(tmp)
                if fileNodeNormal and not len(fileNodeNormal) > 1:
                    sizeX = cmds.getAttr(fileNodeNormal + ".outSize")[0][0]
                    sizeY = cmds.getAttr(fileNodeNormal + ".outSize")[0][1]
                    if not sizeY <= 2048 and not sizeX <= 2048:
                        tmp = []
                        tmp.append(gunTransform + " - normal texture res: " + str(sizeX).split(".")[0] + "x" +
                                   str(sizeY).split(".")[0] + " is wrong")
                        tmp.append(gunTransform)
                        returnList.append(tmp)

    # check turret
    if turretList:
        turretSG = cmds.listConnections(turretList, type="shadingEngine")
        turretTransform = cmds.listRelatives(turretList, p=1, f=1)[0]
        if turretSG:
            for i in turretSG:
                fileNodeColor = None
                fileNodeNormal = None
                try:
                    # fileNodeColor = cmds.listConnections(cmds.listConnections(i + ".surfaceShader")[0] + ".color")
                    # fileNodeNormal = cmds.listConnections(cmds.listConnections(cmds.listConnections(i + ".surfaceShader")[0] + ".normalCamera"), c=0, s=1)
                    fileNodeColorTmp = cmds.listConnections(i + ".surfaceShader")[0]
                    if fileNodeColorTmp:
                        fileNodeColor = cmds.listConnections(fileNodeColorTmp + ".color")

                    fileNodeNormalTmp = cmds.listConnections(i + ".surfaceShader")[0]
                    if fileNodeNormalTmp:
                        fileNodeNormalTmp = cmds.listConnections(fileNodeNormalTmp + ".normalCamera")
                        if fileNodeNormalTmp:
                            fileNodeNormal = cmds.listConnections(fileNodeNormalTmp, c=0, s=1)

                    for j in fileNodeNormal:
                        if cmds.nodeType(j) == "file":
                            fileNodeNormal = j
                            break
                except:
                    pass
                if fileNodeColor:
                    sizeX = cmds.getAttr(fileNodeColor[0] + ".outSize")[0][0]
                    sizeY = cmds.getAttr(fileNodeColor[0] + ".outSize")[0][1]
                    if not sizeY <= 2048 and not sizeX <= 2048:
                        tmp = []
                        tmp.append(turretTransform + " - texture res: " + str(sizeX).split(".")[0] + "x" +
                                   str(sizeY).split(".")[0] + " is wrong")
                        tmp.append(turretTransform)
                        returnList.append(tmp)
                if fileNodeNormal and not len(fileNodeNormal) > 1:
                    sizeX = cmds.getAttr(fileNodeNormal + ".outSize")[0][0]
                    sizeY = cmds.getAttr(fileNodeNormal + ".outSize")[0][1]
                    if not sizeY <= 2048 and not sizeX <= 2048:
                        tmp = []
                        tmp.append(turretTransform + " - normal texture res: " + str(sizeX).split(".")[0] + "x" +
                                   str(sizeY).split(".")[0] + " is wrong")
                        tmp.append(turretTransform)
                        returnList.append(turretTransform + " - normal texture res: " + str(sizeX).split(".")[0] + "x" +
                                          str(sizeY).split(".")[0] + " is wrong")

    # check chassis
    if chassisList:
        chassisSG = cmds.listConnections(chassisList, type="shadingEngine")
        chassisTransform = cmds.listRelatives(chassisList, p=1, f=1)[0]
        if chassisSG:
            for i in chassisSG:
                fileNodeColor = None
                fileNodeNormal = None
                try:
                    # fileNodeColor = cmds.listConnections(cmds.listConnections(i + ".surfaceShader")[0] + ".color")
                    # fileNodeNormal = cmds.listConnections(cmds.listConnections(cmds.listConnections(i + ".surfaceShader")[0] + ".normalCamera"), c=0, s=1)
                    fileNodeColorTmp = cmds.listConnections(i + ".surfaceShader")[0]
                    if fileNodeColorTmp:
                        fileNodeColor = cmds.listConnections(fileNodeColorTmp + ".color")

                    fileNodeNormalTmp = cmds.listConnections(i + ".surfaceShader")[0]
                    if fileNodeNormalTmp:
                        fileNodeNormalTmp = cmds.listConnections(fileNodeNormalTmp + ".normalCamera")
                        if fileNodeNormalTmp:
                            fileNodeNormal = cmds.listConnections(fileNodeNormalTmp, c=0, s=1)

                    for j in fileNodeNormal:
                        if cmds.nodeType(j) == "file":
                            fileNodeNormal = j
                            break
                except:
                    pass
                if fileNodeColor:
                    sizeX = cmds.getAttr(fileNodeColor[0] + ".outSize")[0][0]
                    sizeY = cmds.getAttr(fileNodeColor[0] + ".outSize")[0][1]
                    if not sizeY <= 2048 and not sizeX <= 2048:
                        tmp = []
                        tmp.append(chassisTransform + " - texture res: " + str(sizeX).split(".")[0] + "x" +
                                   str(sizeY).split(".")[0] + " is wrong")
                        tmp.append(chassisTransform)
                        returnList.append(tmp)
                if fileNodeNormal and not len(fileNodeNormal) > 1:
                    sizeX = cmds.getAttr(fileNodeNormal + ".outSize")[0][0]
                    sizeY = cmds.getAttr(fileNodeNormal + ".outSize")[0][1]
                    if not sizeY <= 2048 and not sizeX <= 2048:
                        tmp = []
                        tmp.append(chassisTransform + " - normal texture res: " + str(sizeX).split(".")[0] + "x" +
                                   str(sizeY).split(".")[0] + " is wrong")
                        tmp.append(chassisTransform)
                        returnList.append(tmp)

    # check track
    if trackList:
        trackSG = cmds.listConnections(trackList, type="shadingEngine")
        trackTransform = cmds.listRelatives(trackList, p=1, f=1)[0]
        if trackSG:
            for i in trackSG:
                fileNodeColor = None
                fileNodeNormal = None
                try:
                    # fileNodeColor = cmds.listConnections(cmds.listConnections(i + ".surfaceShader")[0] + ".color")
                    # fileNodeNormal = cmds.listConnections(cmds.listConnections(cmds.listConnections(i + ".surfaceShader")[0] + ".normalCamera"), c=0, s=1)
                    fileNodeColorTmp = cmds.listConnections(i + ".surfaceShader")[0]
                    if fileNodeColorTmp:
                        fileNodeColor = cmds.listConnections(fileNodeColorTmp + ".color")

                    fileNodeNormalTmp = cmds.listConnections(i + ".surfaceShader")[0]
                    if fileNodeNormalTmp:
                        fileNodeNormalTmp = cmds.listConnections(fileNodeNormalTmp + ".normalCamera")
                        if fileNodeNormalTmp:
                            fileNodeNormal = cmds.listConnections(fileNodeNormalTmp, c=0, s=1)

                    for j in fileNodeNormal:
                        if cmds.nodeType(j) == "file":
                            fileNodeNormal = j
                            break
                except:
                    pass
                if fileNodeColor:
                    sizeX = cmds.getAttr(fileNodeColor[0] + ".outSize")[0][0]
                    sizeY = cmds.getAttr(fileNodeColor[0] + ".outSize")[0][1]
                    if sizeX == 0.0 and sizeY == 0.0:
                        continue
                    if not sizeX <= 1024 and not sizeX <= 512:
                        tmp = []
                        tmp.append(trackTransform + " - texture res: " + str(sizeX).split(".")[0] + "x" +
                                   str(sizeY).split(".")[0] + " is wrong")
                        tmp.append(trackTransform)
                        returnList.append(tmp)
                    elif not sizeY == 512 and not sizeY == 256:
                        tmp = []
                        tmp.append(trackTransform + " - texture res: " + str(sizeX).split(".")[0] + "x" +
                                   str(sizeY).split(".")[0] + " is wrong")
                        tmp.append(trackTransform)
                        returnList.append(tmp)

                if fileNodeNormal and not len(fileNodeNormal) > 1:
                    sizeX = cmds.getAttr(fileNodeNormal + ".outSize")[0][0]
                    sizeY = cmds.getAttr(fileNodeNormal + ".outSize")[0][1]
                    if sizeX == 0.0 and sizeY == 0.0:
                        continue
                    if not sizeX <= 1024 and not sizeX <= 512:
                        tmp = []
                        tmp.append(trackTransform + " - normal texture res: " + str(sizeX).split(".")[0] + "x" +
                                   str(sizeY).split(".")[0] + " is wrong")
                        tmp.append(trackTransform)
                        returnList.append(tmp)
                    elif not sizeY == 512 and not sizeY == 256:
                        tmp = []
                        tmp.append(trackTransform + " - normal texture res: " + str(sizeX).split(".")[0] + "x" +
                                   str(sizeY).split(".")[0] + " is wrong")
                        tmp.append(trackTransform)
                        returnList.append(tmp)

    if lod4list:
        hullSG = cmds.listConnections(lod4list, type="shadingEngine")
        hullTransform = cmds.listRelatives(lod4list, p=1, f=1)[0]
        if hullSG:
            for i in hullSG:
                fileNodeColor = None
                fileNodeNormal = None
                try:
                    # here we need to get all file nodes connected with the SG

                    fileNodeColorTmp = cmds.listConnections(i + ".surfaceShader")[0]
                    if fileNodeColorTmp:
                        fileNodeColor = cmds.listConnections(fileNodeColorTmp + ".color")

                    fileNodeNormalTmp = cmds.listConnections(i + ".surfaceShader")[0]
                    if fileNodeNormalTmp:
                        fileNodeNormalTmp = cmds.listConnections(fileNodeNormalTmp + ".normalCamera")
                        if fileNodeNormalTmp:
                            fileNodeNormal = cmds.listConnections(fileNodeNormalTmp, c=0, s=1)
                    # fileNodeColor = cmds.listConnections(cmds.listConnections(i + ".surfaceShader")[0] + ".color")
                    # fileNodeNormal = cmds.listConnections(cmds.listConnections(cmds.listConnections(i + ".surfaceShader")[0] + ".normalCamera"), c=0, s=1)

                    for j in fileNodeNormal:
                        if cmds.nodeType(j) == "file":
                            fileNodeNormal = j
                            break

                except:
                    pass
                if fileNodeColor:
                    sizeX = cmds.getAttr(fileNodeColor[0] + ".outSize")[0][0]
                    sizeY = cmds.getAttr(fileNodeColor[0] + ".outSize")[0][1]
                    if not sizeY <= 256 and not sizeX <= 256:
                        tmp = []
                        tmp.append(
                            hullTransform + " - texture res: " + str(sizeX).split(".")[0] + "x" + str(sizeY).split(".")[
                                0] + " is wrong")
                        tmp.append(hullTransform)
                        returnList.append(tmp)
                if fileNodeNormal and not len(fileNodeNormal) > 1:
                    sizeX = cmds.getAttr(fileNodeNormal + ".outSize")[0][0]
                    sizeY = cmds.getAttr(fileNodeNormal + ".outSize")[0][1]
                    if not sizeY <= 256 and not sizeX <= 256:
                        tmp = []
                        tmp.append(hullTransform + " - normal texture res: " + str(sizeX).split(".")[0] + "x" +
                                   str(sizeY).split(".")[0] + " is wrong")
                        tmp.append(hullTransform)
                        returnList.append(tmp)

    return returnList
