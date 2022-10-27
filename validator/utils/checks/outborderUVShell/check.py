import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

checkId = 108
checkLabel = "Check UV Shells out of UV border"


def main():
    returnList = []

    # meshList = cmds.ls(type="mesh", l=1)
    # polyObjList = []
    # if meshList:
    #     polyObjList = cmds.listRelatives(meshList, p=1, f=1)

    # areaTolerance = 0.0

    # for w in polyObjList:
    #     #add current object to the selection list
    #     MSelection  = OpenMaya.MSelectionList()
    #     MSelection.clear()
    #     MSelection.add(w)

    #     #convert selection list to Mobject and get its DagPath
    #     dagPath = OpenMaya.MDagPath()
    #     mObject = OpenMaya.MObject()
    #     MSelection.getDagPath(0,dagPath, mObject)

    #     #apply MFnMesh to our object to use mesh function set
    #     fnMesh = OpenMaya.MFnMesh(dagPath)

    #     #create a pointer to int data
    #     shells = OpenMaya.MScriptUtil()
    #     shells.createFromInt(0)
    #     shellsPtr = shells.asUintPtr()

    #     #put UV IDs by their shell into array
    #     uvShellArray = OpenMaya.MIntArray()
    #     fnMesh.getUvShellsIds(uvShellArray, shellsPtr)

    #     numOfShells =  shells.getUint(shellsPtr)
    #     shellIDs = list(set(uvShellArray))

    #     uvsShellsList = []
    #     for i in shellIDs:
    #         temp = []
    #         for indexUV,j in enumerate(uvShellArray):
    #             if j == i:
    #                 temp.append(w + ".map[" + str(indexUV) + "]")

    #         uvsShellsList.append(temp)

    #         #for each uv in the current shell
    #         numUVsInTheShell = len(temp)

    #         uvCoord = []
    #         outsideUCoord = []
    #         outsideVCoord = []

    #         for k in temp: #for uv in shell
    #             # curUVIndex = int(k[-2]) #get index
    #             curUVIndex = k.split(".map[")[-1]
    #             curUVIndex = int(curUVIndex.split("]")[0])

    #             u_util = OpenMaya.MScriptUtil(0.0) #get coords
    #             u_ptr = u_util.asFloatPtr()
    #             v_util = OpenMaya.MScriptUtil(0.0)
    #             v_ptr = v_util.asFloatPtr()
    #             fnMesh.getUV(curUVIndex, u_ptr, v_ptr)
    #             uResult =  u_util.getFloat(u_ptr)
    #             vResult =  v_util.getFloat(v_ptr)

    #             tmpCoord = [] #save coords
    #             tmpCoord.append(uResult)
    #             tmpCoord.append(vResult)
    #             uvCoord.append(tmpCoord)

    #             if uResult >= 1 or uResult <= 0: #if uv outside u
    #                 outsideUCoord.append(k)

    #             if vResult >= 1 or vResult <= 0: #if uv outside v
    #                 outsideVCoord.append(k)

    #         # print  numUVsInTheShell, len(outsideUCoord)
    #         # print uvCoord
    #         # print temp

    #         if len(outsideUCoord) == numUVsInTheShell:
    #             tmp = []
    #             tmp.append(w)
    #             tmp.append(w)
    #             returnList.append(tmp)
    #         elif len(outsideVCoord) == numUVsInTheShell:
    #             tmp = []
    #             tmp.append(w)
    #             tmp.append(w)
    #             returnList.append(tmp)

    return returnList
