import maya.cmds as cmds
from maya.mel import eval as meval
import os
import re
import posixpath
from simplygon_tools.utils.utilites import Settings
import simplygon_tools.utils.utilites as utl
from simplygon_tools.utils.constants import *
import subprocess


def check_socket():
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((HOST, PORT))
    sock.close()
    if result == 0:
        print("Port is open")
        return True
    else:
        print("Port is not open")
        return False


def load_import_preset():
    preset_path = '/'.join(FBX_PRESET.split('\\'))
    print('_preset', preset_path)
    print('preset', FBX_PRESET)
    meval('FBXLoadImportPresetFile -f "' + preset_path + '";')


def export_selection(selection):
    print('export manual', Settings.lods_manual)
    print('export auto', Settings.lods_calculate)
    # load_import_preset()

    # todo validate
    selection = cmds.ls(sl=True)

    # todo check
    # detach textures
    node_material = utl.clear_textures()
    # full_export_path = posixpath.join(FILES_DIR, 'export.fbx')
    cmds.file(INPUT_FILES, f=True, options='v=0', typ='FBX export', pr=1, es=1)

    # assign textures
    utl.reassign_textures(node_material)


def edit_lods_spl(preset_path, lod_counts):  # lods_count, example ['5000', '2500', '1000'] or ['', '2500', '']
    with open(preset_path, 'r') as file:
        # read a list of lines into data
        data = file.readlines()

    lods_line = []

    # gather line with triangle counts
    for idx, x in enumerate(data):
        if 'TriangleCount' in data[idx]:
            print('find', data[idx])
            lods_line.append([data[idx], idx])

    # change line to new value
    for idx, x in enumerate(lod_counts):
        if lod_counts[idx].isdigit():
            print('F', lod_counts[idx])
            new_lod_count = lod_counts[idx]
            lods_line[idx][0] = re.sub(r"\d+", new_lod_count, lods_line[idx][0])
            print('Final_line', lods_line[idx][0])
            data[lods_line[idx][1]] = lods_line[idx][0]

    with open(preset_path, 'w') as file:
        file.writelines(data)


def batch_command():
    cmd = SIMPLYGON_EXE + ' --Input ' + INPUT_FILES + \
          ' --Output ' + OUTPUT_FILES + \
          ' --OutputFileFormat fbx --SPL ' + SPL_PRESET + \
          ' --Server ' + HOST_PORT + ' --Verbose'
    print('CMD', cmd)
    return cmd


def execute_command(command):
    if check_socket():
        for i in range(10):
            result = os.system(command)
            print('\nRESULT!\n', result)
            if result > -1:
                break


def send_to_simplygon(preset, type_reduce):
    PRESET_PATH = posixpath.join(FILES_DIR, 'input', preset + '.spl')

    # todo refactor
    print('TYPE ', type_reduce)
    lods_count = Settings.lods_calculate[1:]
    lods_count = list(map(str, lods_count))
    if type_reduce is 'Manual':
        lods_count = Settings.lods_manual
        print('TYPE_R', lods_count)

    # edit_lods_spl(PRESET_PATH, lods_count)

    cmd = SIMPLYGON + r' ' \
                      r'--Input ' + EXPORT_FILE + ' ' \
                                                  r'--Output ' + OUTPUT_DIR + ' ' \
                                                                              r'--OutputFileFormat fbx ' \
                                                                              r'--Spl ' + PRESET_PATH + ' ' \
                                                                                                        r'--Server ' + HOST + ':' + str(
        PORT) + ' ' \
                r'--Verbose'

    # todo
    if check_socket():
        os.system(cmd)
    else:
        return


def import_lods():
    load_import_preset()
    for i in range(1, 4):
        lod_import_file = os.path.join(IMPORT_FILES, 'LOD' + str(i), 'export_lods_LOD' + str(i) + '.fbx')
        print('lod: ', lod_import_file)
        # full_import_path = posixpath.join(FILES_DIR, 'export.fbx')
        cmds.file(lod_import_file, i=True, add=True,
                  type='FBX', iv=True,
                  mnc=False, pr=True,
                  ra=True, rdn=True,
                  namespace=':')


def main_commands(type_reduce=None):
    print('\n\n\n\nTYPE BUTTON ', type_reduce)

    # get polycount
    lod_list = utl.lods_count(type_reduce)
    return
    # get selection
    selection = cmds.ls(sl=True)
    # export selection to fbx
    export_selection(selection)
    # todo
    lod_list = lods_count(type_reduce)
    print('\n\n\nLODS', lod_list)
    edit_lods_spl(SPL_PRESET, lod_list)
    cmd = batch_command()
    utl.clear_folder(OUTPUT_FILES)
    execute_command(cmd)
    import_lods()
    # data = subprocess.check_output(cmd, shell=False)
    # print('DATE', data)
    # delete previous simplygon`s lods
    # if utl.exists_folder(OUTPUT_DIR):
    #     utl.clear_folder(OUTPUT_DIR)
    # edit xml preset
    # send to simplygon
    # send_to_simplygon('proxy', type_reduce)
    # check valid generation lods
    # import simplygon`s lods
    # reconstruct scene - name, layers etc.
    pass
