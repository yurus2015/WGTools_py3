import maya.cmds as cmds
from maya.mel import eval as meval
import os
import re
import posixpath
from simplygon_tools.utils.utilites import Settings
import simplygon_tools.utils.utilites as utl
from simplygon_tools.utils.constants import *
from simplygon_tools.utils.tank_lod_import import *
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
    # selection = cmds.ls(sl=True)
    # todo need export without selection
    cmds.select(selection)

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


def edit_preset_spl(preset_path, lod_coefficient):  # lods coeff, example [0.3, 0.5, 0.5]
    with open(preset_path, 'r') as file:
        # read a list of lines into data
        data = file.readlines()

    lods_line = []

    # gather line with coefficients
    for idx, x in enumerate(data):
        if 'TriangleRatio' in data[idx]:
            print('find', data[idx])
            lods_line.append([data[idx], idx])

    # change line to new value
    for idx, x in enumerate(lod_coefficient):
        # if lod_coefficient[idx].isfloat():
        print('F', lod_coefficient[idx])
        new_lod_count = lod_coefficient[idx]
        lods_line[idx][0] = re.sub(r"0.\d+", str(new_lod_count), lods_line[idx][0])
        print('Final_line', lods_line[idx][0])
        data[lods_line[idx][1]] = lods_line[idx][0]

    with open(preset_path, 'w') as file:
        file.writelines(data)


def batch_command(preset):
    cmd = SIMPLYGON_EXE + ' --Input ' + INPUT_FILES + \
          ' --Output ' + OUTPUT_FILES + \
          ' --OutputFileFormat fbx --SPL ' + preset + \
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


# legacy code
# def send_to_simplygon(preset, type_reduce):
#     PRESET_PATH = posixpath.join(FILES_DIR, 'input', preset + '.spl')
#
#     # todo refactor
#     print('TYPE ', type_reduce)
#     lods_count = Settings.lods_calculate[1:]
#     lods_count = list(map(str, lods_count))
#     if type_reduce is 'Manual':
#         lods_count = Settings.lods_manual
#         print('TYPE_R', lods_count)
#
#     # edit_lods_spl(PRESET_PATH, lods_count)
#
#     cmd = SIMPLYGON_EXE + r' --Input ' + INPUT_FILES
#     cmd += ' --Output ' + OUTPUT_FILES
#     cmd += ' --OutputFileFormat fbx --Spl ' + PRESET_PATH
#     cmd += ' --Server ' + HOST + ':' + str(PORT) + ' --Verbose'
#     # todo
#     if check_socket():
#         os.system(cmd)
#     else:
#         return


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


def main_commands(start_lod, end_lod, type_reduce=None):
    # todo add argument proxy or crash or normal - integer value
    # type reduce - auto or manual
    # auto: by algorithm
    # get polycount from ui
    lod_list = utl.lods_coefficient(type_reduce)
    # print('\n\n\nLODS', lod_list)
    coefficient_list = lod_list[4:]
    # print('\n\n\nCOEF', coefficient_list)
    # get selection
    selection = cmds.ls(sl=True, l=True)

    export_data = utl.export_data(selection)
    # print('DATA \n', export_data, '\n', len(export_data))
    # utl.logging('EXPORT DATA', *export_data)
    # return
    # loop to every in export data
    for i in export_data:
        lod_1_coefficient = utl.coefficient_by_type(i)
        print(lod_1_coefficient)
        # get polycount exported
        # start_count = cmds.polyEvaluate(i, t=True)
        # children = cmds.listRelatives(i, ad=1, typ='transform', f=1)  # mesh??
        # if children:
        #     start_count = cmds.polyEvaluate(children, t=True)
        # print('START COUNT', start_count)

        lod1 = coefficient_list[0] * lod_1_coefficient
        # coeff to list and rounded to 3 digit after point
        spl_coefficient = [round(lod1, 3), round(coefficient_list[1], 3), round(coefficient_list[2], 3)]
        # print('LOD 1 COUNT', spl_coefficient)
        edit_preset_spl(LODS_PROXY_PRESET, spl_coefficient)

        # temp comment -----####
        # export to fbx
        export_selection(i)

        # generate batch command
        cmd = batch_command(LODS_PROXY_PRESET)
        utl.clear_folder(OUTPUT_FILES)
        execute_command(cmd)
        # temp comment -------####
        # todo inform user about process and progress

        # check loding is successfully otherwise repeat 10 times
        for index in range(10):
            if utl.exists_folder(OUTPUT_FILES) and os.listdir(OUTPUT_FILES):
                utl.in_viewport_massage('Reducing successfully')
                import_all_lods(i, start_lod, end_lod)
                break

            elif index == 10:
                print('Server is busy. repeat loding again')

            else:
                # todo inform user about failed
                pass
