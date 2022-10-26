import maya.cmds as cmds

#from validator.resources.validator_API import *
checkId = 201
checkLabel = "2.2 Check object`s UV sets"

def removeList(fromList, thisList):
	resultList =  [n for n in fromList if n not in thisList]
	resultList = list(resultList)
	return resultList
def removeDupplicateList(currentList):
	resultList = list(set(currentList))
	return resultList

def uvSetsCount(item):
	uvSets = cmds.polyUVSet (item, query = True, allUVSets=True) #get all uvSets
	return uvSets

def uvSetName(uvset):
	if uvset == 'map1' or uvset == 'map2':
		return True
	else:
		return False

def checkNameMesh(item):
	exeptNames = ['_bsp', 'HP', 's_wall', 's_ramp']
	exeptMesh = []
	for name in exeptNames:
		if name in item:
			return True
	return False

def checkPolycountUvset(item, uvset):
	cmds.polyUVSet(item,  currentUVSet=True,  uvSet=uvset)
	faceObj = cmds.ls(item+'.f[*]', fl = True)
	faces_count = len(faceObj)
	faceUVs = cmds.ls(cmds.polyListComponentConversion(cmds.polyListComponentConversion(faceObj, tuv = 1), tf =1), fl =1)
	face_uv_count = len(faceUVs)

	if faceObj != face_uv_count:

		return removeList(faceObj, faceUVs)
	else:
		return None

def main():
	print('<< ' + checkLabel.upper() + ' >>')
	returnList = []

	listAllMesh = cmds.ls(type = 'transform', l=1)
	listAllMesh = cmds.ls(cmds.filterExpand(listAllMesh, sm=12 ), l=1)
	listAllMesh = removeDupplicateList(listAllMesh)
	cmds.undoInfo( state=True, infinity=True )
	for mesh in listAllMesh:
		meshFullName = mesh
		#Horrible Dirty Shit for havok preset
		if "havok" in cmds.file(q=1,sn = 1):
			if "havok" not in mesh.split("|")[1]:
				continue
		# mesh = mesh.split('|')[-1]

		#YURUS Hack
		#find not correct uvset

		trisNode = cmds.polyTriangulate(mesh, ch=1)[0]
		cmds.undo()

		tmp = []
		shortName = mesh.split('|')[-1]
		#print 'SHORT', shortName
		uvsets = uvSetsCount(mesh)
		if checkNameMesh(shortName) == False:

			if len(uvsets) < 3:
				for sets in uvsets:
					if uvSetName(sets) == False:
						tmp.append(mesh + " has uvSet with wrong name")
						tmp.append(mesh)


			if len(uvsets) > 2:
				tmp.append(shortName + " has more than 2 uvSet. Need only two")
				tmp.append(mesh)

			for uvset in uvsets:
				cmds.polyUVSet(mesh, currentUVSet=True,  uvSet=uvset)
				cmds.select(mesh)
				cmds.selectType( pf=True )
				cmds.polySelectConstraint( m=3, t=0x0008, tx=2 ) # to unmaped faces
				unmapp = cmds.ls(sl=1)
				cmds.polySelectConstraint( tx=0 ) # turn off unmaped faces constraint
				cmds.select(d=1)
				if unmapp:
					tmp.append(shortName + " has unmapped faces in " + uvset + " uvSet")
					tmp.append(unmapp)

				perInst = cmds.polyUVSet(mesh, q=1, pi =1, uvSet = uvset)
				if not perInst:
					tmp.append(shortName + " has empty " + uvset + " uvSet")
					tmp.append(mesh)

		else:

			if len(uvsets) > 1:
				tmp.append(shortName + " has more than 1 uvSet. " + shortName + " need only one")
				tmp.append(mesh)



			if uvSetName(uvsets[0]) == False:
				tmp.append(mesh + " has uvSet with wrong name")
				tmp.append(mesh)


		if tmp:
			returnList.append(tmp)


	return returnList

