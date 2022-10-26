
import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 61
checkLabel = "1.3 Check Working Units"


def main(*args):

	cmds.currentUnit( linear='m' )
	size = cmds.grid( query=True, size=True )
	spacing = cmds.grid( query=True, spacing=True )
	cmds.grid(spacing = spacing*100, size = size*100 )


	return  []
