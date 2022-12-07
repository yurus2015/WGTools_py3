from simplygon_tools.utils.constants import *
import simplygon_tools.utils.utilites as utl
from maya.mel import eval as meval
import maya.cmds as cmds
import re


def import_lod(lod_path):
    cmds.file(lod_path, i=True, add=True,
              type='FBX', iv=True,
              mnc=False, pr=True,
              ra=True, rdn=True,
              namespace=':')


# probably can combine with import_lod
# def import_proxy(lod_path):
#     pass


# one time in cycle
def load_preset_fbx():
    # from constants
    preset_path = '/'.join(FBX_PRESET.split('\\'))
    meval('FBXLoadImportPresetFile -f "' + preset_path + '";')


# todo send exported objects as arguments
def get_imported_objects(lod_path, lod_number, imported_list):
    imported = []
    if not isinstance(imported_list, list):
        imported_list = [imported_list]
        # todo remove tracks any case
        # hmmm... we should`t export track
        # sub = 'truck_'
        # imported_list = ([s for s in imported_list if sub not in s])

    before = set(cmds.ls(assemblies=True))
    import_lod(lod_path)
    after = set(cmds.ls(assemblies=True))
    imported_head = after.difference(before)
    imported_head = list(imported_head)

    utl.logging('IMPORT AS LIST', imported_list)
    utl.logging('IMPORT AS HEAD', imported_head)
    # print('IMPORTED \n', imported_head)
    # print('EXPORTED \n', imported_list)
    # print('LOD \n', lod_number)

    # if lod_number == 4:
    #     print('SSSSS', lod_path)

    # todo restore normal
    # utl.restore_soft_normals(imported_head)
    # utl.soft_restore(imported_head)

    for element in imported_list:
        # replace lod's name in imported to current in loop
        new_name = re.sub(r'lod\d', 'lod' + str(lod_number), element)
        print('NEW NAME \n', new_name)
        utl.logging('VALID NAME', new_name)
        current_name = re.sub(r'lod\d', imported_head[0], element)
        print('CURRENT NAME: \n', current_name)
        utl.logging('CURRENT NAME', current_name)

        # check exists current name element
        if not cmds.objExists(current_name):  # its mesh without group or proxy or reduce to zero
            short_name = element.split('|')[-1]
            current_name = cmds.rename(imported_head[0], short_name)

        # check exists object, if yes, remove existing
        if cmds.objExists(new_name):
            print('Exists!')
            cmds.delete(new_name)

        # create group in hierarchy
        parent_group = create_hierarchy(new_name)
        print('PARENT GRP \n', parent_group)

        try:
            # parent imported to specify lod/group
            cmds.parent(current_name, parent_group)
        except:
            pass

    # delete source lod/group
    for head in imported_head:
        if cmds.objExists(head):
            cmds.delete(head)


def create_hierarchy(input_path):
    parent_group_list = input_path.split('|')[1:-1]
    rebuilt_path = ''
    for g in parent_group_list:
        parent = rebuilt_path
        rebuilt_path = rebuilt_path + '|' + g
        if not cmds.objExists(rebuilt_path):
            if len(parent):
                cmds.group(n=g, em=True, p=parent)
            else:
                cmds.group(n=g, em=True)
    return rebuilt_path


# loop through all lods
# todo send exported objects as arguments
def import_all_lods(imported_list, start, end):
    # todo load specific preset: only lods, lods and proxy, only proxy
    load_preset_fbx()
    utl.logging('IMPORT', imported_list)
    for i in range(start, end):
        utl.logging('LOD', i)
        # lod_dir = os.path.join(str(output_dir), 'LOD' + str(i))
        fbx_file = utl.generate_lod_fbx_path('LOD' + str(i))
        utl.logging('IMP FILE', fbx_file)
        # lod_import_file = os.path.join(IMPORT_FILES, 'LOD' + str(i), 'export_lods_LOD' + str(i) + '.fbx')
        if os.path.isfile(fbx_file):
            get_imported_objects(fbx_file, i, imported_list)
