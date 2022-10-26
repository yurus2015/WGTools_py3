import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as omu
import os
import re
import posixpath

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

PATTERN = ['chassis', 'guns', 'hull_\d+_?\d', 'turret_\d+_?\d']
MAYAMATERIAL = ['lambert1', 'particleCloud1']
SUFIXES = ['_AM', '_GM', '_AO', '_NM', '_MM', '_CM', '_BM', '_ID', '_DM']
DIR = posixpath.join(os.path.dirname(os.path.realpath(__file__)), '').replace(os.sep, '/')
BAKEFILE = posixpath.join(DIR, 'bake_batch.py')


class TransferMaps(object):
    def __init__(self):
        self.texturePath = Utils.textures_dir()
        self.trackPath = Utils.track_textures_dir()
        self.check_pathes()

        self.original_textures = Utils.find_textures_tga(self.texturePath)
        self.track_textures = Utils.find_track_textures(self.trackPath)

        self.materials = Utils.list_materials()
        self.legacy_materials = Utils.legacy_materials()
        self.custom_materials = Utils.custom_materials()
        self.track_materials = Utils.track_materials()

        self.source_objects = Utils.getMeshData('lod0')
        self.target_objects = Utils.getMeshData('lod4')
        self.pair_mat, self.pair_txt = self.mat_texture_list()

        cmds.file(save=True)
        self.bake_batch(self.source_objects, self.target_objects, self.pair_mat, self.pair_txt)

        Utils.create_proxy_material()
        Utils.assign_texture(self.texturePath)

    def mat_texture_list(self):
        pair_mat = []
        pair_txt = []
        for text in self.original_textures:
            for mat in self.legacy_materials:
                for ptrn in PATTERN:
                    find = re.findall(ptrn, text)
                    if find and re.findall(ptrn, text) == re.findall(ptrn, mat):
                        pair_mat.append(mat)
                        pair_txt.append(text.split('_AM.')[0])

            for mat in self.custom_materials:
                if mat in text:
                    pair_mat.append(mat)
                    pair_txt.append(text.split('_AM.')[0])

        for mat in self.track_materials:
            if self.track_textures:
                pair_mat.append(mat)
                pair_txt.append(self.track_textures[0].split('_AM.')[0])

        return pair_mat, pair_txt

    def check_pathes(self):
        if not self.texturePath:
            Utils.confirmDialog('Set texture path', 'Warning', 'Ok')
            return
        if not self.trackPath:
            Utils.confirmDialog('Set track texture path', 'Warning', 'Ok')
            return

    def check_materials(self):
        mat_without_textures = []
        if self.legacy_materials:
            for mat in self.legacy_materials:
                if not Utils.check_legacy_mat_textures(mat, self.original_textures):
                    mat_without_textures.append(mat)

        if self.custom_materials:
            for mat in self.custom_materials:
                if not Utils.check_custom_mat_textures(mat, self.original_textures):
                    mat_without_textures.append(mat)
        return mat_without_textures

    def bake_batch(self, sources, targets, materials, textures):
        ts = ','.join([str(x) for x in targets])
        ss = ','.join([str(x) for x in sources])
        mt = ','.join([str(x) for x in materials])
        tx = ','.join([str(x) for x in textures])

        filename = Utils.returnFileName()
        filename += '_proxy'
        name = posixpath.join(self.texturePath, filename)

        checkers = Utils.suffix_check()
        for sfx in range(len(SUFIXES)):
            if checkers[sfx]:
                self.threadingBake(ss, ts, mt, tx, name, SUFIXES[sfx])

    def connect_textures(self, materials, textures, suffix):
        legacy_materials = materials.split(',')
        legacy_textures = textures.split(',')

        for i in range(len(legacy_materials)):
            texture_name = legacy_textures[i] + suffix + '.tga'
            if os.path.isfile(texture_name):
                try:
                    fileNode = cmds.listConnections(legacy_materials[i] + ".color")
                    if fileNode:
                        fileNode = fileNode[0]
                    else:
                        fileNode = cmds.shadingNode('file', asTexture=True, name=legacy_materials[i] + "_file")
                        cmds.connectAttr(fileNode + ".outColor", legacy_materials[i] + ".color", f=True)
                    cmds.setAttr(fileNode + ".fileTextureName", texture_name, type="string")

                except Exception:
                    pass

    def threadingBake(self, sources, targets, materials, textures, name, suffix):
        sources = sources.split(',')
        targets = targets.split(',')

        target_txt = ""
        for i in targets:
            target_txt += "\n-target " + i + ' -uvSet map1 -searchOffset 0.1 -maxSearchDistance 1.4 -searchCage "" '

        sources_txt = ""
        for i in sources:
            sources_txt += "\n-source " + i

        fileName = '\n-filename "' + name + suffix + '"'
        cmd = """surfaceSampler """ + target_txt + sources_txt + """
				-mapOutput diffuseRGB
				-mapWidth 256
				-mapHeight 256
				-max 1
				-mapSpace tangent
				-mapMaterials 1
				-shadows 1 """ + fileName + """
				-fileFormat "tga"
				-superSampling 2
				-filterType 0
				-filterSize 3
				-overscan 1
				-searchMethod 0
				-useGeometryNormals 1
				-ignoreMirroredFaces 0
				-flipU 0
				-flipV 0;
			"""
        self.connect_textures(materials, textures, suffix)
        mel.eval(cmd)


class Utils(object):
    def __init__(cls):
        pass

    @classmethod
    def removeString(cls, fromList, thisList):
        if thisList:
            resultList = [n for n in fromList if n not in thisList]
            resultList = list(resultList)
        else:
            resultList = fromList
        return resultList

    @classmethod
    def confirmDialog(cls, message, title, label):
        cmds.confirmDialog(title=title, message=message, button=[label], defaultButton='Yes')

    @classmethod
    def mainWindowPointer(cls):
        ptr = omu.MQtUtil.mainWindow()  # pointer for the main window
        return wrapInstance(long(ptr), QWidget)

    @classmethod
    def textures_dir(cls):
        texturesDir = cls.mainWindowPointer().findChildren(QLineEdit, 'TextureDir')[0].text()
        return texturesDir

    @classmethod
    def track_textures_dir(cls):
        tracksFile = cls.mainWindowPointer().findChildren(QLineEdit, 'TrackTextureFile')[0].text()
        return tracksFile

    @classmethod
    def suffix_check(cls):
        checkers = []
        for suffix in SUFIXES:
            checker = cls.mainWindowPointer().findChildren(QCheckBox, suffix)[0].isChecked()
            checkers.append(checker)
        return checkers

    @classmethod
    def find_textures_tga(cls, path):
        textures_list = []
        for i in os.listdir(path):  # get all files in this folder
            if i.lower().endswith(".tga") and '_am' in i.lower():
                current_path = posixpath.join(path, i)
                textures_list.append(current_path)
        return textures_list

    @classmethod
    def find_track_textures(cls, path):
        textures_list = []
        track_path = os.path.dirname(path)  # dirs of texture
        name_track = os.path.basename(path)  # base name track texture without extention
        name_track = re.split('_[A-Z][A-Z]\.', name_track)[0]  # name track without type
        track_textures = cls.find_textures_tga(track_path)
        for texture in track_textures:
            if name_track in texture:
                textures_list.append(texture)
        return textures_list

    @classmethod
    def list_materials(cls):
        materials = cmds.ls(mat=1)
        materials_all = cls.removeString(materials, MAYAMATERIAL)
        return materials_all

    @classmethod
    def legacy_materials(cls):
        legacy_materials = []
        materials = cls.list_materials()
        for mat in materials:
            for patern in PATTERN:
                if re.findall(patern, mat):
                    legacy_materials.append(mat)
        return legacy_materials

    @classmethod
    def track_materials(cls):
        track_mat = []
        materials = cls.list_materials()
        for mat in materials:
            if 'track' in mat:
                track_mat.append(mat)
        return track_mat

    @classmethod
    def custom_materials(cls):
        materials = cls.list_materials()
        legacy_materials = cls.legacy_materials()
        custom_materials = cls.removeString(materials, legacy_materials)
        return custom_materials

    @classmethod
    def check_custom_mat_textures(cls, mat, textures):
        valid = False
        for texture in textures:
            if mat in texture:
                valid = True
                break
        return valid

    @classmethod
    def check_legacy_mat_textures(cls, mat, textures):
        valid = False
        for patern in PATTERN:
            find = re.findall(patern, mat)
            print('mat_\n', find)
            if find:
                for texture in textures:
                    if find[0] in texture:
                        print('re\n', texture)
                        break
        return valid

    @classmethod
    def current_scene_path(cls):
        fileName = cmds.file(query=True, sn=True)
        return fileName

    @classmethod
    def returnFileName(cls):
        file_name = cmds.file(query=True, sn=1, shn=True)
        name = os.path.splitext(file_name)[0]
        return name

    @classmethod
    def getMeshData(cls, lod):
        processingObjects = []
        allMeshes = cmds.ls(type="mesh", l=1)
        for i in allMeshes:
            if lod in i:
                processingObjects.append(i)
        processingObjects = list(set(processingObjects))
        return processingObjects

    @classmethod
    def create_proxy_material(cls):
        material_proxy = cmds.ls('tank_proxy', mat=1)
        if not material_proxy:
            cmds.shadingNode("blinn", asShader=True, n='tank_proxy')
            sg = cmds.sets(renderable=1, noSurfaceShader=1, empty=1, name='tank_proxySG')
            cmds.connectAttr(('tank_proxy' + '.outColor'), (sg + '.surfaceShader'), f=1)
        lod4 = cmds.ls('lod4', tr=1)
        sg = cmds.listConnections('tank_proxy', t="shadingEngine")[0]
        cmds.sets(lod4, e=True, forceElement=sg)

    @classmethod
    def assign_texture(cls, texture_path):
        filename = cls.returnFileName()
        filename += '_proxy_AM.tga'
        name = posixpath.join(texture_path, filename)
        fileNode = cmds.shadingNode('file', asTexture=True, name="proxy_file")
        cmds.setAttr(fileNode + ".fileTextureName", name, type="string")
        cmds.connectAttr(fileNode + ".outColor", 'tank_proxy' + ".color", f=True)
