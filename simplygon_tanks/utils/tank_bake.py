import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as omu
import os, shutil, re
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance


def mainWindowPointer():
    ptr = omu.MQtUtil.mainWindow()  # pointer for the main window
    return wrapInstance(long(ptr), QWidget)


def inViewMessage(msg_text):
    inViewMessageEnable = cmds.optionVar(q='inViewMessageEnable')
    if inViewMessageEnable == 0:
        cmds.optionVar(iv=('inViewMessageEnable', 1))
    cmds.inViewMessage(amg='<hl>Bake Texture: ' + msg_text, pos='botLeft', fade=True)

    if inViewMessageEnable == 0:
        cmds.optionVar(iv=('inViewMessageEnable', 0))


def sg_texture_pathes():
    texturesDir = mainWindowPointer().findChildren(QLineEdit, 'TextureDir')
    tracksFile = mainWindowPointer().findChildren(QLineEdit, 'TrackTextureFile')
    exeptionDir = mainWindowPointer().findChildren(QLineEdit, 'CrashTextureFile')
    textinline = texturesDir[0].text()
    trackinline = tracksFile[0].text()

    textinline = textinline.replace("//", "/")
    textinline = textinline.replace("\\", "/")

    trackinline = trackinline.replace("//", "/")
    trackinline = trackinline.replace("\\", "/")
    try:
        exeptinline = exeptionDir[0].text()
        exeptinline = exeptinline.replace("//", "/")
        exeptinline = exeptinline.replace("\\", "/")
    except:
        exeptinline = None
    print('TEXTURE PATHES', textinline, ' ', trackinline, ' ', exeptinline)
    return textinline, trackinline, exeptinline


class Utils2(object):
    def __init__(self):
        pass

    @classmethod
    def getFileInfo(cls):
        rawFilePath = cmds.file(q=True, exn=True)  # get file path
        fileName = cmds.file(q=True, sn=True, shn=True)  # get file name
        filePath = rawFilePath[:len(rawFilePath) - len(fileName)]  # correct file name
        projectPath = filePath[:len(filePath) - len(filePath.split("/")[-2]) - 1]
        return rawFilePath, fileName, filePath, projectPath

    @classmethod
    def getShader(cls, obj):
        result = []

        shape = obj

        try:
            shape = cmds.listRelatives(shape, c=1, type="mesh")[0]
        except:
            pass

        connections = cmds.listHistory(shape, f=1, ag=1)

        for obj in connections:
            if cmds.nodeType(obj) == "shadingEngine":
                result.append(cmds.listConnections(obj + ".surfaceShader")[0])

        return result

    @classmethod
    def getObjectType(cls, obj):
        objectType = None

        if "hull_01" in obj:
            return "hull_01"

        if "hull_01_2" in obj:
            return "hull_01_2"

        if "hull_01_3" in obj:
            return "hull_01_3"

        if "turret_01" in obj:
            # print 'OBJECT NAME', obj
            return "turret_01"

        if "turret_01_2" in obj:
            # print 'OBJECT NAME', obj
            return "turret_01_2"

        if "turret_01_3" in obj:
            # print 'OBJECT NAME', obj
            return "turret_01_3"

        if "turret_02" in obj:
            return "turret_02"

        if "turret_03" in obj:
            return "turret_03"

        if "chassis" in obj:
            return "chassis"

        else:
            return "gun"

    @classmethod
    def getMaterialType(cls, obj):
        # objectType = None
        if "hull_01" in obj and "hull_01_" not in obj:
            return "hull_01"

        if "hull_01_2" in obj:
            return "hull_01_2"

        if "hull_01_3" in obj:
            return "hull_01_3"

        if "turret_01" in obj and "turret_01_" not in obj:
            # print 'OBJECT NAME', obj
            return "turret_01"

        if "turret_01_2" in obj:
            return "turret_01_2"

        if "turret_01_3" in obj:
            return "turret_01_3"

        if "turret_02" in obj:
            return "turret_02"

        if "turret_03" in obj:
            return "turret_03"

        if "chassis" in obj:
            return "chassis"

        if "track" in obj:
            return "track"

        if "guns" in obj:
            return "gun"

        if "inside" in obj:
            return "inside"

        else:
            return None

    @classmethod
    def findShaderTexture(cls, textureList, textureType, material):
        ##################template dir
        dir = str(os.path.dirname(__file__))
        dir = dir.replace("\\", "\\\\")
        parentDir = os.path.dirname(dir)
        parentDir = os.path.dirname(parentDir)
        parentDir = os.path.dirname(parentDir)
        templateDir = os.path.dirname(parentDir) + "\\\\simplygonPresets\\\\cm256_template.tga"
        ##################
        for i in textureList:
            # print 'SEPARATE', material, ' ', i.lower(), ' ', textureType.lower()
            if material == 'track' and textureType.lower() in i.lower():
                # print 'RETURN I TRACK', i
                return i
            elif "hull_01" in material and "hull_01_2" not in material and "hull_01_3" not in material:
                if "hull_01" in i.lower() and "hull_01_2" not in i.lower() and "hull_01_3" not in i.lower() and textureType.lower() in i.lower():
                    # print 'RETURN I HULL BASE', i
                    return i
            elif "hull_01_2" in material:
                if "hull_01_2" in i.lower() and textureType.lower() in i.lower():
                    # print 'RETURN I HULL SECOND', i
                    return i

            elif "hull_01_3" in material:
                if "hull_01_3" in i.lower() and textureType.lower() in i.lower():
                    # print 'RETURN I HULL SECOND', i
                    return i

            elif "turret_01" in material and "turret_01_2" not in material and "turret_01_3" not in material:
                if "turret_01" in i.lower() and "turret_01_2" not in i.lower() and "turret_01_3" not in i.lower() and textureType.lower() in i.lower():
                    # print 'RETURN I HULL BASE', i
                    return i
            elif "turret_01_2" in material:
                if "turret_01_2" in i.lower() and textureType.lower() in i.lower():
                    # print 'RETURN I HULL SECOND', i
                    return i

            elif "turret_01_3" in material:
                if "turret_01_3" in i.lower() and textureType.lower() in i.lower():
                    # print 'RETURN I HULL SECOND', i
                    return i

            elif material in i.lower() and textureType.lower() in i.lower():
                # print 'RETURN I', i
                return i
            elif material == 'chassis' and textureType.lower() == '_cm':
                # print 'RETURN I_CM', i
                return templateDir
            elif (material == 'inside'):
                # print 'RETURN I_INSIDE', i
                return templateDir
        # elif matrial == 'inside'

    @classmethod
    def findObjectTexture(cls, textureList, textureType, obj):
        objectType = cls.getObjectType(obj)  # its turret / gun / hull / chassis

        for i in textureList:
            # print 'TXT IN LIST', i, objectType.lower(), textureType.lower()
            if objectType.lower() in i.lower() and textureType.lower() in i.lower():
                # print 'RETURN I', i
                return i
            elif objectType.lower() == 'chassis' and textureType.lower() == '_cm':
                dir = str(os.path.dirname(__file__))
                dir = dir.replace("\\", "\\\\")

                parentDir = os.path.dirname(dir)
                parentDir = os.path.dirname(parentDir)
                # parentDir = os.path.dirname(parentDir)
                i = os.path.dirname(parentDir) + "\\\\simplygonPresets\\\\cm256_template.tga"
                # print 'RETURN I_CM', i
                return i


class Baker(object):

    def __init__(self, obj=None, source=None, maping=False):
        self.parentObject = obj
        self.sourceObject = source
        self.mapping = maping
        self.processingObjects = []
        self.sourceObjectList = []
        self.targetSourceLinks = []
        self.textureList = []
        self.rawFilePath, self.fileName, self.filePath, self.projectPath = Utils2.getFileInfo()
        self.exportProxyPath = None

        self.pathText, self.trackText, self.crashText = sg_texture_pathes()

        self.getMeshData()  # gather source and target shapes into a list
        if self.mapping:
            self.autoMapLayout()  # auto-map projection for lod4
        cmds.file(save=1)

        self.prepareScene(
            self.sourceObjectList)  # initialize materials (delete all channels connections but Color, gather info about existing maps in originalTextures)
        if len(self.pathText) == 0 or len(self.trackText) == 0:
            cmds.confirmDialog(title='Textures', message='Set texture dirs', button=['I understand'],
                               defaultButton='Yes')
            return
        elif (len(self.pathText) == 0 and len(self.trackText) != 0) or (
                len(self.pathText) != 0 and len(self.trackText) == 0):
            cmds.confirmDialog(title='Textures', message='Set texture and track dirs or clear this',
                               button=['I understand'], defaultButton='Yes')
            return

        else:
            self.cycleBaking('original')
            self.matConnect()
            self.lod4MatConnect()

    def getMeshData(self):
        if self.parentObject is None: return None

        allMeshes = cmds.ls(type="mesh", l=1)

        for i in allMeshes:
            if self.parentObject in i:
                self.processingObjects.append(i)

            elif self.sourceObject in i:  # and not "havok" in i:
                self.sourceObjectList.append(i)

        self.processingObjects = list(set(self.processingObjects))
        self.sourceObjectList = list(set(self.sourceObjectList))

    def autoMapLayout(self):
        if self.parentObject == None: return None

        for i in self.processingObjects:
            cmds.polyAutoProjection(i, \
                                    layoutMethod=0, \
                                    projectBothDirections=0, \
                                    insertBeforeDeformers=1, \
                                    createNewMap=0, \
                                    layout=2, \
                                    scaleMode=1, \
                                    optimize=0, \
                                    planes=4, \
                                    percentageSpace=0.2, \
                                    worldSpace=0)

        cmds.delete(self.processingObjects, ch=1)
        cmds.select(self.processingObjects)

        cmds.polyMultiLayoutUV(layoutMethod=1, \
                               scale=2, \
                               rotateForBestFit=2, \
                               flipReversed=1, \
                               percentageSpace=0.2, \
                               layout=2, \
                               prescale=2, \
                               sizeU=1, \
                               sizeV=1, \
                               offsetU=0, \
                               offsetV=0)

        cmds.select(self.processingObjects)
        cmds.delete(ch=1)

        cmds.select(self.sourceObjectList)
        cmds.delete(ch=1)

    def prepareScene(self, listOfShapes=None):
        # delete extra connections
        for i in listOfShapes:
            connections = cmds.listHistory(i, f=1, ag=1)
            for obj in connections:
                if cmds.nodeType(obj) == "shadingEngine":
                    surfaceShader = cmds.listConnections(obj + ".surfaceShader")
                    if surfaceShader:
                        specularColorConnection = None
                        bumpMappingConnection = None
                        ambientColorConnection = None
                        try:
                            specularColorConnection = cmds.listConnections(surfaceShader[0] + ".specularColor")
                        except:
                            pass
                        if specularColorConnection:
                            cmds.disconnectAttr(specularColorConnection[0] + ".outColor",
                                                surfaceShader[0] + ".specularColor")
                        try:
                            bumpMappingConnection = cmds.listConnections(surfaceShader[0] + ".normalCamera")
                        except:
                            pass
                        if bumpMappingConnection:
                            cmds.disconnectAttr(bumpMappingConnection[0] + ".outNormal",
                                                surfaceShader[0] + ".normalCamera")
                        try:
                            ambientColorConnection = cmds.listConnections(surfaceShader[0] + ".ambientColor")
                        except:
                            pass
                        if ambientColorConnection:
                            cmds.disconnectAttr(ambientColorConnection[0] + ".outColor",
                                                surfaceShader[0] + ".ambientColor")

        # get all textures in a folder
        self.textureList = []

        for i in os.listdir(self.pathText):  # get all files in this folder
            # if "original" in i.lower(): #if we find "original"
            #	for (dirpath, dirnames, filenames) in os.walk(self.filePath + "/" + i): #walk through all files in scenePath/originaltextures
            # for x in filenames:
            if i.endswith(".tga") or i.endswith(".TGA"):
                path = self.pathText + "/" + i
                path = path.replace("//", "/")
                path = path.replace("\\", "/")
                self.textureList.append(path)

        for i in self.sourceObjectList:
            shader = Utils2.getShader(i)
            for shd in shader:
                colorConnections = cmds.listConnections(shd + ".color")
                if not colorConnections:
                    fileNode = cmds.createNode("file", name=shd + "_file")
                    cmds.connectAttr(fileNode + ".outColor", shd + ".color")

        '''
		####################################################
		#                  TRACK                           #
		####################################################
		'''
        self.textureTrackList = []
        allTexturesInDir = []
        tracktexture = self.trackText  # track texture from UI
        trackPath = os.path.dirname(tracktexture)  # dirs of texture
        nameTrack = os.path.basename(tracktexture)  # base name track texture without extention
        nameTrack = re.split('_[A-Z][A-Z].', nameTrack)  # root name track without type suffix

        '''
		# gather all textures in track dirs
		'''
        for i in os.listdir(trackPath):  # get all files in this folder
            if i.endswith(".tga") or i.endswith(".TGA"):
                path = trackPath + "/" + i
                path = path.replace("//", "/")
                path = path.replace("\\", "/")
                allTexturesInDir.append(path)  # get all textures

        for texture in allTexturesInDir:
            if nameTrack[0] in texture:
                self.textureTrackList.append(texture)  # got only track textures

        '''
		####################################################
		#                  END TRACK                       #
		####################################################
		'''

        '''
		####################################################
		#                  CRASH                           #
		####################################################
		'''
        self.textureCrashList = []

        for texture in self.textureList:
            if '_AO' in texture:
                self.textureCrashList.append(texture)  # got only AO textures

        '''
		####################################################
		#                  END CRASH                       #
		####################################################
		'''

    def copyTemplateMM(self):
        dir = str(os.path.dirname(__file__))
        dir = dir.replace("\\", "\\\\")
        parentDir = os.path.dirname(dir)
        parentDir = os.path.dirname(parentDir)
        parentDir = os.path.dirname(parentDir)
        MMTemplatePath = os.path.dirname(parentDir) + "\\\\simplygonPresets\\\\mm256_template.tga"
        if os.path.isfile(self.pathText + "/" + self.fileName[:-3] + "_proxy_MM.tga"):
            pass
        else:
            shutil.copy(MMTemplatePath, self.pathText)
            os.rename(self.pathText + "/mm256_template.tga", self.pathText + "/" + self.fileName[:-3] + "_proxy_MM.tga")

    def bakeCrash(self):
        sceneMaterials = cmds.ls(mat=1)
        for mat in sceneMaterials:
            # print 'MATERIAL', mat
            matType = Utils2.getMaterialType(mat)
            if matType:
                if matType == 'track':
                    matTexturePath = Utils2.findShaderTexture(self.textureCrashList, '_crash_AO', matType)
                    if not matTexturePath:
                        matTexturePath = Utils2.findShaderTexture(self.textureCrashList, '_AO', matType)
                    # print 'TEXTURE TRACK SHADER AO PATH', matTexturePath
                else:
                    matTexturePath = Utils2.findShaderTexture(self.textureCrashList, '_crash_AO', matType)
                    if not matTexturePath:
                        matTexturePath = Utils2.findShaderTexture(self.textureCrashList, '_AO', matType)
                    # print 'TEXTURE SHADER AO PATH', matTexturePath
                if matTexturePath:
                    fileNode = cmds.listConnections(mat + ".color")[0]
                    cmds.setAttr(fileNode + ".fileTextureName", matTexturePath, type="string")
                else:
                    continue
            else:
                continue

        self.bakeProcess('_AO')

    def bakePreset(self, template="_AM"):
        #
        #######################YURUS
        sceneMaterials = cmds.ls(mat=1)
        for mat in sceneMaterials:
            # print 'MATERIAL', mat
            matType = Utils2.getMaterialType(mat)
            # print 'MAT TYPE', matType
            if matType:
                if matType == 'track':
                    matTexturePath = Utils2.findShaderTexture(self.textureTrackList, template, matType)
                # print 'TEXTURE TRACK SHADER PATH', matTexturePath
                else:
                    matTexturePath = Utils2.findShaderTexture(self.textureList, template, matType)
                # print 'TEXTURE SHADER PATH', matTexturePath
                if matTexturePath:
                    fileNode = cmds.listConnections(mat + ".color")[0]
                    cmds.setAttr(fileNode + ".fileTextureName", matTexturePath, type="string")
                else:
                    continue
            else:
                continue

        self.bakeProcess(template)

    def bakeProcess(self, template="AM"):
        txtTarget = ""
        for i in self.processingObjects:
            txtTarget += "\n-target " + i + ' -uvSet map1 -searchOffset 0.1 -maxSearchDistance 0.4 -searchCage "" '

        txtSource = ""
        for i in self.sourceObjectList:
            txtSource += "\n-source " + i

        fileName = '\n-filename "' + self.pathText + "/" + self.fileName[:-3] + "_proxy" + template + '"'

        cmd = """surfaceSampler """ + txtTarget + txtSource + """
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
        # print 'CMD', cmd
        mel.eval(cmd)

    def cycleBaking(self, type_texture):
        if not self.processingObjects: return 1
        if not self.sourceObjectList: return 1

        '''
		#############################################
		#                CRASH                      #
		#############################################
		'''
        mayaFileName = cmds.file(q=True, sn=1, shn=1)
        fileName = mayaFileName.split('.')[0]
        if 'crash' in fileName:
            self.bakeCrash()

        #############################################
        #               END CRASH                   #
        #############################################
        #############################################
        #                NORMAL                     #
        #############################################
        else:
            self.bakePreset("_AM")
            self.bakePreset("_GM")
            self.bakePreset("_AO")
            self.bakePreset("_NM")

            try:
                self.bakePreset("_CM")
            except:
                pass
            try:
                self.bakePreset("_BM")
            except:
                pass
            try:
                self.bakePreset("_ID")
            except:
                pass
            try:
                self.bakePreset("_DM")
            except:
                pass
            self.copyTemplateMM()

            inViewMessage('Proxy texture baked')

    def textureLink(self, phong, path, extention):
        # check texture exist
        texture = path + extention
        if os.path.isfile(texture):
            # print 'Texture Path', texture
            # create file node and connect it to texture
            fileNode = cmds.shadingNode('file', asTexture=True, name=phong + "_file")
            cmds.setAttr(fileNode + ".fileTextureName", texture, type="string")
            place2d = ("place_" + fileNode)
            place2d = cmds.shadingNode('place2dTexture', asUtility=True, name=place2d)
            cmds.connectAttr(place2d + ".coverage", fileNode + ".coverage", f=True)
            cmds.connectAttr(place2d + ".translateFrame", fileNode + ".translateFrame", f=True)
            cmds.connectAttr(place2d + ".rotateFrame", fileNode + ".rotateFrame", f=True)
            cmds.connectAttr(place2d + ".mirrorU", fileNode + ".mirrorU", f=True)
            cmds.connectAttr(place2d + ".mirrorV", fileNode + ".mirrorV", f=True)
            cmds.connectAttr(place2d + ".stagger", fileNode + ".stagger", f=True)
            cmds.connectAttr(place2d + ".wrapU", fileNode + ".wrapU", f=True)
            cmds.connectAttr(place2d + ".wrapV", fileNode + ".wrapV", f=True)
            cmds.connectAttr(place2d + ".repeatUV", fileNode + ".repeatUV", f=True)
            cmds.connectAttr(place2d + ".offset", fileNode + ".offset", f=True)
            cmds.connectAttr(place2d + ".rotateUV", fileNode + ".rotateUV", f=True)
            cmds.connectAttr(place2d + ".outUV", fileNode + ".uv", f=True)
            cmds.connectAttr(place2d + ".outUvFilterSize", fileNode + ".uvFilterSize", f=True)

            if extention == 'AM.tga':
                cmds.connectAttr(fileNode + ".outColor", phong + ".color", f=True)
            if extention == 'AO.tga':
                cmds.connectAttr(fileNode + ".outColor", phong + ".ambientColor", f=True)
            if extention == 'GM.tga':
                cmds.connectAttr(fileNode + ".outColor", phong + ".specularColor", f=True)
            if extention == 'NM.tga':
                bumpNode = cmds.shadingNode('bump2d', asTexture=True, name=phong + "_bump")
                cmds.connectAttr(fileNode + ".outAlpha", bumpNode + ".bumpValue", f=True)
                cmds.setAttr(bumpNode + '.bumpInterp', 1)
                cmds.connectAttr(bumpNode + ".outNormal", phong + ".normalCamera", f=True)

    def lod4MatConnect(self):
        typeMat = ['AM.tga', 'AO.tga', 'GM.tga', 'NM.tga']
        texturesLod4 = self.pathText + "/" + self.fileName[:-3] + "_proxy_"
        for ext in typeMat:
            try:
                self.textureLink('tank_proxy', texturesLod4, ext)
            except:
                print('Textures ' + textureLink + ext + ' not exists')

        mel.eval('MLdeleteUnused;')

    def matConnect(self):
        mayaFileName = cmds.file(q=True, sn=1, shn=1)
        fileName = mayaFileName.split('.')[0]
        if 'crash' in fileName:
            fileName = fileName.split('_')[0]

        # pathText = self.directoryname.text()
        # print 'Path ', pathText
        materials = ["tank_chassis_01", "tank_guns", "tank_hull_01", "tank_hull_01_2", "tank_hull_01_3", "tank_hull_02",
                     "tank_hull_02_2", "tank_hull_03", "tank_turret_01", "tank_turret_01_2", "tank_turret_01_3",
                     "tank_turret_02", "tank_turret_03"]
        suffixes = ["_chassis_01_", "_guns_", "_hull_01_", "_hull_01_2_", "_hull_01_3_", "_hull_02_", "_hull_02_2_",
                    "_hull_03_", "_turret_01_", "_turret_01_2_", "_turret_01_3_",
                    "_turret_02_", "_turret_03_"]
        typeMat = ['AM.tga', 'AO.tga', 'GM.tga', 'NM.tga']

        # self.progressBar.setVisible(True)
        for index in range(len(materials)):
            try:
                if len(cmds.ls(materials)) != 0:
                    textureLink = self.pathText + "/" + self.fileName[:-3] + suffixes[index]
                    for ext in typeMat:
                        try:
                            self.textureLink(materials[index], textureLink, ext)
                        # print 'zzzzzzzzzzzZZZZZZZZZZzzzzzzzzzzzzzzzz\n', materials[index], textureLink
                        except:
                            print('Textures ' + textureLink + ext + ' not exists')
            except:
                print('Linkin texture to ' + materials[index] + ' failed')
