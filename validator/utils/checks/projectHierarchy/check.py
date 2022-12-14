import maya.cmds as cmds
import re
import os
import sys
import os.path
from validator.utils.validator_API import *

checkId = 39
checkLabel = "1.4 Check SVN Structure"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    objList = vl_listAllTransforms()
    returnList = []

    try:
        # get file info
        rawFilePath = cmds.file(q=True, exn=True)
        fileName = cmds.file(q=True, sn=True, shn=True)
        filePath = rawFilePath[:len(rawFilePath) - len(fileName)]
        search = fileName.find("_crash")
        Tankname = None
        if search != -1:
            Tankname = fileName[:search]
        else:
            Tankname = fileName[:-3]

        checkStatus = 0

        folderLevel_1 = os.path.abspath(os.path.join(filePath, os.pardir))
        folderLevel_1_fixed = str(folderLevel_1).replace("\\", "/")
        folderLevel_2 = os.path.abspath(os.path.join(folderLevel_1, os.pardir))
        folderLevel_2_fixed = str(folderLevel_2).replace("\\", "/")

        # Check for folders Fin Expor Work
        folderL1 = os.listdir(folderLevel_1_fixed)
        for i in folderL1:
            if i != "Fin" and i != "Export" and i != "Work" and i != ".svn":
                checkStatus = 1

        # Check for the name of folder level2
        folderL2 = os.listdir(folderLevel_2_fixed)
        folderL2List = folderLevel_2_fixed.split('/')
        folderL2Name = folderL2List[-1]
        searchL2 = folderL2Name.find(Tankname)
        if searchL2 != -1:
            pass
        else:
            checkStatus = 2

        # Check for Fin and Export Content
        fldFinList = []
        fldExportList = []

        fldFinPath = folderLevel_1_fixed + "/Fin"

        try:
            fldFinList = os.listdir(fldFinPath)
        except:
            pass

        fldExportPath = folderLevel_1_fixed + "/Export"

        try:
            fldExportList = os.listdir(fldExportPath)
        except:
            pass

        if fldFinList:
            for j in fldFinList:
                fName = j.split('.')
                if fName[1] != "mb" and fName[1] != "tga" and fName[1] != "TGA" and fName[1] != "mayaSwatches":
                    checkStatus = 3

        if fldExportList:
            for k in fldExportList:
                fName = k.split('.')
                if fName[1] != "mb" and fName[1] != "dds" and fName[1] != "DDS" and fName[1] != "mayaSwatches":
                    checkStatus = 4

        errorMessage1 = "Check the Model folder. There are some extra folders"
        errorMessage2 = "Main folder of your project doesn't contain your tank name"
        errorMessage3 = "There are some extra filetypes in the Fin folder"
        errorMessage4 = "There are some extra filetypes in the Export folder"

        if checkStatus == 1:
            tmp = []
            tmp.append(errorMessage1)
            tmp.append(" ")
            returnList.append(tmp)
        if checkStatus == 2:
            tmp = []
            tmp.append(errorMessage2)
            tmp.append(" ")
            returnList.append(tmp)
        if checkStatus == 3:
            tmp = []
            tmp.append(errorMessage3)
            tmp.append(" ")
            returnList.append(tmp)
        if checkStatus == 4:
            tmp = []
            tmp.append(errorMessage4)
            tmp.append(" ")
            returnList.append(tmp)
    except:
        pass

    return returnList
