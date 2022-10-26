import maya.cmds as cmds
import math
from validator2019.utils.validator_API import *
checkId = 18
checkLabel = "6.16 Check transformations of HP objests"


def main():
	print('<< ' + checkLabel.upper() + ' >>')
	objList = vl_listHPModules()
	returnList = []

	for x in objList:

		objTtranslate = cmds.xform (x, q=True, t=True, ws = True)
		objPivot = cmds.xform (x, q=True, piv=True, ws = True)
		objScale = cmds.xform (x, q=True, s=True, r=True)
		check = 0

		for y in range(len(objTtranslate)):
			objTtranslate[y] = round(objTtranslate[y], 3)
			objPivot[y] = round(objPivot[y], 3)
			if objTtranslate[y] != objPivot[y] and abs(objTtranslate[y] - objPivot[y]) > 0.0011:
				#print 'DIFF ', abs(objTtranslate[y] - objPivot[y])
				check =1

		if check == 1:
			tmp = []
			tmp.append(x + " - transform value is not equal to real position")
			tmp.append(x)
			returnList.append(tmp)

		check = 0

		for y in range(len(objScale)):
			objScale[y] = round(objScale[y], 3)
			for i in objScale:
				if i != 1.0:
					check =1
		if check == 1:
			tmp = []
			tmp.append(x + " - scale value is not equal to 1")
			tmp.append(x)
			returnList.append(tmp)

		check = 0
		bbx = cmds.xform(x, q=True, bbi=True, ws=True)
		value = 0.01
		unit = cmds.currentUnit( query=True, linear=True )
		if unit != 'm':
			value = 1.00


		if objPivot[0] < bbx[0]-value or objPivot[0] > bbx[3]+value or objPivot[1] < bbx[1]-value or objPivot[1] > bbx[4]+value or objPivot[2] < bbx[2]-value or objPivot[2] > bbx[5]+value:

			tmp = []
			tmp.append(x + " - pivot is not inside")
			tmp.append(x)
			returnList.append(tmp)


	return  returnList
