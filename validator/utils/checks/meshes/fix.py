import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 31
checkLabel = "8.5 Check for empty shapes"


def main(*args):
    listTransforms = vl_listAllTransforms()
    # returnList = []

    for x in range(len(listTransforms)):
        shapes = cmds.listRelatives(listTransforms[x], shapes=True, f=True)
        for shape in shapes:
            listConnection = cmds.listConnections(shape)
            if listConnection:
                continue
            else:
                cmds.delete(shape)
# if len(shapes) == 2 :
#	origName = None
#	for y in shapes:
#		check = y.find("Orig")
#		if check != -1:
#			origName = 1
#
#	if origName != 1:
#		print 'BAG'
#		#if there is two or more connections, its means, transform have another empty shape(bug)
#		for shape in shapes:
#			inter = cmds.getAttr(shape +'.intermediateObject')
#			print 'INTER', inter
#			if inter:
#				cmds.delete(shape)
# return []
