import maya.cmds as cmds

checkId = 417
checkLabel = "Lost Nodes"


def main(*args):
    if args:
        cmds.delete(args[0])

    return []
