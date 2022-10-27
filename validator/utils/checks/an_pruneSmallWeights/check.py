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
    for mesh in all_meshes:
        cluster = find_skin_cluster(mesh)
        if cluster:
            vertex = cmds.polyListComponentConversion(mesh, tv=True)
            vertex = cmds.ls(vertex, fl=True)
            for v in vertex:
                value = cmds.skinPercent(cluster, v, query=True, value=True)
                for vl in value:
                    if 0.01 > vl > 0.0:
                        tmp = [mesh, mesh]
                        # tmp.append(mesh)
                        # tmp.append(mesh)
                        return_list.append(tmp)
                        break
    return return_list
