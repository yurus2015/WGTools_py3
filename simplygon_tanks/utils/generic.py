import maya.cmds as cmds
import maya.mel
from importlib import reload
from maya.mel import eval as meval
import re
import os
import maya.OpenMayaUI as omu
# import sceneTools.importReplaceEditor as ire
# import tank_export.utils.importReplaceEditor as ire

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance


def mainWindowPointer():
    ptr = omu.MQtUtil.mainWindow()  # pointer for the main window
    return wrapInstance(long(ptr), QWidget)


import simplygon_tanks.utils.tank_reduce as tr

reload(tr)
import simplygon_tanks.utils.tank_bake as tb

reload(tb)
import simplygon_tanks.utils.tank_bake_2019 as tb_

reload(tb_)


def confirmDialog(text, do):
    result = cmds.confirmDialog(title='Tanks Simplygon', message=text, button=['   OK   ', 'Cancel'],
                                defaultButton='   OK   ', cancelButton='Cancel', dismissString='Cancel')
    if do == 'err':
        raise ValueError()
        return
    if result == '   OK   ':
        return True


def isCrash():
    mayaFileName = cmds.file(q=True, sn=1, shn=1)
    if '_crash' in mayaFileName.lower():
        return True
    else:
        return False


def isStyle():
    patern_style = re.compile('_\dDst')
    mayaFileName = cmds.file(q=True, sn=1, shn=1)
    if patern_style.findall(mayaFileName):
        return True
    else:
        return False


def emptyScene():
    if cmds.ls(type='mesh'):
        return True
    else:
        return False


def isTank():
    if cmds.ls('hull*') and cmds.ls('turret*'):
        return True
    else:
        return False


def isWeelsTank():
    tracks = cmds.ls("*track_*", l=1, tr=1)
    if tracks:
        return False
    else:
        return True


def removeList(fromList, thisList):
    resultList = [n for n in fromList if n not in thisList]
    resultList = list(resultList)
    return resultList


def removeDupplicateList(currentList):
    resultList = list(set(currentList))
    return resultList


def removeString(fromString, thisString):
    newstr = fromString.replace(thisString, "")
    return newstr


def nameCurrentFile():  # if 'untitled': return 0, if normal: return 1, if 'crash': return 2
    mayaFileName = cmds.file(q=True, sn=1, shn=1)
    if len(mayaFileName) < 1:
        return 0
    if '_crash' in mayaFileName.lower():
        return 2
    else:
        return 1


def closeWindow():
    if cmds.window("Simplygon", q=True, exists=True):
        cmds.deleteUI("Simplygon")


def sg_texture_pathes():
    texturesDir = mainWindowPointer().findChildren(QLineEdit, 'TextureDir')
    tracksFile = mainWindowPointer().findChildren(QLineEdit, 'TrackTextureFile')
    exeptionDir = mainWindowPointer().findChildren(QLineEdit, 'CrashTextureFile')
    textinline = texturesDir[0].text()
    trackinline = tracksFile[0].text()
    try:
        exeptinline = exeptionDir[0].text()
    except:
        exeptinline = None
    return textinline, trackinline, exeptinline


def valid_lods():
    valide_lod_list = ('lod0', 'lod1', 'lod2', 'lod3')
    lods = cmds.ls('lod*', tr=1)
    return_lods = removeList(valide_lod_list, lods)

    return return_lods


def sg_delete_lods():
    invalide_lod_list = ('lod1', 'lod2', 'lod3', 'lod4')
    for lod in invalide_lod_list:
        try:
            cmds.delete(lod)
        except:
            pass


def exist_createGroup(parentGroup):
    try:
        if cmds.objExists(parentGroup) == False:
            partGroup = cmds.group(em=True, name=parentGroup.split('|')[-1])
            cmds.parent(partGroup, parentGroup.split('|')[-2])
        return True
    except:
        return None


def sg_deleteNodes():
    noValidNodes = cmds.ls(type=['file', 'place2dTexture', 'bump2d', 'multiplyDivide'])
    if noValidNodes:
        cmds.delete(noValidNodes)


def sg_revertMat(toType):
    defaultShader = ['lambert1', 'particleCloud1']
    shaders = cmds.ls(mat=1)
    shaders = removeList(shaders, defaultShader)

    for shader in shaders:
        replaceWith = cmds.createNode(toType)
        meval('replaceNode ' + shader + ' ' + replaceWith)
        cmds.delete(shader)
        cmds.rename(replaceWith, shader)


def deleteCurrentLayers():
    displayLayers = cmds.ls(type="displayLayer", l=1)
    displayLayers.remove("defaultLayer")
    if displayLayers:
        cmds.delete(displayLayers)


def sg_objectLayersUtil():
    deleteCurrentLayers()
    displayLayers = []

    lodList = cmds.ls("*lod*", l=1, tr=1)

    if lodList:
        for lod in lodList:
            relatives = cmds.listRelatives(lod, c=1, f=1)
            for rel in relatives:
                if 'bsp' in rel:
                    l_name = rel.split("|")[-1]
                    layerName = (l_name.split('_bsp'))[0].title()

                elif 'inside' in rel:
                    layerName = 'Hull'

                else:
                    layerName = rel.split("|")[-1].title()  # object name lower case

                try:
                    if layerName not in displayLayers:  # at the beginning its actually empty
                        displayLayers.append(layerName)
                        cmds.createDisplayLayer(n=layerName, empty=1)
                    cmds.editDisplayLayerMembers(layerName, rel)
                except:
                    pass

    # sorting
    dLayers = cmds.ls(l=1, type="displayLayer")
    dLayers.remove("defaultLayer")

    layer_hull = []
    layer_turret = []
    layer_gun = []
    layer_chassis = []

    for layer in dLayers:
        if "Hull" in layer:
            layer_hull.append(layer)
        elif "Turret" in layer:
            layer_turret.append(layer)
        elif "Gun" in layer:
            layer_gun.append(layer)
        elif "Chassis" in layer:
            layer_chassis.append(layer)

    layer_hull = sorted(layer_hull, reverse=True)
    layer_turret = sorted(layer_turret, reverse=True)
    layer_gun = sorted(layer_gun, reverse=True)
    layer_chassis = sorted(layer_chassis, reverse=True)
    resultLayer = layer_chassis + layer_gun + layer_turret + layer_hull

    for idx, i in enumerate(resultLayer):
        objects = cmds.editDisplayLayerMembers(i, q=1, fn=1)
        cmds.delete(i)
        cmds.createDisplayLayer(n=i, empty=1)
        cmds.editDisplayLayerMembers(i, objects)
        cmds.setAttr(i + '.displayOrder', idx + 1)


def sg_reorderOutliner():
    lodList = cmds.ls("lod*", l=1, tr=1)
    lodList = sorted(lodList, reverse=True)

    hull = []
    turret = []
    gun = []
    chassis = []

    for lod in lodList:
        cmds.reorder(lod, f=1)
        children = cmds.listRelatives(lod, c=1, typ='transform')
        for child in children:
            if 'hull' in child:
                hull.append(child)
            if 'turret' in child:
                turret.append(child)
            if 'gun' in child:
                gun.append(child)
            if 'chassis' in child:
                chassis.append(child)
                fullPath = cmds.ls(child, l=1)
                chassisElements = cmds.listRelatives(fullPath, c=1, typ='transform', pa=1)
                chassisElements = sorted(chassisElements)
                for wheel in chassisElements:
                    cmds.reorder(wheel, f=1)

        hull = sorted(hull, reverse=True)
        turret = sorted(turret, reverse=True)
        gun = sorted(gun, reverse=True)
        chassis = sorted(chassis, reverse=True)

        resultList = chassis + gun + turret + hull
        resultList = cmds.ls(resultList, l=1)
        for element in resultList:
            cmds.reorder(element, f=1)

    camList = ['side', 'front', 'top', 'persp']
    for cam in camList:
        cmds.reorder(cam, f=1)


def sg_textureLink(blinn, path, extention):
    # check texture exist
    texture = path + extention
    if os.path.isfile(texture):
        # create file node and connect it to texture
        fileNode = cmds.shadingNode('file', asTexture=True, name=blinn + "_file")
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
            cmds.connectAttr(fileNode + ".outColor", blinn + ".color", f=True)
        if extention == 'AO.tga':
            cmds.connectAttr(fileNode + ".outColor", blinn + ".ambientColor", f=True)
        if extention == 'GM.tga':
            cmds.connectAttr(fileNode + ".outColor", blinn + ".specularColor", f=True)
        if extention == 'NM.tga':
            bumpNode = cmds.shadingNode('bump2d', asTexture=True, name=blinn + "_bump")
            cmds.connectAttr(fileNode + ".outAlpha", bumpNode + ".bumpValue", f=True)
            cmds.setAttr(bumpNode + '.bumpInterp', 1)
            cmds.connectAttr(bumpNode + ".outNormal", blinn + ".normalCamera", f=True)


def sg_matConnect():
    mayaFileName = cmds.file(q=True, sn=1, shn=1)
    fileName = mayaFileName.split('.')[0]
    if 'crash' in fileName:
        fileName = fileName.split('_crash')[0]

    pathText, trackText, crashText = sg_texture_pathes()

    materials = ["tank_chassis_01", "tank_guns", "tank_hull_01", "tank_hull_01_2", "tank_hull_02",
                 "tank_hull_02_2", "tank_hull_03", "tank_turret_01", "tank_turret_02", "tank_turret_03"]
    suffixes = ["_chassis_01_", "_guns_", "_hull_01_", "_hull_01_2_", "_hull_02_", "_hull_02_2_", "_hull_03_",
                "_turret_01_",
                "_turret_02_", "_turret_03_"]
    typeMat = ['AM.tga', 'AO.tga', 'GM.tga', 'NM.tga']

    for index in range(len(materials)):
        if len(cmds.ls(materials)) != 0:
            textureLink = pathText + '/' + fileName + suffixes[index]
            for ext in typeMat:
                sg_textureLink(materials[index], textureLink, ext)

    trackPath = os.path.dirname(trackText)
    nameTrack = os.path.basename(trackText)
    import re
    nameTrack = re.split('_[A-Z][A-Z].', nameTrack)
    track_mat = ['track_mat_L', 'track_mat_R']
    texLink = trackPath + '/' + nameTrack[0]

    for index in range(len(track_mat)):
        try:
            if len(cmds.ls(track_mat)) != 0:
                texLink = trackPath + '/' + nameTrack[0] + '_'
                for ext in typeMat:
                    try:
                        sg_textureLink(track_mat[index], texLink, ext)
                    except:
                        print('Textures ' + textLink + ext + ' not exists')
        except:
            print('Linkin texture to ' + track_mat[index] + ' failed')


def sg_to_wg():
    lods = valid_lods()

    # get all object
    mesh_objects = cmds.listRelatives(cmds.ls(type='mesh', l=1), f=1, p=1)
    transform_objects = removeDupplicateList(mesh_objects)
    for lod in lods:
        cmds.group(em=True, name=lod)
        upperName = lod.upper()
        for transform in transform_objects:
            if upperName in transform:
                # parent group
                parentGroup = cmds.listRelatives(transform, p=1)
                if 'hull' in parentGroup[0] or 'turret' in parentGroup[0] or 'chassis' in parentGroup[0]:
                    if exist_createGroup(lod + '|' + parentGroup[0]):
                        relocateTransform = cmds.parent(transform, lod + '|' + parentGroup[0])
                else:  # guns
                    relocateTransform = cmds.parent(transform, lod)

                validName = removeString(relocateTransform[0], '_' + upperName)
                validName = validName.split('|')[-1]

                cmds.rename(relocateTransform[0], validName)


def load_uv_border_plugins():
    currentVersion = cmds.about(v=1)
    if '2014' in currentVersion:
        if not cmds.pluginInfo('techartAPI2014', query=True, l=True):
            try:
                cmds.loadPlugin('techartAPI2014')
            except:
                raise MissingPluginError('Unable to load techartAPI2014.mll!')

    if '2016 Extension 2' in currentVersion:
        if not cmds.pluginInfo('techartAPI2016ext2', query=True, l=True):
            try:
                cmds.loadPlugin('techartAPI2016ext2')
            except:
                raise MissingPluginError('Unable to load techartAPI2016ext2.mll!')

    if '2018' in currentVersion:
        if not cmds.pluginInfo('techartAPI2018', query=True, l=True):
            try:
                cmds.loadPlugin('techartAPI2018')
            except:
                raise MissingPluginError('Unable to load techartAPI2018.mll!')


def load_Simplygon_plugins():
    pluginList = cmds.pluginInfo(query=True, listPlugins=True)
    currentVersion = cmds.about(v=1)
    if '2014' in currentVersion:
        if not cmds.pluginInfo('SimplygonMaya2014Release64', query=True, l=True):
            try:
                cmds.loadPlugin('SimplygonMaya2014Releasex64')
            except:
                cmds.confirmDialog(title='Simplygon plugin', message='Simplygon plugin not installed',
                                   button=['I undestand'], defaultButton='Yes')
                raise MissingPluginError('Unable to load SimplygonMaya2014Releasex64.mll!')
    if '2016 Extension 2' in currentVersion:
        if not cmds.pluginInfo('SimplygonMaya2014Release64', query=True, l=True):
            try:
                cmds.loadPlugin('SimplygonMaya2016Extension2Releasex64')
            except:
                cmds.confirmDialog(title='Simplygon plugin', message='Simplygon plugin not installed',
                                   button=['I undestand'], defaultButton='Yes')
                raise MissingPluginError('Unable to load techartAPI2016ext2.mll!')

    if '2018' in currentVersion:
        if not cmds.pluginInfo('SimplygonMaya2018Releasex64', query=True, l=True):
            try:
                cmds.loadPlugin('SimplygonMaya2018Releasex64')
            except:
                cmds.confirmDialog(title='Simplygon plugin', message='Simplygon plugin not installed',
                                   button=['I undestand'], defaultButton='Yes')
                raise MissingPluginError('Unable to load SimplygonMaya2018Releasex64.mll!')


# pass
def importProxy():
    ire.main()


def proxy_generate():
    lod4 = cmds.ls('|lod4', tr=1)
    if lod4:
        cmds.delete(lod4)
    instance = tr.AutoSimplygon(proxy=True)


def restoreSmoothGroup():
    load_uv_border_plugins()
    objList = cmds.ls(typ='mesh')
    transformList = cmds.listRelatives(objList, type='transform', p=True, f=1)
    for o in transformList:
        if 'lod0' in o:
            pass
        else:
            lod0_object = re.sub('lod\d', "lod0", o)
            cmds.select(o)
            cmds.polyNormalPerVertex(ufn=1)
            cmds.polySoftEdge(o, a=180, ch=0)
            cmds.select(o)
            mapBorders = meval('selectUVBorderEdge -uve')
            cmds.select(mapBorders)
            mapBorders = cmds.filterExpand(sm=32)
            try:
                cmds.polySoftEdge(mapBorders, a=66, ch=1)
            except:
                pass
            cmds.select(o)
            cmds.delete(ch=1)

            if cmds.objExists(lod0_object):
                print('Transfer from ' + lod0_object + ' to ' + o)
                try:
                    cmds.transferAttributes(lod0_object, o, transferPositions=0, transferNormals=1, transferUVs=0,
                                            transferColors=0, sampleSpace=0, searchMethod=0,
                                            flipUVs=0, colorBorders=1)
                except:
                    pass
            else:
                print('Object ' + lod0_object + ' dont exist. Skip transfer')
                continue

    try:
        lod4 = cmds.listRelatives('|lod4', ad=1, type='transform', f=1)
        for l in lod4:
            cmds.polySoftEdge(l, a=180)
            cmds.delete(l, ch=1)
        cmds.select(d=1)
    except:
        pass

    cmds.select(transformList)
    cmds.polyNormalPerVertex(ufn=1)
    cmds.delete(ch=1)
    cmds.select(d=1)


def tank_scene():
    sg_revertMat('blinn')
    sg_deleteNodes()
    sg_matConnect()
    sg_to_wg()
    sg_objectLayersUtil()
    sg_reorderOutliner()


def tank_reduce(coeffs):
    selection = cmds.ls(sl=1, l=1, tr=1)
    instance = tr.AutoSimplygon(selection, coeffs)


def tank_bake():
    selection = cmds.ls(sl=1, l=1, fl=1)
    instance = tb.Baker(obj="lod4", source="lod0", maping=False)

    if selection:
        try:
            cmds.select(selection)
        except:
            pass
    else:
        cmds.select(d=1)


def tank_bake_2019():
    # selection = cmds.ls(sl=1, l=1, fl=1)
    instance = tb_.TransferMaps()


# instance.list_textures()

def only_reduce():
    load_Simplygon_plugins()
    lod0, lod1, lod2, lod3, cf1, cf2, cf3 = polycountCompute()
    tank_reduce([lod1, lod2, lod3, cf1, cf2, cf3])
    load_uv_border_plugins()
    restoreSmoothGroup()
    tank_scene()

    cmds.ogs(p=1)
    cmds.ogs(p=1)


def common_reduce():
    load_Simplygon_plugins()
    c1, c2, c3 = manualReduce()
    lod0, lod1, lod2, lod3, cf1, cf2, cf3 = polycountCompute(c1, c2, c3)
    tank_reduce([lod1, lod2, lod3, cf1, cf2, cf3])
    load_uv_border_plugins()
    restoreSmoothGroup()
    tank_scene()


def manualReduce():
    widgets = QApplication.instance().allWidgets()
    for x in widgets:
        if 'Simplygon_Wnd' in str(x.__class__):
            o1, o2, o3 = x.returnManualValue()
            try:
                o1, o2, o3 = int(o1), int(o2), int(o3)
                return o1, o2, o3
            except:
                confirmDialog('Values in the Manual row isn`t correct', 'err')


def only_bake():
    tank_bake()
    cmds.ogs(p=1)
    cmds.ogs(p=1)


def create_lodsGroup():
    lods = ('lod1', 'lod2', 'lod3')
    tracks = cmds.ls('lod0|chassis*|track*', tr=1, l=1)
    print('Tracks', tracks)
    if tracks:
        for lod in lods:
            grp = cmds.group(em=True, name=lod)
            chassis = cmds.group(em=True, name='chassis_01')
            chassis = cmds.parent(chassis, grp)
            track_n = cmds.duplicate(tracks)
            track_n = cmds.parent(track_n, chassis)
            cmds.rename(track_n[0], 'track_L')
            cmds.rename(track_n[1], 'track_R')
            cmds.select(d=1)
    else:
        confirmDialog('Tracks in lod0 don`t exist', 'err')


def create_hierarchy():
    lods = cmds.ls('|lod*', tr=1, l=1)
    predefine_lods = ('|lod0')
    remainLods = removeList(lods, predefine_lods)
    if remainLods:
        result = confirmDialog('Lods 1-4 exists. Delete them?', 'make')
        if result:
            cmds.delete(remainLods)
            create_lodsGroup()
    else:
        create_lodsGroup()


def checkTracksLod():
    lod0_tracks = []
    lod1_tracks = []
    lod2_tracks = []
    lod3_tracks = []
    lods = cmds.ls('|lod0', '|lod1', '|lod2', '|lod3', tr=1)
    for lod in lods:
        if 'lod0' in lod:
            children = cmds.listRelatives(lod, ad=1, typ='transform', f=1)
            for child in children:
                if 'track_' in child:
                    lod0_tracks.append(child)
                else:
                    pass

        if 'lod1' in lod:
            children = cmds.listRelatives(lod, ad=1, typ='transform', f=1)
            for child in children:
                if 'track_' in child:
                    lod1_tracks.append(child)
                else:
                    pass

        if 'lod2' in lod:
            children = cmds.listRelatives(lod, ad=1, typ='transform', f=1)
            for child in children:
                if 'track_' in child:
                    lod2_tracks.append(child)
                else:
                    pass

        if 'lod3' in lod:
            children = cmds.listRelatives(lod, ad=1, typ='transform', f=1)
            for child in children:
                if 'track_' in child:
                    lod3_tracks.append(child)
                else:
                    pass

    return lod0_tracks, lod1_tracks, lod2_tracks, lod3_tracks


def polycountCompute(*args):
    count1 = 18000.0
    if isStyle():
        count1 = 22000.0
    count2 = 10000.0
    count3 = 5000.0
    print('args ', args)
    if args:
        count1 = args[0]
        count2 = args[1]
        count3 = args[2]

    lod0_hull_turret = []
    turrets = []
    lod0_gun_chassis = []
    guns = []
    tracks0, tracks1, tracks2, tracks3 = checkTracksLod()
    lod0 = cmds.ls('|lod0', tr=1)

    children = cmds.listRelatives(lod0[0], c=1, typ='transform', f=1)
    grand_children = cmds.listRelatives(lod0[0], ad=1, typ='mesh', f=1)
    grand_children = cmds.listRelatives(grand_children, p=1, typ='transform', f=1)
    for child in children:
        if 'hull_' in child:
            lod0_hull_turret.append(child)
        if 'turret_' in child:
            mesh = cmds.filterExpand(child, sm=12)
            count = cmds.polyEvaluate(mesh, t=1)
            turrets.append([child, count])
        if 'gun_' in child:
            count = cmds.polyEvaluate(child, t=1)
            guns.append([child, count])

    for child in grand_children:
        if 'chassis' in child and 'track_' not in child:
            lod0_gun_chassis.append(child)

    if guns:
        guns = sorted(guns, key=lambda guns: guns[1])
        lod0_gun_chassis.append(guns[-1][0])

    if turrets:
        turrets = sorted(turrets, key=lambda turrets: turrets[1])
        lod0_hull_turret.append(turrets[-1][0])

    lod0_hull_turret = cmds.filterExpand(lod0_hull_turret, sm=12, fp=1)
    lod0_hull_turret_cnt = cmds.polyEvaluate(lod0_hull_turret, t=1)
    lod0_gun_chassis = cmds.filterExpand(lod0_gun_chassis, sm=12, fp=1)
    lod0_gun_chassis_cnt = cmds.polyEvaluate(lod0_gun_chassis, t=1)
    tracks_lod0 = cmds.filterExpand(tracks0, sm=12, fp=1)
    tracks_lod1 = cmds.filterExpand(tracks1, sm=12, fp=1)
    tracks_lod1_cnt = cmds.polyEvaluate(tracks_lod1, t=1)
    tracks_lod2 = cmds.filterExpand(tracks2, sm=12, fp=1)
    tracks_lod2_cnt = cmds.polyEvaluate(tracks_lod2, t=1)
    tracks_lod3 = cmds.filterExpand(tracks3, sm=12, fp=1)
    tracks_lod3_cnt = cmds.polyEvaluate(tracks_lod3, t=1)

    coef1 = 1.0
    coef2 = 1.0
    coef3 = 1.0

    baseLod0_polycount = 0.3 * lod0_hull_turret_cnt + 0.4 * lod0_gun_chassis_cnt
    try:
        cfc1 = (count1 - tracks_lod1_cnt) / baseLod0_polycount
        if args:
            coef1 = cfc1
        elif cfc1 < 1.0:
            coef1 = cfc1
        lod1_auto_count = baseLod0_polycount * coef1 + tracks_lod1_cnt
        lod1_without_tracks = baseLod0_polycount * coef1

    except:
        if tracks0:
            lod1_auto_count = 'No tracks'
        else:
            cfc1 = count1 / baseLod0_polycount
            if args:
                coef1 = cfc1
            elif cfc1 < 1.0:
                coef1 = cfc1
            lod1_auto_count = baseLod0_polycount * coef1

    try:
        cfc2 = (count2 - tracks_lod2_cnt) / (0.5 * lod1_without_tracks)
        if args:
            coef2 = cfc2
        elif cfc2 < 1.0:
            coef2 = cfc2

        lod2_auto_count = 0.5 * lod1_without_tracks * coef2 + tracks_lod2_cnt
        lod2_without_tracks = lod2_auto_count - tracks_lod2_cnt
    except:
        if tracks0:
            lod2_auto_count = 'No tracks'
        else:
            cfc2 = count2 / (0.5 * lod1_auto_count)
            if args:
                coef2 = cfc2
            elif cfc2 < 1.0:
                coef2 = cfc2
            lod2_auto_count = 0.5 * lod1_auto_count * coef2

    try:
        cfc3 = (count3 - tracks_lod3_cnt) / (0.5 * lod2_without_tracks)
        if args:
            coef3 = cfc3
        elif cfc3 < 1.0:
            coef3 = cfc3

        lod3_auto_count = 0.5 * lod2_without_tracks * coef3 + tracks_lod3_cnt
        lod3_without_tracks = lod3_auto_count - tracks_lod3_cnt
    except:
        if tracks0:
            lod3_auto_count = 'No tracks'
        else:
            cfc3 = count3 / (0.5 * lod2_auto_count)
            if args:
                coef3 = cfc3
            elif cfc3 < 1.0:
                coef3 = cfc3
            lod3_auto_count = 0.5 * lod2_auto_count * coef3

    # return
    if tracks_lod0:
        polyTrackLod0 = cmds.polyEvaluate(tracks_lod0, t=1)
    else:
        polyTrackLod0 = 0
    lod0_auto_count = lod0_hull_turret_cnt + lod0_gun_chassis_cnt + polyTrackLod0

    return lod0_auto_count, lod1_auto_count, lod2_auto_count, lod3_auto_count, coef1, 0.5 * coef2, 0.5 * coef3
