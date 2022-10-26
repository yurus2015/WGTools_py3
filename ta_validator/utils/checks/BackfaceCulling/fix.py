import maya.cmds as cmds

from validator2019.utils.validator_API import *
checkId = 2
checkLabel = "3.6 Check Objects with backface culling"


def main(*args):


	if args:
		for i in args:

			#first - unlock
			cmds.setAttr(i +".backfaceCulling", l = False)
			#second - switch off
			cmds.setAttr(i +".backfaceCulling", False)

	# meshList = cmds.ls(type="mesh", l=1)

	# if meshList:
	# 	for i in meshList:
	# 		cmds.setAttr(i+".backfaceCulling", False)

	return []