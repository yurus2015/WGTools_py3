import maya.cmds as cmds
#from validator.resources.validator_API import *
checkId = 412
checkLabel = "3.23 Check for group pivots"


def main(*args):

    if args:
        for i in args:
            cmds.xform(i, ws = 1, rp = (0, 0, 0))
            cmds.xform(i, ws = 1, sp = (0, 0, 0))

	return []