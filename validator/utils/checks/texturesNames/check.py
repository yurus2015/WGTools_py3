import maya.cmds as cmds
import re, posixpath
import os
import struct
from validator.utils.validator_API import *

checkId = 43
checkLabel = "8.7 Check names of textures"


def file_path():
    scene_file_path = cmds.file(q=True, exn=True)
    scene_file_path = os.path.dirname(scene_file_path)
    return scene_file_path


def textures_in_folder(folder, extension):
    textures_list = []
    extension_list = []
    size_list = []
    for file in os.listdir(folder):
        if extension == '.dds' and (file.endswith('.mb') or file.endswith('.fmt')):
            pass

        elif file.endswith(extension):
            texture_name = os.path.splitext(file)[0]
            textures_list.append(texture_name)

            valid_size = dimensions_texture(folder, file, extension)
            if valid_size:
                size_list.append(file)

        else:
            extension_list.append(file)

    return textures_list, extension_list, size_list


def dimensions_texture(path, file, extension):
    sizes = [256, 512, 1024, 2048, 4096]
    full_path = os.path.join(path, file)
    w, h = image_size(full_path, extension)
    w_check = False
    h_check = False
    for size in sizes:
        if w == size:
            w_check = True
        if h == size:
            h_check = True
    if not w_check or not h_check:
        return True


def image_size(file_path, extension):
    # ext = extensionFile(file_path)
    with open(file_path) as input:
        h = -1
        w = -1
        if extension == '.tga':
            data = input.read(25)
            w = struct.unpack("h", data[12:14])
            h = struct.unpack("h", data[14:16])
        if extension == '.dds':
            data = input.read(25)
            w = struct.unpack("i", data[16:20])
            h = struct.unpack("i", data[12:16])

        width = w[0]
        height = h[0]

        return width, height


def main():
    returnList = []
    textures_list = []
    black_list = []

    tank_name = vl_original_tank_name()
    if not tank_name:
        returnList.append(['No valid scene`s name', ''])
        return returnList

    scene_path = file_path()
    extension = '.tga'
    original_textures_path = False
    print('path ', scene_path.lower())
    if '/fin' in scene_path.lower():  # this foder must have a Original_Textures dir
        for file in os.listdir(scene_path):
            if file.lower() == 'original_textures':
                original_textures_path = posixpath.join(scene_path, file)
                break

    if '/export' in scene_path.lower():
        original_textures_path = scene_path
        extension = '.dds'

    if original_textures_path:
        textures_list, black_list, size_list = textures_in_folder(original_textures_path, extension)

        if black_list:
            for x in black_list:
                tmp = []
                tmp.append(x + ' - incorrect extension')
                tmp.append(x)
                returnList.append(tmp)

        if size_list:
            for x in size_list:
                tmp = []
                tmp.append(x + ' - incorrect texture dimensions')
                tmp.append(x)
                returnList.append(tmp)

    if not original_textures_path:
        tmp = []
        tmp.append("There is not 'Fin' or 'Export' folder, or 'Fin' folder  hasn`t an 'Original_textures' folder")
        tmp.append("")
        returnList.append(tmp)

    txtValidNames = vl_tank_textures_names(tank_name)
    for x in range(len(textures_list)):
        valid = 0
        for y in txtValidNames:
            temp = y.search(textures_list[x])
            if temp != None:
                valid = 1
            if textures_list[x].find("track") != -1:
                prefixtank_name = textures_list[x].split("track")[0]
                correctName = tank_name + "_" + textures_list[x][len(prefixtank_name):]
                temp = y.search(correctName)
                if temp != None:
                    valid = 1

        if valid == 0:
            tmp = []
            tmp.append(textures_list[x] + ' - incorrect name')
            tmp.append(textures_list[x])
            returnList.append(tmp)

    return returnList
