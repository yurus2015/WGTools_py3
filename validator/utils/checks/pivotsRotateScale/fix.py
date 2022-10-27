import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 37
checkLabel = "3.26 Check Rotate Pivot and Scale Pivot values"


def main(*args):
    if args:
        for obj in args:
            obj_pivot = cmds.xform(obj, q=1, ws=1, rp=1)
            cmds.xform(obj, ws=1, sp=obj_pivot)

    return []
