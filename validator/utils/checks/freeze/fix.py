import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 12
checkLabel = "1.13 Check objects with non-zero transformations"


def main(*args):
    if args:
        for i in args:
            cmds.makeIdentity(i, a=1, t=1, r=1, s=1)

    return []
