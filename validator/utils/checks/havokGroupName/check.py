import maya.cmds as cmds
#from validator2019.utils.validator_API import *
checkId = 24
checkLabel = "Havok scenes should have a material group"

VALIDNAME = ['__n_metal', '__n_wood', '__n_stone']

def main():
	print('<< ' + checkLabel.upper() + ' >>')
	returnList = []

	topLevelDags = cmds.ls(l=1, assemblies = 1)
	file_name = cmds.file(q=1, sn=1, shn=1)
	material = 'havok material'

	for n in VALIDNAME:
		if n in file_name:
			material = n
			for i in topLevelDags:
				if n in i:
					return  returnList

	# for i in topLevelDags:
	# 	for n in VALIDNAME:
	# 		if n in i:
	# 			material = n
	# 			if n in file_name:
	# 				return returnList


	# for i in topLevelDags:
	#     if "_havok" in i:
	#         return  returnList

	returnList.append(["The current scene has no groups which name contains: "+ material,""])
	return  returnList