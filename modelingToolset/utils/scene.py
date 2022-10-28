import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import modelingToolset.utils.std as std_u


def cleanup():
    selection = cmds.ls(sl=1, l=1, fl=1)
    mesh = None

    if ".f" in selection[0] or ".e" in selection[0] or ".vtx" in selection[0] or ".map" in selection[0]:
        mesh = selection[0].split(".")[0]

    cmds.selectMode(o=1, co=0)
    cmds.select(mesh)

    mel.eval(
        'polyCleanupArgList 4 { "0","1","0","0","0","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","1","0","0" };')

    cmds.selectMode(co=1, o=0)
    cmds.select(selection)


def getActiveCamera():
    try:
        pan = cmds.getPanel(wf=True)
        cam = cmds.modelPanel(pan, q=True, camera=True)
        camShape = cmds.listRelatives(cam, c=1, f=1)[0]
        return cam, camShape
    except:
        return None, None


def degreeToRad(degree):
    return degree * 0.0175


def getUVShells(uvList):
    shellData = []

    while uvList:
        cmds.select(uvList[0])
        mel.eval('polySelectBorderShell 0;')
        shell = cmds.ls(sl=1, l=1, fl=1)
        if shell:
            shellData.append(shell)

        uvList = std_u.removeList(uvList, shell)

    return shellData


def get_shader(obj):
    shader = None

    shape = obj

    try:
        shape = cmds.listRelatives(shape, c=1, type="mesh")[0]
    except:
        pass

    connections = cmds.listHistory(shape, f=1)

    for obj in connections:
        if cmds.nodeType(obj) == "shadingEngine":
            shader = cmds.listConnections(obj + ".surfaceShader")[0]

    return shader


def get_texture_File(obj, channel="color"):
    file_node = None

    shader = get_shader(obj)

    if shader:
        # get color connections
        incommingConnections = cmds.listConnections(shader + "." + channel)

        if not incommingConnections:
            return None

        file_node = incommingConnections[0]

    # bump specific feature
    if cmds.nodeType(file_node) == "bump2d":
        incommingConnections = cmds.listConnections(file_node + ".bumpValue")
        if not incommingConnections:
            return None
        file_node = incommingConnections[0]

    return file_node


def get_color_Place2dTexture(obj):
    place2DTexture_node = None

    file_node = get_texture_File(obj, channel="color")

    if not file_node:
        return None

    connections = list(set(cmds.listConnections(file_node, d=0, s=1)))

    if connections:
        place2DTexture_node = [i for i in connections if cmds.nodeType(i) == "place2dTexture"][0]

    return place2DTexture_node


def get_bump_Place2dTexture(obj):
    place2DTexture_node = None

    file_node = get_texture_File(obj, channel="normalCamera")

    if not file_node:
        return None

    connections = list(set(cmds.listConnections(file_node, d=0, s=1)))

    if connections:
        place2DTexture_node = [i for i in connections if cmds.nodeType(i) == "place2dTexture"][0]

    return place2DTexture_node
