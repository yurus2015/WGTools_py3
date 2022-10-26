import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

checkId = 130
checkLabel = "4.23 Check phantom UVs"

def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []

    itDag = OpenMaya.MItDag(OpenMaya.MItDag.kDepthFirst, OpenMaya.MFn.kTransform)

    while not itDag.isDone():
        DP  = OpenMaya.MDagPath()
        itDag.getPath(DP)
        DN = DP.node()



        if DP.childCount() > 0:
            fnDagNode = OpenMaya.MFnDagNode(DP)
            child = fnDagNode.child(0)
            if child.apiTypeStr() == "kMesh":

                #<py>
                objPath = DP.fullPathName()
                objVtx = cmds.ls(cmds.polyListComponentConversion(objPath, tv=1), l=1, fl=1)
                objUVs = cmds.ls(cmds.polyListComponentConversion(objVtx, tuv=1), l=1, fl=1)
                correctNumUVs = len(objUVs)
                #</py>

                fnMesh = OpenMaya.MFnMesh(DP)
                actualNumUVs = fnMesh.numUVs()

                if not actualNumUVs == correctNumUVs:

                    tmp = []
                    tmp.append(objPath)
                    tmp.append(objPath)
                    returnList.append(tmp)




        next(itDag)


    #get through all transforms polygons and get UV count info

    return returnList
