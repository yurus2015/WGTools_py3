import maya.cmds as cmds


# def find_skin_cluster(mesh):
# 	clasters = cmds.ls(type='skinCluster')
# 	for c in clasters:
# 		geometry = cmds.skinCluster(c, q=1, g=1)
# 		for g in geometry:
# 			shape = cmds.ls(g, l=1)[0]
# 			if shape==mesh:
# 				return c

def main(*args):
    units = cmds.currentUnit(query=True, linear=True)
    if units == 'cm':
        slide = 0.1
    if units == 'm':
        slide = 0.001
    if args:
        for i in args:
            print('FIXED', i)
            if i[1] == 0:
                cmds.move(slide, 0, 0, i[0] + '.vtx[0]', r=True, ws=1)
            elif i[1] == 1:
                cmds.move(0, slide, 0, i[0] + '.vtx[0]', r=True, ws=1)
            else:
                cmds.move(0, 0, slide, i[0] + '.vtx[0]', r=True, ws=1)

    return []
