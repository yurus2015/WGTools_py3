import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

checkId = 130
checkLabel = "Check phantom UVs"

def main(*args):

    if args:
        for i in args:
            cmds.select(i)
            cmds.transferAttributes(i,i,transferUVs=2, transferColors = 1, searchMethod=3, colorBorders=1)
            cmds.delete(ch=1)
            try:
            	cmds.polyColorSet(delete=1)
            except:
            	pass
