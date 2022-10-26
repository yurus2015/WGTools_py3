import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

checkId = 111
checkLabel = "Check N-Gons"

def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []

    itDag = OpenMaya.MItDag(OpenMaya.MItDag.kDepthFirst, OpenMaya.MFn.kTransform)
    while not itDag.isDone():

        #get DAG path
        DagPath = OpenMaya.MDagPath()
        itDag.getPath(DagPath)


        #Get DAG node
        oObj = OpenMaya.MObject()
        oObj = DagPath.node()

        uInt_util = OpenMaya.MScriptUtil(0)
        uInt_ptr = uInt_util.asUintPtr()

        DagPath.numberOfShapesDirectlyBelow(uInt_ptr)

        numShapes = uInt_util.getUint(uInt_ptr)


        if numShapes > 0:

            DagPath.extendToShapeDirectlyBelow(0)

            if( DagPath.hasFn(OpenMaya.MFn.kMesh)):


                component = OpenMaya.MObject()
                polyIter = OpenMaya.MItMeshPolygon(DagPath, component)

                while not polyIter.isDone():
                    vert_list = OpenMaya.MIntArray()
                    polyIter.getVertices(vert_list)
                    if vert_list.length() > 4:
                        id = polyIter.index()
                        tmp = []
                        tmp.append(DagPath.fullPathName()[:len(DagPath.fullPathName()) - len(DagPath.fullPathName().split("|")[-1])-1] + ".f[" + str(id) + "]")
                        tmp.append(DagPath.fullPathName()[:len(DagPath.fullPathName()) - len(DagPath.fullPathName().split("|")[-1])-1] + ".f[" + str(id) + "]")
                        returnList.append(tmp)
                    next(polyIter)



        next(itDag)

    return returnList