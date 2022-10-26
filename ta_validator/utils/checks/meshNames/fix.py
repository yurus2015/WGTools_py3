import maya.cmds as cmds
from maya.mel import eval as meval
from validator2019.utils.validator_API import *
checkId = 32

checkLabel = "1.10 Check names of meshes"



def main(*args):

    allMeshes = cmds.ls(type="mesh", l=1)
    if allMeshes:
        for i in allMeshes:
            master = cmds.listRelatives(i, p = True, path = True, typ = 'transform')
            shortName = master[0].split('|')
            cmds.select(i)
            evalCMD = 'renameSelectionList("' + shortName[-1] +'Shape")'
            meval(evalCMD)
