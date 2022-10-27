import maya.cmds as cmds
from validator.utils.validator_API import *

checkLabel = "8.12 Check forbidden symbols in names"


def main(*args):
    allMeshes = cmds.ls(type="mesh", l=1)
    if allMeshes:
        for m in allMeshes:
            master = cmds.listRelatives(m, p=True, path=True, typ='transform')
            shortName = master[0].split('|')
            cmds.rename(m, shortName[-1] + "_Shape")
