import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 20
checkLabel = "Check orientation of joints"


def main(*args):
    if args:
        for x in args:
            cmds.makeIdentity(x, apply=1, t=1, r=1, s=0, n=0, pn=1, jointOrient=1)
    #   LIST_joints = cmds.ls (type = "joint", l=1)
    #   if LIST_joints:
    # for x in LIST_joints:
    #     cmds.makeIdentity(x, apply=1, t=1, r=1, s=0, n=0, pn=1, jointOrient = 1)

    return []
