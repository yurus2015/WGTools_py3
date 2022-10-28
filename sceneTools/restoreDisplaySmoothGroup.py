import maya.cmds as cmds


def list_remove_duplicate(source_list):
    return list(set(source_list))


def list_subtract(big_list, small_list):
    return list(set(big_list) - set(small_list))


def soft_hard_display_restore(mesh):
    # long path mesh or needs mesh long path yet
    mesh_long_name = cmds.ls(mesh, l=True)[0]
    mesh_shape_list = cmds.filterExpand(mesh_long_name, sm=12, fp=True)
    smooth_node = cmds.polySoftEdge(mesh_shape_list[0], a=180, ch=True)[0]
    connected_nodes = cmds.listConnections(smooth_node, sh=1, s=1)
    connected_nodes = cmds.ls(connected_nodes, l=True)

    # remove duplicate
    connected_nodes = list_remove_duplicate(connected_nodes)

    # remove base shape - get original
    original_nodes = list_subtract(connected_nodes, mesh_shape_list)

    cmds.transferAttributes(original_nodes[0], mesh_shape_list[0], transferNormals=1)
    cmds.delete(mesh_long_name, ch=1)
    cmds.select(d=True)


def restore_selected():
    selection = cmds.ls(sl=True)
    shapes = cmds.filterExpand(selection, sm=12, fp=True)
    for s in shapes:
        soft_hard_display_restore(s)
    cmds.select(selection)


def restore_all():
    all_meshes = cmds.ls(typ='mesh')
    for m in all_meshes:
        soft_hard_display_restore(m)
