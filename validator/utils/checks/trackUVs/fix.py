import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

checkId = 112
checkLabel = "4.24 Check onefold track UV scale"


def main(*args):
    searchThreshold = 0.05

    if args:
        for obj in args:
            selectionList = OpenMaya.MSelectionList()
            selectionList.clear()
            selectionList.add(obj)

            DagPath = OpenMaya.MDagPath()
            selectionList.getDagPath(0, DagPath)

            DagNode = OpenMaya.MObject()
            DagNode = DagPath.node()

            fnMesh = OpenMaya.MFnMesh(DagPath)

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

            min_array = []
            max_array = []

            for i in range(vArray.length()):
                if vArray[i] > minV - searchThreshold and vArray[i] < minV + searchThreshold:
                    min_array.append(i)
                elif vArray[i] < maxV + searchThreshold and vArray[i] > maxV - searchThreshold:
                    max_array.append(i)

            maxBorder = 0
            minBorder = 0

            if abs(int(abs(maxV)) - abs(maxV)) < 0.5:
                maxBorder = int(maxV)
            else:
                maxBorder = int(maxV) + (maxV / abs(maxV))

            if abs(int(abs(minV)) - abs(minV)) < 0.5:
                minBorder = int(minV)
            else:
                minBorder = int(minV) + (minV / abs(minV))

            scaleApprox = maxBorder - minBorder

            scaleFactor = scaleApprox / (maxV - minV)

            cmds.polyEditUV(obj + ".map[*]", pu=0, pv=0, su=1, sv=scaleFactor)

            # for i in min_array:
            #     cmds.polyEditUV(obj + ".map[" + str(i) + "]", v = minBorder, r=0)

            # for i in max_array:
            #     cmds.polyEditUV(obj + ".map[" + str(i) + "]", v = maxBorder, r=0)
