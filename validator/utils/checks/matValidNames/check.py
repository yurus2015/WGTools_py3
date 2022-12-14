import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 28
checkLabel = "3.1 Check names of materials"


def main():
    validNamesList = vl_tanksMatValidNames()

    matData = listAllMat()
    returnList = []

    # dom didom dom dom - KOSTIL'
    rawFilePath = cmds.file(q=True, exn=True)
    if "G_Tiger" in rawFilePath or "G45_G_Tiger" in rawFilePath:
        return returnList

    for x in range(len(matData)):
        valid = 0
        for y in validNamesList:
            temp = y.search(matData[x])
            if temp != None:
                valid = 1
        if valid == 0:
            tmp = []
            tmp.append(matData[x])
            tmp.append(matData[x])
            returnList.append(tmp)

    for x in validNamesList:
        pattern = x.pattern
        try:
            pattern = pattern.replace('\d', '#')
        except:
            pass
        try:
            pattern = pattern.replace('\Z', '')
        except:
            pass
        try:
            pattern = pattern.replace('^', '')
        except:
            pass
        # helpStringList.append(pattern)

    track_mat = []
    for i in matData:
        if i.find("track_mat") != -1:
            track_mat.append(i)
    if track_mat:
        if not len(track_mat) == 2:
            tmp = []
            tmp.append("The scene has more or less then 2 track_mat materials")
            tmp.append("")
            returnList.append(tmp)
        else:
            if (track_mat[0].find("_L") != -1 and track_mat[1].find("_L") != -1):
                tmp = []
                tmp.append("Both of track_mats have postfix '_L'")
                tmp.append("")
                returnList.append(tmp)

            elif (track_mat[0].find("_R") != -1 and track_mat[1].find("_R") != -1):
                tmp = []
                tmp.append("Both of track_mats have postfix '_R'")
                tmp.append("")
                returnList.append(tmp)

            else:
                pass
    else:
        tmp = []
        tmp.append("There are no track_mat materials in the scene")
        tmp.append("")
        returnList.append(tmp)

    return returnList
