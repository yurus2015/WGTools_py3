import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import re
import os
checkId = 110
checkLabel = "Check TGA textures"

def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []

    rawFilePath = cmds.file (q=True, exn=True)
    fileName = cmds.file(q=True, sn=True, shn=True)
    filePath = None
    if fileName:
        fileNameFrmt = fileName.split(".")[0]
        ext = fileName.split(".")[-1]
        filePath = rawFilePath[:len(rawFilePath) - len(fileName)]
        search =  fileName.find("_crash")
        Tankname = None
        if search != -1:
            Tankname = fileName[:search]

        else:
            Tankname = fileName[:-3]


    file_list = cmds.ls(type="file", l=1)
    for i in file_list:
        txt = cmds.getAttr(i + ".fileTextureName")
        if txt:
            if txt.split(".")[-1] != "tga" and txt.split(".")[-1] != "TGA":
                tmp = []
                tmp.append(i + " node has a wrong texture format assigned")
                tmp.append(i)
                returnList.append(tmp)

    if filePath:
        isFin = False
        origTxtName = ""
        for file in os.listdir(filePath):
            if file == "Original_textures" or file == "original_textures" or file == "Original_Textures" or file == "original_Textures":
                origTxtName = file
                isFin = True
                filePath = filePath + "/" + file + "/"
                break

        if isFin:
            for txt in os.listdir(filePath):
                if txt == ".mayaSwatches":
                    import shutil
                    shutil.rmtree(filePath + txt)
                    continue

                if "shadow" not in txt and "Shadow" not in txt:
                    if txt.split(".")[-1] != "tga" and txt.split(".")[-1] != "TGA":
                        tmp = []
                        tmp.append("Original_Textures folder contants texture files with a wrong format")
                        tmp.append(txt)
                        returnList.append(tmp)

    return  returnList