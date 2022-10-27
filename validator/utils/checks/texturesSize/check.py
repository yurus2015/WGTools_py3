import maya.cmds as cmds
import re
import os
import maya.OpenMaya as OpenMaya
import struct
from validator.utils.validator_API import *

checkId = 44
checkLabel = "Check texture proportions"


def get_image_size(file_path, filename):
    size = os.path.getsize(file_path)
    fileName, ext = os.path.splitext(filename)
    if ext == '.tga' or ext == '.dds':
        with open(file_path) as input:
            h = -1
            w = -1
            if ext == '.tga':
                data = input.read(25)
                w = struct.unpack("h", data[12:14])
                h = struct.unpack("h", data[14:16])
            if ext == '.dds':
                data = input.read(25)
                w = struct.unpack("i", data[16:20])
                h = struct.unpack("i", data[12:16])

        Width = int(w[0])
        Height = int(h[0])
        return Width, Height
    else:
        print("This is not TGA or DDS file")


def main():
    returnList = []
    texturesList = []

    rawFilePath = cmds.file(q=True, exn=True)
    fileName = cmds.file(q=True, sn=True, shn=True)
    if fileName:
        fileNameFrmt = fileName.split(".")[0]
        ext = fileName.split(".")[-1]
        filePath = rawFilePath[:len(rawFilePath) - len(fileName)]
        search = fileName.find("_crash")
        Tankname = None
        if search != -1:
            Tankname = fileName[:search]

        else:
            Tankname = fileName[:-3]

        # check if it has original_textures in the scene folder
        isFin = False
        for file in os.listdir(filePath):
            if file == "Original_textures" or file == "original_textures" or file == "Original_Textures" or file == "original_Textures":
                isFin = True
                filePath = filePath + "/" + file + "/"
                break

        try:
            for file in os.listdir(filePath):
                if file.endswith(".tga") or file.endswith(".dds"):
                    texturesList.append(file)
        # print file[:-4]
        except:
            pass

        textGrplist = []
        if texturesList:
            for x in texturesList:
                grpList = []
                if x.find("crash") == -1:
                    txtName = x.split(".")[0]
                    postfixLen = len(txtName.split("_")[-1])
                    grpName = txtName[:-postfixLen]

                    for i in texturesList:
                        if i.find(grpName) != -1:
                            grpList.append(i)

                    for i in grpList:
                        texturesList.remove(i)
                    textGrplist.append(grpList)

            # print fileName, ext, filePath
            if textGrplist:
                for i in textGrplist:
                    proportions = []
                    for x in i:

                        W = 0
                        H = 0
                        txtExt = x.split(".")[-1]
                        txtShortName = x.split(".")[0]

                        if txtExt == 'tga' or txtExt == 'dds':
                            W, H = get_image_size(filePath + x, x)
                            proportions.append(W / H)
                    # print x
                    # txtPath = filePath + x
                    # mimage = OpenMaya.MImage()
                    # mimage.readFromFile(txtPath)
                    # wScriptUtil = OpenMaya.MScriptUtil()
                    # widthPtr = wScriptUtil.asUintPtr()
                    # hScriptUtil = OpenMaya.MScriptUtil()
                    # heightPtr = hScriptUtil.asUintPtr()
                    # wScriptUtil.setUint(widthPtr, 0)
                    # hScriptUtil.setUint(heightPtr, 0)
                    # mimage.getSize(widthPtr, heightPtr)
                    # width = wScriptUtil.getUint(widthPtr)
                    # height = hScriptUtil.getUint(heightPtr)
                    # #a = cmds.vGetTxtrInfo(p = txtPath)
                    # proportions.append(width/height)

                    super = list(set(proportions))
                    if len(super) > 1:
                        for x in i:
                            tmp = []
                            tmp.append(x)
                            tmp.append(x)
                            returnList.append(tmp)

    return returnList
