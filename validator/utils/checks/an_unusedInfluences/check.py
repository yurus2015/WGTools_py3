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

            # mel example:
            # string influence[] = `skinCluster -q -inf $skinCluster`;
            # string vertex_influence[] = `skinCluster -q -wi $skinCluster`;

            influence = cmds.skinCluster(cluster, q=1, inf=1)
            vertex_influence = cmds.skinCluster(cluster, q=1, wi=1)

            # mel example: int $nodeState = `getAttr ($skinCluster+".nodeState")`;
            node_state = cmds.getAttr(cluster + ".nodeState")
            cmds.setAttr(cluster + ".nodeState", 1)

            for i in influence:
                found = None
                for w in vertex_influence:
                    if w == i:
                        found = True
                        break
                if not found:
                    tmp = [mesh, [(cluster, i)]]
                    # tmp.append(mesh)
                    # tmp.append([(cluster, i)])
                    return_list.append(tmp)

            cmds.setAttr(cluster + ".nodeState", node_state)

    return return_list
