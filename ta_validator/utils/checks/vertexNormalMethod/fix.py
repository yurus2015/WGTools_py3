import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 59

checkLabel = "5.1 Vertex  Normal Method"

def main(*args):

	if args:
		for i in args:
			vmn = cmds.setAttr(i + ".vertexNormalMethod", 3)
	return []