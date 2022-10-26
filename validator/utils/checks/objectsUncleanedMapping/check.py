import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

checkId = 1311
checkLabel = "2.12 Check unclean mapping"

AREA_UV_TOLERANCE = 0.00000001
AREA_TOLERANCE = 0.0

def removeDupplicateList(currentList):
	resultList = list(set(currentList))
	return resultList


def main():
	print('<< ' + checkLabel.upper() + ' >>')
	returnList = []

	meshList = cmds.ls(type="mesh", l=1)
	polyObjList = []
	if meshList:
		polyObjList = cmds.listRelatives(meshList, p=1, f=1)
		polyObjList = removeDupplicateList(polyObjList)

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

		number = OpenMaya.MScriptUtil()
		number.createFromDouble(0.0)
		numPointer = number.asDoublePtr()
		numberUV = OpenMaya.MScriptUtil()
		numberUV.createFromDouble(0.0)
		numUVPointer = numberUV.asDoublePtr()

		zeroAreaCount = 0
		zeroUVAreaCount = 0
		emptyUVAreaCount = 0

		list_zeroFace = []
		list_zeroUV = []
		list_emptyUV = []
		while not geomIter.isDone():
			id = geomIter.index() #face ID
			geomIter.getArea(numPointer, OpenMaya.MSpace.kWorld)
			resultArea = OpenMaya.MScriptUtil(numPointer).asDouble()
			if resultArea <= AREA_TOLERANCE:
				list_zeroFace.append(i + ".f[" + str(geomIter.index()) + "]")
				zeroAreaCount += 1
			#UV area
			geomIter.getUVArea(numUVPointer)
			resultArea = OpenMaya.MScriptUtil(numUVPointer).asDouble()
			if geomIter.hasUVs():
				if "lod3" not in i and "lod4" not in i:
					if resultArea <= AREA_UV_TOLERANCE:
						list_zeroUV.append(i + ".f[" + str(geomIter.index()) + "]")
						zeroUVAreaCount += 1
			else:
				list_emptyUV.append(i + ".f[" + str(geomIter.index()) + "]")
				emptyUVAreaCount += 1
			# <_end_>
			next(geomIter)

		if zeroAreaCount:
			tmp = []
			tmp.append(i + " has faces with zero area")
			tmp.append(list_zeroFace)
			returnList.append(tmp)

		if zeroUVAreaCount:
			if 'HP_' in i or 's_wall' in i or '_bsp' in i or '_ramp' in i:
				pass
			else:
				tmp = []
				tmp.append(i + " has faces with zero or very small UV area")
				tmp.append(list_zeroUV)
				returnList.append(tmp)

		if emptyUVAreaCount:
			if 'HP_' in i or 's_wall' in i or '_ramp' in i:
				pass
			else:
				tmp = []
				tmp.append(i + " has faces without UV")
				tmp.append(list_emptyUV)
				returnList.append(tmp)

	return returnList
