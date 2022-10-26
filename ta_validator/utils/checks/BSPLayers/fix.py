import maya.cmds as cmds
from validator2019.utils.validator_API import *


checkId = 417
checkLabel = "BSP layers"

def main(*args):



	if args:
		bsp_l = None
		layers = cmds.ls(type = 'displayLayer')
		for layer in layers:
			if 'BSP' in layer:
				bsp_l = True

		if bsp_l == None:
			cmds.createDisplayLayer(n='BSP', empty=1)

		for i in args:
			cmds.editDisplayLayerMembers('BSP', i)

	return []




