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
			#string $infls[] = `skinCluster -q -inf $skinCluster`;
			# string $wtinfs[] = `skinCluster -q -wi $skinCluster`;
			infls = cmds.skinCluster(claster, q=1, inf=1)
			wtinfs = cmds.skinCluster(claster, q=1, wi=1)
			#	int $nodeState = `getAttr ($skinCluster+".nodeState")`;
			nodeState = cmds.getAttr(claster+".nodeState")
			cmds.setAttr(claster+".nodeState",1)

			for i in infls:
				found = None
				for w in wtinfs:
					if w == i:
						found = True
						break
				if not found:
					tmp = []
					tmp.append(mesh)
					tmp.append([(claster, i)])
					returnList.append(tmp)

			cmds.setAttr(claster+".nodeState",nodeState)

	return  returnList

