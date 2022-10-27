import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 36
checkLabel = "3.8 Check Objects with attribute 'Opposite' turned on"


def main(*args):
    if args:
        for i in args:
            cmds.setAttr(i + ".opposite", False)

    return []
