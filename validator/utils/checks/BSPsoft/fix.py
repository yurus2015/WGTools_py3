import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 413
checkLabel = "BSP soft"


def main(*args):
    if args:
        for i in args:
            cmds.polySoftEdge(i, a=180, ch=0)

    return []
