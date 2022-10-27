import maya.cmds as cmds
import re
import os
from os.path import isfile, join
import maya.OpenMaya as OpenMaya
from maya.mel import eval as meval
import struct
from validator.utils.validator_API import *

checkId = 44
checkLabel = "Check texture propierties"


def removeList(fromList, thisList):
    resultList = [n for n in fromList if n not in thisList]
    resultList = list(resultList)
    return resultList


def filePath():
    rawFilePath = cmds.file(q=True, exn=True)
    return rawFilePath


def original_tank_name(filePath):
    name = cmds.file(q=True, sn=True, shn=True)
    short_name = os.path.splitext(name)[0]

    # words = filePath.split('/')
    # name = words[-1].split('.')
    # s_name = name[0]
    if 'crash' in short_name.lower():
        short_name = short_name.split('_crash')[0]
    # short_name = c_name[0]

    return short_name


def extensionFile(filePath):
    words = filePath.split('/')
    ext = words[-1].split('.')
    return ext[1]


def validFinFolder(filePath):
    if '/Fin/' in filePath.lower():
        return True
    else:
        return None


def validCrashName(filePath):
    if '_crash' in filePath:
        return True
    else:
        return None


def validHullName(filePath):
    if 'hull' in filePath:
        return True
    else:
        return None


def validShaderName(filePath):
    # texturesList = []
    if '_NM' not in filePath and '_GM' not in filePath and '_AM' not in filePath and '_AO' not in filePath and '_MM' not in filePath and '_CM' not in filePath and 'ShadowMap' not in filePath:
        return filePath


def originalFolderPath(filePath):
    shortName = original_tank_name(filePath)
    # path without name
    path = filePath.split(shortName + '.mb')
    for file in os.listdir(path[0]):
        if file == "Original_textures" or file == "original_textures" or file == "Original_Textures" or file == "original_Textures":
            # isFin = True
            originalPath = path[0] + file + "/"
            return originalPath


def textureList(origPath):
    onlyfiles = []
    # from os.path import isfile, join
    onlyfiles = [f for f in os.listdir(origPath) if isfile(join(origPath, f))]
    # print onlyfiles
    # for file in os.listdir(origPath):
    # if file.endswith(".tga") or file.endswith(".dds"):
    # texturesList.append(file)
    return onlyfiles


def imageSize(filePath):
    ext = extensionFile(filePath)
    with open(filePath) as input:
        h = -1
        w = -1
        if ext == 'tga':
            data = input.read(25)
            w = struct.unpack("h", data[12:14])
            h = struct.unpack("h", data[14:16])
        if ext == 'dds':
            data = input.read(25)
            w = struct.unpack("i", data[16:20])
            h = struct.unpack("i", data[12:16])

        Width = int(w[0])
        Height = int(h[0])
        return Width, Height


def texturesSorting(path, shortFileName, currentPresetNameForChecking):
    # meval("global string $validatorPresetName")
    # currentPresetNameForChecking = meval("$tempVar = $validatorPresetName")
    returnList = []
    validExt = []
    invalidShader = []
    textures = textureList(path)
    currentFileName = cmds.file(q=1, sn=1, shn=1)
    # shortFileName = original_tank_name(currentFilePath)

    # check extension
    if textures:
        for t in textures:
            ext = extensionFile(t)
            # if currentPresetNameForChecking = 'Outsource':
            #	if ext=='tga':
            #		validExt.append(t)

            if ext == 'tga' or ext == 'dds':
                validExt.append(t)
            else:

                tmp = []
                if t != currentFileName:
                    #	pass
                    # else:
                    tmp.append(str(t) + " - not valid extension (only .tga or .dds)")
                    tmp.append(t)
                    returnList.append(tmp)
    # check shader type
    # print 'VALID', validExt
    if validExt:
        textures = validExt
        for t in textures:
            invalid = validShaderName(t)
            if invalid:
                invalidShader.append(invalid)
                tmp = []
                tmp.append(str(t) + " - not valid type (NM, MM, AO, GM etc)")
                tmp.append(t)
                returnList.append(tmp)
    if invalidShader:
        validExt = removeList(validExt, invalidShader)

    # check correct name by tank
    # print 'TEXTURES0', validExt
    if validExt:
        for t in validExt:
            invalid = []

            if shortFileName not in t:
                invalid.append(t)
                tmp = []
                tmp.append(str(t) + " - not valid name (exm: " + shortFileName + "_hull_01_NM)")
                tmp.append(t)
                returnList.append(tmp)
        if invalid:
            validExt = removeList(validExt, invalid)

    # check size proportion
    # print 'TEXTURES', validExt
    if validExt:
        for t in validExt:

            w, h = imageSize(path + t)
            invalid = []
            if (w == 256 or w == 512 or w == 1024 or w == 2048 or w == 4096) and (
                    h == 256 or h == 512 or h == 1024 or h == 2048 or h == 4096):
                continue
            else:
                invalid.append(t)
                tmp = []
                tmp.append(str(t) + " - not valid size value (width = " + str(w) + ", heght = " + str(h) + ")")
                tmp.append(t)
                returnList.append(tmp)
        if invalid:
            validExt = removeList(validExt, invalid)

    # check size-name
    if validExt:
        for t in validExt:
            w, h = imageSize(path + t)
            maxTxt = w
            if h > w:
                maxTxt = h

            invalid = []
            if 'guns' in t and 'CM' not in t and maxTxt != 2048:
                invalid.append(t)
            # print 'I AM HERE', t
            if 'guns' in t and 'CM' in t and maxTxt != 1024:
                invalid.append(t)

            if 'turret' in t and 'CM' not in t and not maxTxt == 2048:
                invalid.append(t)
            if 'turret' in t and 'CM' in t and not maxTxt == 1024:
                invalid.append(t)

            if 'hull' in t and 'CM' not in t and not maxTxt == 4096:
                invalid.append(t)
            if 'hull' in t and 'CM' in t and not maxTxt == 2048:
                invalid.append(t)

            if 'chassis' in t and 'CM' not in t and not maxTxt == 2048:
                invalid.append(t)

            if invalid:
                for i in invalid:
                    tmp = []
                    tmp.append(str(t) + " - not valid texture SIZE for current type")
                    tmp.append(t)

                    returnList.append(tmp)
    return returnList


def main():
    returnList = []
    # validExt = []
    # invalidShader = []
    meval("global string $validatorPresetName")
    currentPresetNameForChecking = meval("$tempVar = $validatorPresetName")
    print(currentPresetNameForChecking)
    # name of maya file
    currentFilePath = filePath()
    # print 'FILE PATH', currentFilePath

    ########################### OUTSOURCE PRESET
    if currentPresetNameForChecking == 'Outsource':

        tankName = original_tank_name(currentFilePath)
        shortName = cmds.file(q=1, sn=1, shn=1)

        # print 'NAME', shortName+'.mb'
        path = currentFilePath.split(shortName)
        # print 'OUT', path, path[0]

        returnList = texturesSorting(path[0], tankName, currentPresetNameForChecking)
    ############################ TANKS PRESET
    else:
        # fin folder or not
        # print 'NOT OUTSOURCE'
        if validFinFolder(currentFilePath):
            # short name
            # print 'Current Path', validFinFolder(currentFilePath)

            shortFileName = original_tank_name(currentFilePath)

            # original textures folder

            try:
                originalFolder = originalFolderPath(currentFilePath)
            # print 'ORIG FOLDER', originalFolder
            except:
                return returnList

            if originalFolder:
                returnList = texturesSorting(originalFolder, shortFileName, currentPresetNameForChecking)
    # textures = textureList(originalFolder)

    return returnList


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


def texturesSizeCheck():
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

                    super = list(set(proportions))
                    if len(super) > 1:
                        for x in i:
                            tmp = []
                            tmp.append(x)
                            tmp.append(x)
                            returnList.append(tmp)

    return returnList
