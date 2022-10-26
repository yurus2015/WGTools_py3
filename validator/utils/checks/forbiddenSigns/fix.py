import maya.cmds as cmds
from maya.mel import eval as meval

from validator.resources.validator_API import *
checkId = 11

checkLabel = "8.12 Check forbidden symbols in names"


def main(*args):

    allMeshes = cmds.ls(type="mesh", l=1)
    if allMeshes:
        for m in allMeshes:
            master = cmds.listRelatives(m, p = True, path = True, typ = 'transform')
            shortName = master[0].split('|')
            cmds.rename(m, shortName[-1] + "_Shape")
            # cmds.select(m)
            # evalCMD = 'renameSelectionList("' + shortName[-1] +'_Shape")'
            # meval(evalCMD)