import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

checkId = 131
checkLabel = "1.16 Check unclean polygons"

def main():
	print('<< ' + checkLabel.upper() + ' >>')
	returnList = []


	meshList = cmds.ls(type="mesh", l=1)
	polyObjList = []
	if meshList:
		polyObjList = cmds.listRelatives(meshList, p=1, f=1)

	for i in polyObjList:
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

		#int pointer
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

			geomIter.numTriangles(numTriPtr)
			realNumTri = OpenMaya.MScriptUtil(numTriPtr).asInt()
			if realNumTri != 1 and "track" not in i:
				list_notTriang.append(i + ".f[" + str(geomIter.index()) + "]")
				triangleCount += 1


			vert_list = OpenMaya.MIntArray()
			geomIter.getVertices(vert_list)
			if vert_list.length() > 4:
				list_ngons.append(i + ".f[" + str(geomIter.index()) + "]")
				ngonsCount += 1

			next(geomIter)


		#result
		#if list_notTriang:
		#    tmp = []
		#    tmp.append(i + " has not triangulated faces")
		#    tmp.append(list_notTriang)
		#    returnList.append(tmp)

		if list_ngons:
			tmp = []
			tmp.append(i + " has NGons")
			tmp.append(list_ngons)
			returnList.append(tmp)


	return returnList


def main_2():

	returnList = []
	it_mesh = OpenMaya.MItDependencyNodes(OpenMaya.MFn.kMesh)

	while not it_mesh.isDone():
		v_pols = []
		v_mesh = []
		mObject = it_mesh.thisNode()

		dag_path = OpenMaya.MDagPath.getAPathTo( mObject )
		mFnMesh = OpenMaya.MFnMesh( dag_path )
		print('name', mFnMesh.name())
		mObject_numFaces = mFnMesh.numPolygons()
		mIntArray = OpenMaya.MIntArray()
		for faceID in range(0, mObject_numFaces ):
			mIntArray.clear()
			mFnMesh.getPolygonVertices( faceID, mIntArray )

			if mIntArray.__len__() > 4:
				if not dag_path.fullPathName() in v_mesh:
					v_mesh.append( dag_path.fullPathName() )
				v_pols.append( '%s.f[%d]' %( dag_path.fullPathName(), faceID ) )
		print('test', v_pols)
		if v_pols:
			tmp = []
			tmp.append("Mesh has NGons")
			tmp.append(v_pols)
			returnList.append(tmp)

		next(it_mesh)

	return returnList
