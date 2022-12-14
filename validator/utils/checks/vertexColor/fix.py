import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 201
checkLabel = "Check Vertex Color"


def main(*args):
    mesh = cmds.ls(typ='mesh')
    for m in mesh:
        c_sets = cmds.polyColorSet(m, query=True, allColorSets=True)
        if c_sets:
            transf = cmds.listRelatives(m, p=1, type='transform')
            if 'HP' in transf[0]:
                print('Current', transf[0])
                pass
            else:
                for set in c_sets:
                    cmds.polyColorSet(m, delete=True, colorSet=set)
    return []
