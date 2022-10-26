import maya.cmds as cmds
from validator2019.utils.validator_API import *
import os
import re
dir = os.path.dirname(__file__)

checkId = 160
checkLabel = "Check havok shape type"

def main():
	print('<< ' + checkLabel.upper() + ' >>')
	return_list = []
	names = vl_read_json(dir, "HavokShapeTypeNames.json")
	reg_exp = []
	for x in names["names"]:
		reg_exp.append(re.compile(x))

	for x in cmds.ls(l=True, type = "hkNodeShape"):
		# find = False
		# for r in reg_exp:
		# 	if r.search(x.split("|")[1]):
		# 		find = True
		# if not find:
		# 	continue
		type = cmds.getAttr(x + ".shapeType")
		#if type == 1 or type == 6:
		if type == 6:
			return_list.append([("Havok shape has wrong type %s") % (x), x])

	#for "_havok" group - show up only 6 (mesh) type of shape. Hull type is correct
	havokGroups = cmds.ls(l=1, assemblies=1)
	for i in havokGroups:
		if "_havok" in i:
			relatives = cmds.listRelatives(i, ad=1, c=1, f=1)
			for j in relatives:
				if cmds.nodeType(j) == "hkNodeShape":
					if cmds.getAttr(j + ".shapeType") == 6:
						tmp = []
						tmp.append("Havok shape has wrong type (Mesh): " + str(j))
						tmp.append(j)
						return_list.append(tmp)

	return return_list

