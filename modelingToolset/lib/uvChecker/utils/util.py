import yaml
import os.path
import maya.cmds as cmds
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *


# def read_yaml(path, content):
#     data_file = os.path.join(path, 'data.yaml')
#     print('File:', data_file)
#     with open(data_file) as f:
#         data = yaml.load(f, Loader=yaml.FullLoader)
#         if data:
#             print(data[content])
#             return data[content]
#         else:
#             return None


# openai
# This function takes in the filepath of the YAML file as an argument,
# opens the file and uses the safe_load function from the yaml library to parse the file
# and return the resulting dictionary.
def read_yaml_ai(path: str) -> dict:
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def write_yaml(path, icons_list):
    data_file = os.path.join(path, 'data.yaml')
    data = dict(icons=icons_list)
    with open(data_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def set_path(path):
    """
    Opens a file dialog and sets the file text box to the chosen track texture.
    """
    filename = QFileDialog.getOpenFileName(None, 'Choose Camouflage texture', path, "Image Files (*.tga)",
                                           options=QFileDialog.DontResolveSymlinks | QFileDialog.ReadOnly)
    if os.path.isfile(filename[0]):  # avoids problems if <Cancel> was selected
        return filename[0]


def change_image_size(texture_path, icon_path):
    pixmap = QPixmap(texture_path)
    icon = pixmap.scaled(128, 128, Qt.KeepAspectRatio)
    icon.save(icon_path)


def selected():
    meshes = cmds.filterExpand(sm=12, fp=1)
    if meshes:
        return meshes
    else:
        cmds.confirmDialog(title='Select meshes', message='Select polygonal mesh', button=['Yes'], defaultButton='Yes')


def create_checker_node():
    check_node = cmds.ls('checker_file')
    check_node2d = cmds.ls('checker_2d')

    if check_node:
        file = check_node[0]
    else:
        file = cmds.shadingNode('file', asTexture=True, name="checker_file")

    if check_node2d:
        node_2d = check_node2d[0]
    else:
        node_2d = cmds.shadingNode('place2dTexture', asUtility=1, n='checker_2d')
        cmds.setAttr(node_2d + ".repeatUV.repeatU", 4)
        cmds.setAttr(node_2d + ".repeatUV.repeatV", 4)
    # repeatUV
    if not cmds.isConnected(node_2d + ".repeatUV", file + ".repeatUV"):
        cmds.defaultNavigation(connectToExisting=1, source=node_2d, destination=file)

    return file, node_2d


def take_shaders(mesh):
    shader_engines = cmds.listConnections(cmds.listHistory(mesh), type='shadingEngine')
    materials = cmds.ls(cmds.listConnections(shader_engines), materials=True)

    return materials


def take_texture_file(materials):
    texture = []
    for mat in materials:
        texture_node = cmds.listConnections(mat + ".color", type="file")
        if texture_node:
            texture.append(texture_node[0])
        else:
            texture.append(None)
    return texture


def connect_texture_materials(textures, materials, checker_node):
    for i in range(len(materials)):
        if textures[i] is None:
            if not cmds.isConnected(checker_node + ".outColor", materials[i] + ".color"):
                cmds.connectAttr(checker_node + ".outColor", materials[i] + ".color", force=1)

        elif textures[i] != checker_node:
            if not cmds.isConnected(checker_node + ".outColor", textures[i] + ".colorGain"):
                cmds.connectAttr(checker_node + ".outColor", textures[i] + ".colorGain", force=1)
            if not cmds.isConnected(checker_node + ".outColor", textures[i] + ".colorOffset"):
                cmds.connectAttr(checker_node + ".outColor", textures[i] + ".colorOffset", force=1)
            cmds.setAttr(textures[i] + ".disableFileLoad", 1)


def connect_texture_file_2(texture, checker_node):
    cmds.setAttr(checker_node + '.fileTextureName', texture, type='string')


def iteration(checker_2dnode, repeat_count):
    if repeat_count:
        cmds.setAttr(checker_2dnode + ".repeatUV.repeatU", repeat_count)
        cmds.setAttr(checker_2dnode + ".repeatUV.repeatV", repeat_count)


def rotate_node(node2d, revers=False):
    rotate = cmds.getAttr(node2d + ".rotateFrame")
    if revers:
        if rotate == 0:
            cmds.setAttr(node2d + ".rotateFrame", 90)
        else:
            cmds.setAttr(node2d + ".rotateFrame", 0)
    else:
        cmds.setAttr(node2d + ".rotateFrame", 0)


def uv_link(meshes, uvset=None, texture=None):
    for mesh in meshes:
        indexes = cmds.polyUVSet(mesh, q=True, allUVSetsIndices=True)
        print('UVSETS', indexes, texture, uvset)
        for indx in indexes:
            print(type(indx), type(uvset))
            print(mesh + '.uvSet[' + str(indx) + '].uvSetName')
            if uvset == str(indx):
                print(mesh + '.uvSet[' + str(indx) + '].uvSetName', texture)
                cmds.uvLink(uvSet=mesh + '.uvSet[' + str(indx) + '].uvSetName', texture=texture)


def restore():
    check_node = cmds.ls('checker_file')
    check_node2d = cmds.ls('checker_2d')
    check_node.extend(check_node2d)
    try:
        cmds.delete(check_node)
    except:
        pass
    all_file_nodes = cmds.ls(type='file')
    for f in all_file_nodes:
        cmds.setAttr(f + ".disableFileLoad", 0)


# todo refactor
def assign_checker_texture(tile=None, iterator=None, uvset=None):
    selected_mesh = selected()
    if not selected_mesh:
        return

    print('dim', iterator, uvset)
    checker_node, checker_2d = create_checker_node()
    assigned_shaders = take_shaders(selected_mesh)
    texture_nodes = take_texture_file(assigned_shaders)
    connect_texture_materials(texture_nodes, assigned_shaders, checker_node)
    if tile:
        connect_texture_file_2(tile, checker_node)
    iteration(checker_2d, iterator)
    uv_link(selected_mesh, uvset, texture_nodes[0])
    cmds.select(selected_mesh)
