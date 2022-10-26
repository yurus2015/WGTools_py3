import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 7
checkLabel = "3.23 Check for chassis pivots"

def main(*args):

    if args:
        for i in args:
            cmds.xform(i, ws = 1, rp = (0, 0, 0))
            cmds.xform(i, ws = 1, sp = (0, 0, 0))

	return []