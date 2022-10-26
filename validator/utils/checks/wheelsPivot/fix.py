import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import time
from validator2019.utils.validator_API import *
checkId = 60
checkLabel = "3.24 Check pivots of wheels "

def removeList(fromList, thisList):

	resultList =  [n for n in fromList if n not in thisList]
	resultList = list(resultList)
	return resultList

def getCentroidOfFaces(faces):

	vertexlist = faces

	pointCoords = []
	xAverage = 0
	for i in vertexlist:
		coords = cmds.xform(i, q=1, ws=1, t=1)
		xAverage += coords[0]
		tmp = []
		tmp.append(coords[2])
		tmp.append(coords[1])
		pointCoords.append(tmp)

	xAverage /= len(vertexlist)

	#find convex hull
	points = None
	points = pointCoords

	#shifting array from [x, y, z, number] to [y, z, number, x] for using convexHulls
	for x in range(len(points)):
		points[x] = points[x][1:] + points[x][:1]

	# Sort the points lexicographically (tuples are compared lexicographically).
	# Remove duplicates to detect the case we have just one unique point.
	points = sorted(list(points))
	# Boring case: no points or a single point, possibly repeated multiple times.
	if len(points) <= 1:
		return points

	# 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
	# Returns a positive value, if OAB makes a counter-clockwise turn,
	# negative for clockwise turn, and zero if the points are collinear.
	def cross(o, a, b):
		return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

	# Build lower hull
	lower = []
	for p in points:
		while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
			lower.pop()
		lower.append(p)

	# Build upper hull
	upper = []
	for p in reversed(points):
		while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
			upper.pop()
		upper.append(p)

	# Concatenation of the lower and upper hulls gives the convex hull.
	# Last point of each list is omitted because it is repeated at the beginning of the other list.
	finalPoints =  lower[:-1] + upper[:-1]


	#FIND CENTROID
	arrayLen = len(finalPoints)
	endIdx = arrayLen-1
	#get area
	Area = 0
	for idx, i in enumerate(finalPoints):
		if idx != endIdx:
			Area += finalPoints[idx][0] * finalPoints[idx+1][1] - finalPoints[idx+1][0]*finalPoints[idx][1]
		elif idx == endIdx:
			Area += finalPoints[idx][0] * finalPoints[0][1] - finalPoints[0][0]*finalPoints[idx][1]

	Area *= 0.5

	Cx = 0
	Cy = 0

	for idx,i in enumerate(finalPoints):
		if idx != endIdx:
			Cx += (finalPoints[idx][0]+finalPoints[idx+1][0]) * (finalPoints[idx][0]*finalPoints[idx+1][1] - finalPoints[idx+1][0]*finalPoints[idx][1])
		elif idx == endIdx:
			Cx += (finalPoints[idx][0]+finalPoints[0][0]) * (finalPoints[idx][0]*finalPoints[0][1] - finalPoints[0][0]*finalPoints[idx][1])
	Cx  = Cx / (6*Area)

	for idx,i in enumerate(finalPoints):
		if idx != endIdx:
			Cy += (finalPoints[idx][1]+finalPoints[idx+1][1]) * (finalPoints[idx][0]*finalPoints[idx+1][1] - finalPoints[idx+1][0]*finalPoints[idx][1])
		elif idx == endIdx:
			Cy += (finalPoints[idx][1]+finalPoints[0][1]) * (finalPoints[idx][0]*finalPoints[0][1] - finalPoints[0][0]*finalPoints[idx][1])
	Cy  = Cy / (6*Area)


	finalCoords = [xAverage, Cx, Cy]

	return finalCoords

def bboxWheels(wheel):
	minimum = cmds.getAttr(wheel + '.boundingBoxMin')
	maximum = cmds.getAttr(wheel + '.boundingBoxMax')
	w_coord = cmds.xform(wheel, q=1, ws = 1, rp = 1)

	hight = maximum[0][1] - minimum[0][1]

	width = maximum[0][2] - minimum[0][2]
	if ("%.4f" % hight) == ("%.4f" % width):

		return True

	else:
		return False

def main(*args):

	try:
		lod0 = cmds.ls("lod0*", l=1, type = 'transform')[0]
	except:
		return[]
	relatives = cmds.listRelatives(lod0, ad=1, f=1, type = 'transform')

	listWheels = []
	for i in relatives:
		if i.find("wd_") != -1 or i.find("w_") != -1:
			listWheels.append(i)



	if listWheels:

		for w in listWheels:
			if w.find("lod0") != -1:

				if bboxWheels(w) == True:
					cmds.xform(w, cp=1)
					w_coord = cmds.xform(w, q=1, ws = 1, rp = 1)

				else:

					w_coord = cmds.xform(w, q=1, ws = 1, rp = 1)
					faces = cmds.ls(w+'.f[*]', fl = True)
					centroidCoords = getCentroidOfFaces(faces)
					cmds.xform(w, ws=1, rp = centroidCoords)
					cmds.xform(w, ws=1, sp = centroidCoords)



		#get lod0 chassis children
		lod0Wheels = []
		lod0 = cmds.ls("*lod0*", l=1)[0]
		relatives = cmds.listRelatives(lod0, c=1, f=1)
		for rel in relatives:
			if rel.find("chassis") != -1:
				relrel = cmds.listRelatives(rel, c=1, f=1)
				if relrel:
					lod0Wheels = relrel

				break


		#pivots for lod1, lod2, lod3, lod4
		wheelsNonLod0 = cmds.ls('w_*', 'wd_*', l= 1, type = 'transform')
		wheelsNonLod0 = removeList(wheelsNonLod0, listWheels)

		for w in wheelsNonLod0:
			if w.find("lod0")== -1:
				# get the same pivot as in lod0
				shortName = w.split("|")[-1]
				if lod0Wheels:
					for i in lod0Wheels:
						iShort = i.split("|")[-1]
						if iShort == shortName:
							obj_pivot = cmds.xform(i, q=1, ws = 1, rp = 1)
							cmds.xform(w, ws=1, rp=obj_pivot)
							cmds.xform(w, ws=1, sp=obj_pivot)

	return []