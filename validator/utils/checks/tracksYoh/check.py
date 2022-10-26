import maya.cmds as cmds
import re
import maya.OpenMaya as OpenMaya
import itertools
#list all tracks by name
#divide tracks by side
###bounding box
###center bounding box
###sort by y-size and z-pivot position: least by Y has 0-index

def removeList(fromList, thisList):
	resultList =  [n for n in fromList if n not in thisList]
	resultList = list(resultList)
	return resultList


def valid_lods():
	patern_lod = re.compile('lod[0-3]$')
	lods_group = cmds.ls('lod*', tr=1)
	lods = []
	for lod in lods_group:
		if patern_lod.findall(lod):
			lods.append(lod)

	return lods


def all_tracks(lod):
	pattern_track = re.compile('track_[LR]')
	tracks_in_lod = []
	# for lod in lods:
	transforms = cmds.listRelatives(lod, ad=1, type = 'transform', f=1)
	for transform in transforms:
		if pattern_track.findall(transform):
			tracks_in_lod.append(transform)

	if len(tracks_in_lod) < 3:
		return None
	else:
		return tracks_in_lod


def bounding_box(track):
	center = cmds.getAttr(track+'.center')[0]
	size = cmds.getAttr(track+'.boundingBoxSize')[0]
	return center, size


def side_track(tracks):

	left = []
	right = []
	for track in tracks:
		print('T', track)
		center, size = bounding_box(track)
		if center[0] > 0.0:
			right.append([track, size[1], center[2]])
		else:
			left.append([track, size[1], center[2]])

	left = sorted(left, key=lambda x: x[1])
	right= sorted(right, key=lambda x: x[1])

	print('L ', left)
	return left, right


def included_tracks(tracks):
	for a, b in itertools.combinations(tracks, 2):
		print(a, ' | ', b)

	for track in tracks:
		center, size = bounding_box(track)


def getDagPath( name ):
	selectionList = OpenMaya.MSelectionList()
	selectionList.add( name )
	dagPath = OpenMaya.MDagPath()
	selectionList.getDagPath( 0, dagPath )
	return dagPath


def intersection(track, center):
	# center, size = bounding_box(track)
	mesh = OpenMaya.MFnMesh(getDagPath(track))
	sourcePt = OpenMaya.MFloatPoint(center[0]*100,center[1]*100,center[2]*100)
	directionVec = OpenMaya.MFloatVector(0,-1.0,0)
	hitPtArray = OpenMaya.MFloatPointArray()
	max_distance = 9999999999
	hit = mesh.allIntersections(sourcePt,directionVec,None,None,False,OpenMaya.MSpace.kWorld,max_distance,False,None,True,hitPtArray,None,None,None,None,None,0.0001)
	print('HIT: ', hit)
	return hit

	# source_pnt = OpenMaya.MPoint(center[0],center[1],center[2])
	# ray_dir = OpenMaya.MVector(0,-1,0)
	# max_distance = 9999999999
	# dagPath = OpenMaya.MDagPath()
	# hit = mesh.intersect(source_pnt, ray_dir, None, False, OpenMaya.MSpace.kWorld,)
def main():
	returnList = []

	lods = valid_lods()
	for lod in lods:
		tracks = all_tracks(lod)
		print(tracks)
		left, right = side_track(tracks)

		def check_track_number(side):
			for x in range(len(side)):
				number_pattern = '[LR]' + str(x) + '$'
				comp_pattern = re.compile(number_pattern)
				if not comp_pattern.findall(side[x][0]):
					tmp = []
					tmp.append(side[x][0] + " - not valid name or number")
					tmp.append(side[x][0])
					returnList.append(tmp)
					# returnList.append(side[x][0])

		check_track_number(left)
		check_track_number(right)

	print('RESULT ', returnList)
	return returnList


		# included_tracks(left)

		# #side for left example
		# #left
		# def fractal_check(side):
		# 	center, size = bounding_box(side[0][0])
		# 	intersection_track = []
		# 	for track in side:
		# 		# center, size = bounding_box(track[0])
		# 		if intersection(track[0], center):
		# 			intersection_track.append(track)
		# 	#naming for intersection_track



		# 	out_intersection = removeList(side, intersection_track)
		# 	if out_intersection:
		# 		out_intersection = sorted(out_intersection, key=lambda x: x[1])
