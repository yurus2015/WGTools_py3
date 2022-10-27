import maya.cmds as cmds
from maya.mel import eval as meval

# import re
# import os
# import sys

# from validator.utils.validator_API import *
# checkId = 10
checkLabel = "Lost Nodes"

LOST_NODES = ['materialInfo', 'groupId', 'hyperLayout', 'nodeGraphEditorInfo', 'renderLayerManager']


def main():
    returnList = []

    for node in LOST_NODES:
        nodes = cmds.ls(type=node)
        tmp = []
        lost_nodes = []
        for n in nodes:
            if ':' in n:
                lost_nodes.append(n)
        if lost_nodes:
            tmp.append('Lost nodes: {}'.format(node))
            tmp.append(lost_nodes)
            returnList.append(tmp)

    if returnList:
        cmds.outlinerEditor('outlinerPanel1', edit=True, showDagOnly=False)
        meval('showMinorNodes true;')

    return returnList


def main_():
    objList = vl_listAllTransforms()
    returnList = []

    rawFilePath = cmds.file(q=True, exn=True)

    name = rawFilePath.split("/")
    name = name[-1]

    if name == "untitled":
        errorMessage = "Save your file with the tank name!"
        tmp = []
        tmp.append(errorMessage)
        tmp.append("")
        returnList.append(tmp)
    else:
        fileName = cmds.file(q=True, sn=True, shn=True)
        filePath = rawFilePath[:len(rawFilePath) - len(fileName)]
        search = fileName.find("_crash")
        Tankname = None
        if search != -1:
            Tankname = fileName[:search]

        else:
            Tankname = fileName[:-3]

        checkStatus = 0
        folderArray = filePath.split('/')[0:-1]
        for fld in folderArray:
            check = fld.find(Tankname)
            if check != -1:  # If file name was found in the name of directory
                checkStatus = 1
                break

        if checkStatus != 1:
            errorMessage = "The name of your file is incorrect. Check and fix the name of your file"
            tmp = []
            tmp.append(errorMessage)
            tmp.append("")
            returnList.append(tmp)

    return returnList
