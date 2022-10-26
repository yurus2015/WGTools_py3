'''
algorithm
1. check selected - face or uv
2. convert to shell
3. get 2d bounding box
4. get parameters from grid uv
5. find near coord for up, bottom, left, right
6. scale uv shell
7. return selected
#polySelectBorderShell 0;
'''

import maya.cmds as cmds
from maya.mel import eval as meval

def checkSelection():
	if cmds.filterExpand( sm=(34,35) ):
		return True
	else:
		return False

def convert2shell():
	meval('polySelectBorderShell 0;')

def boundingBox():
	coord = cmds.polyEvaluate( bc2=True )
	return coord

def gridUV():
	gridDiv = cmds.optionVar( q='textureWindowGridDivisions' )
	gridSps = cmds.optionVar( q='textureWindowGridSpacing' )

	return gridDiv/gridSps


