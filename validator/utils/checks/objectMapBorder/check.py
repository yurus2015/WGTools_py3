import maya.cmds as cmds
from maya.mel import eval as meval


checkId = 189
checkLabel = "Check correct smooth group for map borders"

def removeList(fromList, thisList):
	resultList =  [n for n in fromList if n not in thisList]
	resultList = list(resultList)
	return resultList

def intersectionList(oneList, secondList):
	intersect = set(oneList).intersection( set(secondList) )
	intersect = list(intersect)
	return intersect

def removeDupplicateList(currentList):
	resultList = list(set(currentList))
	return resultList

def loadPlugin():

	try:
		cmds.loadPlugin('techartAPI')
	except:
		print("Can`t load techartAPI plugin")


def main():
	print('<< ' + checkLabel.upper() + ' >>')
	loadPlugin()
	meshList = cmds.ls(type="mesh", l=1)
	polyObjList = []
	if meshList:
		polyObjList = cmds.listRelatives(meshList, p=1, f=1)
		polyObjList = removeDupplicateList(polyObjList)

	returnList = []
	if polyObjList:

		for obj in polyObjList:
			cmds.select(obj)

			#fix two uv-sets bag
			uvSets = cmds.polyUVSet (obj, query = True, allUVSets=True) #get all uvSets
			if uvSets:
				if len(uvSets) > 1:
					cmds.polyUVSet(obj,  currentUVSet=True,  uvSet='map1')

			#fix none polygons in current uv-set
			uvs = cmds.ls(obj +'.map[*]', fl = True)
			uvset_faces = cmds.polyListComponentConversion(uvs, fuv=True, tf=True )
			uvset_faces = cmds.ls(uvset_faces, fl =1)
			real_faces = cmds.ls(obj +'.f[*]', fl = True)

			if len(uvset_faces) != len(real_faces):
				continue

			#border edges
			borderEdges = []
			#borderEdges = meval('selectUVBorderEdge -uve')

			#'''
			#print 'BEFORE PLUGIN'
			try:
				borderEdges = meval('selectUVBorderEdge -uve')
			except:
				return returnList
			#'''
			#print 'AFTER PLUGIN'

			cmds.polySelectConstraint( m=3, t=0x8000, sm=2 ) # to get soft edges
			softEdges = cmds.ls(sl=True, fl =1)
			cmds.polySelectConstraint(sm =0)
			cmds.polySelectConstraint(m =0)
			#cmds.polySelectConstraint(disable =1)

			cmds.polySelectConstraint(m=3, t=0x8000, sm=1, w=2 ) # to get hard edges
			hardEdges = cmds.ls(sl=True, fl =1)

			cmds.polySelectConstraint(sm =0, w=0)
			cmds.polySelectConstraint(m =0)
			#cmds.polySelectConstraint(disable =1)
			if borderEdges:
				mustHard = intersectionList(softEdges, borderEdges)
				# if mustHard:
				# 	tmp = []
				# 	tmp.append(obj + " - map border edges should be hard (not always)")
				# 	tmp.append(mustHard)
				# 	returnList.append(tmp)

			if hardEdges:
				mustSplit = removeList(hardEdges, borderEdges)
				if mustSplit:
					tmp = []
					tmp.append(obj + " - hard edges should be split in UV (not always)")
					tmp.append(mustSplit)
					returnList.append(tmp)
	cmds.select(d=1)
	return returnList



