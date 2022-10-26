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
	for mesh in all_meshes:
		claster = find_skin_cluster(mesh)
		if claster:
			vertex = cmds.polyListComponentConversion(mesh, tv=True )
			vertex = cmds.ls(vertex, fl=True)
			for v in vertex:
				value = cmds.skinPercent( claster, v, query=True, value=True )
				for vl in value:
					if vl < 0.01 and vl > 0.0:
						tmp = []
						tmp.append(mesh)
						tmp.append(mesh)
						returnList.append(tmp)
						break
	return  returnList

