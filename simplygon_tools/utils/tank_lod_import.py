from simplygon_tools.utils.constants import *
import simplygon_tools.utils.utilites as utl
from maya.mel import eval as meval
import maya.cmds as cmds
import re


def import_lod(lod_path):
    # import command
    # check lod
    # re-parent to exists valid lod
    # delete imported lod

    # print('lod: ', lod_import_file)
    cmds.file(lod_path, i=True, add=True,
              type='FBX', iv=True,
              mnc=False, pr=True,
              ra=True, rdn=True,
              namespace=':')

    pass


# probably can combine with import_lod
def import_proxy(lod_path):
    pass


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
    before = set(cmds.ls(assemblies=True))
    import_lod(lod_path)
    after = set(cmds.ls(assemblies=True))
    imported_head = after.difference(before)
    imported_head = list(imported_head)
    print('IMPORTED \n', imported_head)
    print('EXPORTED \n', imported_list)
    print('LOD \n', lod_number)

    for element in imported_list:
        # replace lod's name in imported to current in loop
        new_name = re.sub(r'lod\d', 'lod' + str(lod_number), element)
        print('NEW NAME \n', new_name)
        current_name = re.sub(r'lod\d', imported_head[0], element)
        print('CARRENT NAME: \n', current_name)

        # todo restore normal

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
    cmds.delete(imported_head)


def create_hierarchy(input_path):
    parent_group_list = input_path.split('|')[1:-1]
    rebuilt_path = ''
    for g in parent_group_list:
        parent = rebuilt_path
        rebuilt_path = rebuilt_path + '|' + g
        if not cmds.objExists(rebuilt_path):
            cmds.group(n=g, em=True, p=parent)
    return rebuilt_path


# loop through all lods
# todo send exported objects as arguments
def import_all_lods(imported_list):
    # todo load specific preset: only lods, lods and proxy, only proxy
    load_preset_fbx()
    output_dir = utl.generate_lod_path(OUTPUT_FILES)
    print('EX_EX', output_dir)
    for i in range(1, 4):
        lod_dir = os.path.join(str(output_dir), 'LOD' + str(i))
        fbx_file = utl.generate_lod_fbx_path(lod_dir)
        # lod_import_file = os.path.join(IMPORT_FILES, 'LOD' + str(i), 'export_lods_LOD' + str(i) + '.fbx')
        if os.path.isfile(fbx_file):
            get_imported_objects(fbx_file, i, imported_list)
