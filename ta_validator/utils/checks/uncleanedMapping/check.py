import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

checkId = 131
checkLabel = "1.16 Check unclean mapping"

def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []

    meshList = cmds.ls(type="mesh", l=1)
    polyObjList = []
    if meshList:
        polyObjList = cmds.listRelatives(meshList, p=1, f=1)

    for i in polyObjList:

        #Horrible Dirty Shit for havok preset
        if "havok" in cmds.file(q=1,sn = 1):
            if "havok" not in i.split("|")[1]:
                continue


        selectionList = OpenMaya.MSelectionList()
        selectionList.clear()
        selectionList.add(i)

        #get dag and mobject
        DagPath = OpenMaya.MDagPath()
        mObj = OpenMaya.MObject()
        selectionList.getDagPath(0, DagPath, mObj)

        component = OpenMaya.MObject()

        #iterate
        try:
            geomIter = OpenMaya.MItMeshPolygon(DagPath, component)
        except:
            continue

        # int pointer
        numTri = OpenMaya.MScriptUtil()
        numTri.createFromInt(0)
        numTriPtr = numTri.asIntPtr()

        #create double pointer
        number = OpenMaya.MScriptUtil()
        number.createFromDouble(0.0)
        numPointer = number.asDoublePtr()

        numberUV = OpenMaya.MScriptUtil()
        numberUV.createFromDouble(0.0)
        numUVPointer = numberUV.asDoublePtr()


        areaTolerance = 0.0
        areaUVTolerance = 0.00000001

        triangleCount = 0
        ngonsCount = 0
        zeroAreaCount = 0
        zeroUVAreaCount = 0

        list_notTriang = []
        list_ngons = []
        list_zeroFace = []
        list_zeroUV = []

        while not geomIter.isDone():
            id = geomIter.index() #face ID

            # geomIter.numTriangles(numTriPtr)
            # realNumTri = OpenMaya.MScriptUtil(numTriPtr).asInt()
            # if realNumTri != 1 and "track" not in i:
            #     list_notTriang.append(i + ".f[" + str(geomIter.index()) + "]")
            #     triangleCount += 1
            #     # tmp = []
            #     # tmp.append(DagPath.fullPathName()[:len(DagPath.fullPathName()) - len(DagPath.fullPathName().split("|")[-1])-1] + ".f[" + str(id) + "] - is not triangulated")
            #     # tmp.append(DagPath.fullPathName()[:len(DagPath.fullPathName()) - len(DagPath.fullPathName().split("|")[-1])-1] + ".f[" + str(id) + "]")
            #     # returnList.append(tmp)

            # vert_list = OpenMaya.MIntArray()
            # geomIter.getVertices(vert_list)
            # if vert_list.length() > 4:
            #     list_ngons.append(i + ".f[" + str(geomIter.index()) + "]")
            #     ngonsCount += 1
            #     # tmp = []
            #     # tmp.append(DagPath.fullPathName()[:len(DagPath.fullPathName()) - len(DagPath.fullPathName().split("|")[-1])-1] + ".f[" + str(id) + "] - is NGon")
            #     # tmp.append(DagPath.fullPathName()[:len(DagPath.fullPathName()) - len(DagPath.fullPathName().split("|")[-1])-1] + ".f[" + str(id) + "]")
            #     # returnList.append(tmp)


            geomIter.getArea(numPointer, OpenMaya.MSpace.kWorld)
            resultArea = OpenMaya.MScriptUtil(numPointer).asDouble()
            if resultArea <= areaTolerance:
                list_zeroFace.append(i + ".f[" + str(geomIter.index()) + "]")
                zeroAreaCount += 1

            #UV area
            geomIter.getUVArea(numUVPointer)
            resultArea = OpenMaya.MScriptUtil(numUVPointer).asDouble()
            if geomIter.hasUVs():
                if "lod3" not in i and "lod4" not in i:
                    if resultArea <= areaUVTolerance:
                        list_zeroUV.append(i + ".f[" + str(geomIter.index()) + "]")
                        zeroUVAreaCount += 1
            else:
                list_zeroUV.append(i + ".f[" + str(geomIter.index()) + "]")
                zeroUVAreaCount += 1

            # <_end_>
            next(geomIter)

        # if triangleCount:
        #     tmp = []
        #     tmp.append(i + " has not triangulated faces")
        #     tmp.append(list_notTriang)
        #     returnList.append(tmp)

        # if ngonsCount:
        #     tmp = []
        #     tmp.append(i + " has NGons")
        #     tmp.append(list_ngons)
        #     returnList.append(tmp)

        if zeroAreaCount:
            tmp = []
            tmp.append(i + " has faces with zero area")
            tmp.append(list_zeroFace)
            returnList.append(tmp)

        if zeroUVAreaCount:
            tmp = []
            tmp.append(i + " has faces with zero UV area")
            tmp.append(list_zeroUV)
            returnList.append(tmp)


    return returnList
