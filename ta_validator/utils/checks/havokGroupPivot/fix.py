import maya.cmds as cmds

checkId = 371
checkLabel = "Check Havok Group Pivot"


def main(*args):
	if args:
		for obj in args:
			cmds.xform(obj,  ws = 1, rp = [0.0, 0.0, 0.0])
			cmds.xform(obj,  ws = 1, sp = [0.0, 0.0, 0.0])

	return []