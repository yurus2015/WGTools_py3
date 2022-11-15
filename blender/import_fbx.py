import maya.cmds as cmds
import tempfile
import os
from maya.mel import eval as meval


def load_fbx_plugin():
    if not cmds.pluginInfo('fbxmaya', query=True, loaded=True):
        cmds.loadPlugin('fbxmaya')


def set_units_meter():
    if cmds.currentUnit(q=True, linear=True) != "m":
        cmds.currentUnit(linear="m")


def load_import_prefs():
    current_dir = os.path.dirname(__file__)
    preset = os.path.join(current_dir, 'fbx.fbximportpreset')
    preset_path = '/'.join(preset.split('\\'))
    print('_preset_', current_dir)
    print('preset', preset_path)
    meval('FBXLoadImportPresetFile -f "' + preset_path + '";')


def import_file(path=None):
    if not path:  # import from temp directory
        file_name = 'export'
        file = tempfile.gettempdir() + os.sep + file_name + '.fbx'
        # file -import -type "FBX"  -ignoreVersion -ra true -mergeNamespacesOnClash false
        # -namespace "export" -options "fbx"  -pr  -importTimeRange "combine"
        # "d:/Branches/ARTMAIN/game/bin/tools/devtools/maya/simplygon/input/export.fbx";
        cmds.file(file, i=True, add=True,
                  type='FBX', iv=True,
                  mnc=False, pr=True,
                  ra=True, rdn=True,
                  namespace=':')


def imported_objects():
    imported = []
    before = set(cmds.ls(assemblies=True))
    import_file()
    after = set(cmds.ls(assemblies=True))
    imported_head = after.difference(before)
    if imported_head:
        # freeze transform locators/groups only scale
        cmds.makeIdentity(imported_head, apply=True, s=1, n=0)
        imported.extend(imported_head)
    # print('Imported:', imported)
    for head in imported_head:
        child = cmds.listRelatives(head, ad=True, type='transform')
        print('Child', child)
        if child:
            imported.extend(child)
    print('Imported:', imported)
    return imported


def list_remove_duplicate(source_list):
    return list(set(source_list))


def list_subtract(big_list, small_list):
    return list(set(big_list) - set(small_list))


def rename_fbx_index(meshes):  # gunFBXASC046001
    for m in meshes:
        if 'FBXASC046' in m:
            rename_mesh = m.replace('FBXASC046', '')
            cmds.rename(m, rename_mesh)


def soft_restore(meshes):
    # all_meshes = cmds.ls(typ='mesh')
    for m in meshes:
        mesh_long_name = cmds.ls(m, l=True)[0]
        mesh_shape_list = cmds.filterExpand(mesh_long_name, sm=12, fp=True)
        smooth_node = cmds.polySoftEdge(mesh_shape_list[0], a=180, ch=True)[0]
        connected_nodes = cmds.listConnections(smooth_node, sh=1, s=1)
        connected_nodes = cmds.ls(connected_nodes, l=True)

        # todo
        # remove duplicate
        connected_nodes = list_remove_duplicate(connected_nodes)

        # remove base shape - get original
        original_nodes = list_subtract(connected_nodes, mesh_shape_list)

        cmds.transferAttributes(original_nodes[0], mesh_shape_list[0], transferNormals=1)
        cmds.delete(mesh_long_name, ch=1)
        cmds.select(d=True)


def assign_initial_shader(meshes):
    shading_engine = 'initialShadingGroup'
    cmds.sets(meshes, e=True, forceElement=shading_engine)

    # delete unused nodes
    meval('MLdeleteUnused')


def group_restore():
    locator_shape = cmds.ls(type=('locator'), l=True)
    locator_transform = cmds.listRelatives(locator_shape, p=True, type='transform')
    cmds.delete(locator_shape)
    # todo
    # freeze transform locators/groups
    cmds.makeIdentity(locator_transform, apply=True, t=1, r=1, s=1, n=0)


def fbx_import():
    load_fbx_plugin()
    load_import_prefs()
    set_units_meter()
    imported = imported_objects()
    soft_restore(imported)
    assign_initial_shader(imported)
    rename_fbx_index(imported)
    group_restore()
    print('IMPORT')


def fbx_export():
    file_name = 'import'
    file = tempfile.gettempdir() + os.sep + file_name + '.fbx'
