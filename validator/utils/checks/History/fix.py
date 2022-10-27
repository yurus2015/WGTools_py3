import maya.cmds as cmds
import maya.mel as mel

from validator.resources.validator_API import *

checkId = 16
checkLabel = "1.14 Check Objects with history"


def main(*args):
    if args:
        for i in args:
            cmds.select(i)
            mel.eval("doBakeNonDefHistory( 1, {\"prePost\" });")

            # deleting polyBlindData node

            tmpListOfinputs = cmds.listHistory(i, lf=1, il=1)  # List objects which have inputs
            for j in tmpListOfinputs:
                type = cmds.nodeType(j)
                if type == "polyBlindData":
                    try:
                        cmds.delete(j)
                    except:
                        pass

    return []
