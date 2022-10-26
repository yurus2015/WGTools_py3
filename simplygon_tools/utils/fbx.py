import maya.cmds as cmds
from maya.mel import eval as meval
import os
import re
import posixpath
from simplygon_tools.utils.utilites import Settings
import simplygon_tools.utils.utilites as utl
import subprocess

CURRENT_DIR = os.path.realpath(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
FILES_DIR = posixpath.join(PARENT_DIR, 'files')
IMPORT_PRESET = posixpath.join(FILES_DIR, 'import_preset.fbximportpreset')
EXPORT_FILE = posixpath.join(FILES_DIR, 'input', 'export.fbx')
OUTPUT_DIR = posixpath.join(FILES_DIR, 'output')
SIMPLYGON = posixpath.join(FILES_DIR, 'SimplygonBatch.exe')
HOST = '10.128.2.240'
PORT = 55001


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
    preset_path = '/'.join(IMPORT_PRESET.split('\\'))
    print('preset', preset_path)
    meval('FBXLoadImportPresetFile -f "' + preset_path + '";')


def export_selection(selection):

    print('export manual', Settings.lods_manual)
    print('export auto', Settings.lods_calculate)
    load_import_preset()

    # todo validate
    selection = cmds.ls(sl=True)

    # todo check
    # detach textures
    node_material = utl.clear_textures()
    # full_export_path = posixpath.join(FILES_DIR, 'export.fbx')
    cmds.file(EXPORT_FILE, f=True, options='v=0', typ='FBX export', pr=1, es=1)

    # assign textures
    utl.reassign_textures(node_material)

    # import_lods()
    # cmd = SIMPLYGON + r' ' \
    #       r'--Input ' + EXPORT_FILE + ' ' \
    #       r'--Output ' + OUTPUT_DIR + ' ' \
    #       r'--OutputFileFormat fbx ' \
    #       r'--Spl d:\ART_MAIN\game\bin\tools\devtools\maya\simplygon\input\Evgeniy.spl ' \
    #       r'--Server 10.128.2.240:55001 ' \
    #       r'--Verbose'
    # os.system(r'd:\ART_MAIN\game\bin\tools\devtools\maya\simplygon\SimplygonBatch.exe '
    #           '--Input d:\ART_MAIN\game\bin\tools\devtools\maya\simplygon\input\chassis.fbx '
    #           '--Output d:\ART_MAIN\game\bin\tools\devtools\maya\simplygon\output '
    #           '--OutputFileFormat fbx --Spl d:\ART_MAIN\game\bin\tools\devtools\maya\simplygon\input\Evgeniy.spl '
    #           '--Server 10.128.2.240:55001 --Verbose')
    # result = os.system(cmd)

    # data = subprocess.check_output(cmd, shell=False)
    # print('RESULT: ', result)


def edit_lods_spl(preset_path, lods_count):  # lods_count, example ['5000', '2500', '1000'] or ['', '2500', '']
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
    for idx, x in enumerate(lods_count):
        if lods_count[idx].isdigit():
            print('F', lods_count[idx])
            new_lod_count = lods_count[idx]
            lods_line[idx][0] = re.sub(r"\d+", new_lod_count, lods_line[idx][0])
            print('Final_line', lods_line[idx][0])
            data[lods_line[idx][1]] = lods_line[idx][0]

    with open(preset_path, 'w') as file:
        file.writelines(data)


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
                      r'--Server ' + HOST + ':' + str(PORT) + ' ' \
                      r'--Verbose'

    # todo
    if check_socket():
        os.system(cmd)
    else:
        return


def import_lods():
    full_import_path = posixpath.join(FILES_DIR, 'export.fbx')
    cmds.file(full_import_path, i=True, add=True,
              type='FBX', iv=True,
              mnc=False, pr=True,
              ra=True, rdn=True,
              namespace=':')


def main_commands(type_reduce):
    # get polycount
    # get selection
    selection = cmds.ls(sl=True)
    # export selection to fbx
    export_selection(selection)
    # delete previous simplygon`s lods
    if utl.exists_folder(OUTPUT_DIR):
        utl.clear_folder(OUTPUT_DIR)
    # edit xml preset
    # send to simplygon
    send_to_simplygon('proxy', type_reduce)
    # check valid generation lods
    # import simplygon`s lods
    # reconstruct scene - name, layers etc.
    pass
