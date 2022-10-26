import maya.cmds as cmds

def find_skin_cluster(mesh):
	clasters = cmds.ls(type='skinCluster')
	for c in clasters:
		geometry = cmds.skinCluster(c, q=1, g=1)
		for g in geometry:
			shape = cmds.ls(g, l=1)[0]
			if shape==mesh:
				return c


def main():
	returnList = []
	all_meshes = cmds.ls(type='mesh', l=1)
	units = cmds.currentUnit( query=True, linear=True )
	if units == 'cm':
		slide = 0.1
	if units == 'm':
		slide = 0.001
	for mesh in all_meshes:
		claster = find_skin_cluster(mesh)
		if claster:
			bb = cmds.getAttr(mesh+'.boundingBoxSize')
			print('BB', bb)
			for indx in range(len(bb[0])):
				if bb[0][indx] < slide:
					tmp = []
					tmp.append(mesh)
					tmp.append([(mesh, indx)])
					returnList.append(tmp)
					break

	return  returnList
