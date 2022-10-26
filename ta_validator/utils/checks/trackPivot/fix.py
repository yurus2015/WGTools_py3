import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 45
checkLabel = "3.25 Check for track pivots"

def main(*args):
    if args:
        for obj in args:
            obj_pivot = cmds.xform(obj, ws = 1, rp = (0,0,0))
            obj_scalePivot = cmds.xform(obj, ws = 1, sp = (0,0,0))
    return []