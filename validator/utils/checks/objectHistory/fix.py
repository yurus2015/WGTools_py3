import maya.cmds as cmds

checkId = 4199
checkLabel = "Check history"


def main(*args):
    if args:
        for i in args:
            cmds.delete(i, ch=1)

    return []
