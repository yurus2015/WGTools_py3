import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

checkId = 112
checkLabel = "4.19 Correct UV-mapping of in-game track belts"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []
    Tolerance = 0.002

    #if its not a crush scene
    rawFilePath = cmds.file (q=True, exn=True)
    fileName = cmds.file(q=True, sn=True, shn=True)
    if not"crash" in fileName:

        track_list = []
        track_list = cmds.ls("*track*", l=1, type="transform")
        selectionList = OpenMaya.MSelectionList()
        for i in track_list:
            if cmds.listRelatives(i, type="mesh", f=1):
                selectionList.add(i)

        iter = OpenMaya.MItSelectionList(selectionList)

        while not iter.isDone():

            DP = OpenMaya.MDagPath()
            iter.getDagPath(DP)
            # print DP.fullPathName()
            fnMesh = OpenMaya.MFnMesh(DP)
            uArray = OpenMaya.MFloatArray()
            vArray = OpenMaya.MFloatArray()

            fnMesh.getUVs(uArray, vArray)

            minV = 1
            maxV = 0

            for i in range(vArray.length()):
                if vArray[i] < minV:
                    minV = vArray[i]
                if vArray[i] > maxV:
                    maxV = vArray[i]

            length = maxV - minV
            length = round(length, 3)
            decimal = float("0." + str(length).split(".")[-1])
            actual = int(str(length).split(".")[0])
            actualUpper = actual + 1

            if actualUpper - decimal < actualUpper - Tolerance:
                tmp = []
                tmp.append(DP.fullPathName() + " UVs must have " + str(float(actual)) + " or " + str(float(actual + 1)) +  " of V scale")
                tmp.append(DP.fullPathName())
                returnList.append(tmp)

            next(iter)

    return returnList