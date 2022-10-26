import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 24
checkLabel = "3.20 Check LOD groups with non-zero pivots"


def main(*args):

    if args:
        for obj in args:
            rotatePivot = cmds.xform(obj, ws = 1, rp = (0,0,0))
            scalePivot = cmds.xform(obj,  ws = 1, sp = (0,0,0))

    return []