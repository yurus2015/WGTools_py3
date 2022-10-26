import maya.cmds as cmds

def find_skin_cluster(mesh):
	clasters = cmds.ls(type='skinCluster')
	for c in clasters:
		geometry = cmds.skinCluster(c, q=1, g=1)
		for g in geometry:
			shape = cmds.ls(g, l=1)[0]
			if shape==mesh:
				return c

def main(*args):

	if args:
		for i in args:
			cmds.skinCluster(i[0], e=1, ri=i[1])

	return  []
