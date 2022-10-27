import maya.cmds as cmds


def find_skin_cluster(mesh):
    clusters = cmds.ls(type='skinCluster')
    for c in clusters:
        geometry = cmds.skinCluster(c, q=1, g=1)
        for g in geometry:
            shape = cmds.ls(g, l=1)[0]
            if shape == mesh:
                return c


def main():
    return_list = []
    all_meshes = cmds.ls(type='mesh', l=1)
    units = cmds.currentUnit(query=True, linear=True)
    slide = 0.1
    if units == 'cm':
        slide = 0.1
    if units == 'm':
        slide = 0.001
    for mesh in all_meshes:
        cluster = find_skin_cluster(mesh)
        if cluster:
            bb = cmds.getAttr(mesh + '.boundingBoxSize')
            for index in range(len(bb[0])):
                if bb[0][index] < slide:
                    tmp = [mesh, [(mesh, index)]]
                    return_list.append(tmp)
                    break

    return return_list
