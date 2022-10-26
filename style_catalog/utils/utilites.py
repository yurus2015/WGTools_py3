# -*- coding: utf-8 -*-
import os.path
import re
import posixpath
import shutil
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omu
import maya.mel as mel
from PySide2.QtWidgets import *
import style_catalog.utils.photoshop as phs
reload(phs)

LAYER = 'Detached'
TMP_LAYER = 'Temp'
TMP_MATERIAL = 'temp_mat'
CURRENT_DIR = os.path.realpath(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
RESOURCE_DIR = posixpath.join(os.path.dirname(PARENT_DIR), 'resources')


# File actions


def copy_file(source, target):
    shutil.copy(source, target)
    if os.path.isdir(target):
        dst = posixpath.join(target, os.path.basename(source))
        return dst


def directory_exists(path):
    pass


def file_in_directories(root):
    # file_list = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
    file_list = [os.path.join(root, f) for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))]
    print('full name', file_list)
    return file_list


def filter_file_name(list_textures, pattern):
    pattern_textures = []
    for texture in list_textures:
        if pattern in texture:
            pattern_textures.append(texture)
    return pattern_textures


def get_pattern(file):
    base = os.path.basename(file)
    name = os.path.splitext(base)[0]
    pattern = re.split(r'_\D\D$', name)
    return pattern


def check_write_access(path):
    if not os.access(path, os.W_OK):
        in_view_message('ERROR: Access is denied')
        Settings.info_line.setText('ERROR: Access is denied')
        cmds.error()


def list_directories(root):
    directories_list = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
    print directories_list
    return directories_list


def create_folder(path, folder):
    directory = os.path.join(path, folder).replace("\\", "/")
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except:
            in_view_message('ERROR: Access is denied')
            Settings.info_line.setText('ERROR: Access is denied')
            return
    return directory


def choose_file(line_widget=None):
    maya_file = cmds.file(q=True, loc=True)
    file_path = os.path.dirname(maya_file)
    file_name = QFileDialog.getOpenFileName(None, 'Choose Texture', file_path, 'Image Files (*.tga)',
                                            options=QFileDialog.DontResolveSymlinks | QFileDialog.ReadOnly)
    if os.path.isfile(file_name[0]):
        texture_path = str(file_name[0])
        if 'NM' in texture_path:
            Settings.normal_map = texture_path
        if 'AM' in texture_path:
            Settings.albedo_map = texture_path

        line_widget.setText(texture_path)


def choose_directory(line_widget):
    path = QFileDialog.getExistingDirectory(None, 'Pick Export Folder')
    if path:
        Settings.export_path = path
        line_widget.setText(path)


def set_export_dir(nation, type):
    root = QFileDialog.getExistingDirectory(None, 'Pick Export Folder')
    if root:
        directories_list = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]


def load_fbx_plugin():
    if not cmds.pluginInfo('fbxmaya', query=True, l=True):
        cmds.loadPlugin('fbxmaya')


def button_chain_state(widget):
    state = widget.isChecked()
    Settings.chain = state
    print('state', Settings.chain)


def rename_selected(item, name):
    if item.lower() != name.lower():
        cmds.rename(item, name.lower())


def check_item_layer(layer):
    if cmds.objExists(layer):
        return True
    return


def create_item_layer(layer):
    layer_new = cmds.createDisplayLayer(name=layer, empty=True)
    return layer_new


def delete_layer(layer):
    if cmds.objExists(layer):
        if not cmds.editDisplayLayerMembers(layer, query=True):
            cmds.delete(layer)


def remove_members_from_layer(layer):
    items = cmds.editDisplayLayerMembers(layer, query=True)
    if items:
        if not check_item_layer(TMP_LAYER):
            create_item_layer(TMP_LAYER)
        add_item_layer(TMP_LAYER, items)

    return


def add_item_layer(layer, items):
    items = cmds.ls(items, l=True)
    cmds.editDisplayLayerMembers(layer, items, noRecurse=False)
    return


def visible_layers(switch):
    layers = cmds.ls(type='displayLayer')
    for layer in layers:
        if layer != LAYER and layer != 'defaultLayer':
            print('LLL', layer)
            cmds.setAttr(layer+'.visibility', switch)


def default_layer_items():
    meshes = cmds.ls(type='mesh')
    transform = cmds.listRelatives(meshes, p=True, typ='transform', f=True)
    default_layer_transforms = []
    for tr in transform:
        if not cmds.listConnections(tr, type='displayLayer'):
            default_layer_transforms.append(tr)

    return default_layer_transforms


def set_viewport(panel):
    print('Viewport 2.0')
    cmds.modelEditor(panel, e=True, rnm="vp2Renderer")


def hide_grid():
    if cmds.optionVar(q='showGrid'):
        cmds.grid(tgl=False)


def show_grid():
    cmds.grid(tgl=True)
    panels = cmds.getPanel(type='modelPanel')
    for panel in panels:
        cmds.modelEditor(panel, edit=True, grid=True)


def restore_state_grid():
    cmds.grid(tgl=cmds.optionVar(q='showGrid'))


def get_current_panel():
    panel = cmds.getPanel(withFocus=True)
    print(panel)
    panel_type = cmds.getPanel(to=panel)
    if panel_type == 'modelPanel':
        return panel_type
    else:
        return


def get_background_color():
    active_view = omu.M3dView.active3dView()
    background_color = active_view.backgroundColor()
    return background_color


def set_background_color(r, g, b):
    cmds.displayRGBColor('background', r, g, b)
    return


def in_view_message(msg):
    cmds.inViewMessage(amg='<hl>' + msg + '</hl>',
                       pos='botLeft', fade=True, fot=1000)


def align_face():
    print('Align face')
    selection = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selection)
    dag = om.MDagPath()
    component = om.MObject()
    selection.getDagPath(0, dag, component)
    normal = om.MVector()
    vectors = []
    if not component.isNull() and component.apiType() == om.MFn.kMeshPolygonComponent:
        # There were components selected
        face_itr = om.MItMeshPolygon(dag, component)
        while not face_itr.isDone():
            # Do stuff
            face_itr.getNormal(normal, om.MSpace.kWorld)
            normal.normalize()
            print('ops!', normal)
            vectors.append(normal)
            face_itr.next()

    if vectors:
        vector = om.MVector()
        for v in vectors:
            vector += v

        vector /= len(vectors)
        print('Vector', vector)

        world_original = om.MVector(0, 0, 0)


"""Detach functions"""


def detach_faces():
    bsp_face = cmds.filterExpand(ex=False, sm=34)
    if bsp_face:
        new_objects = []
        shape_object = cmds.ls(sl=True, fl=True, o=True, l=True)
        shape_object = cmds.ls(shape_object, s=1)
        for shape in shape_object:
            transform_object = cmds.listRelatives(shape, p=True, f=True)
            name_object = cmds.listRelatives(shape, p=True, f=False)
            duplicate_object = cmds.duplicate(transform_object, n=(name_object[0] + '_1'))
            duplicate_transform = cmds.listRelatives(duplicate_object, c=True, typ="transform", f=True)
            if duplicate_transform:
                cmds.delete(duplicate_transform)
            extension = []
            for face in bsp_face:
                if name_object[0] in face:
                    f = face.split('.', 1)
                    extension.append(duplicate_object[0] + '.' + f[1])
            face_object = cmds.ls(duplicate_object[0] + '.f[*]', fl=True)
            extension = cmds.ls(extension, fl=True)
            face_object = list(set(face_object) - set(extension))
            cmds.delete(face_object)
            new_objects.append(duplicate_object[0])
        cmds.delete(bsp_face)
        cmds.selectMode(object=True)
        cmds.select(new_objects)
        new_objects = cmds.ls(new_objects, l=True)
        return new_objects
    else:
        in_view_message('WARNING: Select faces that should be detached and separated')
        Settings.info_line.setText('WARNING: Select faces that should be detached and separated')
        cmds.error()


def isolate_selection():
    print('Isolate')
    panel = cmds.getPanel(withFocus=True)
    print(panel)
    panel_type = cmds.getPanel(to=panel)
    if panel_type == 'modelPanel':
        print(cmds.isolateSelect(panel, q=True, state=True))
        if not cmds.isolateSelect(panel, q=True, state=True):
            cmds.editor(panel, edit=True, lockMainConnection=True, mainListConnection='activeList')
            cmds.isolateSelect(panel, state=True)
        else:
            cmds.isolateSelect(panel, state=False)


def unparent(item):
    print('Item', item)
    try:
        item = cmds.parent(item, w=True)
    except Exception:
        pass

    return item


def move_to_world_origin(item):
    for i in item:
        bbox = cmds.exactWorldBoundingBox(i)
        bottom = [(bbox[0] + bbox[3]) / 2, bbox[1], (bbox[2] + bbox[5]) / 2]
        cmds.xform(i, piv=bottom, ws=True)
        cmds.move(0, 0, 0, i, rpr=True, absolute=True)
        cmds.makeIdentity(i, apply=True, t=1, r=1, s=1, n=0)


def fit_view():
    cmds.viewFit()


def detach_command():
    detached_object = detach_faces()
    detached_object = unparent(detached_object)
    move_to_world_origin(detached_object)
    fit_view()

    if check_item_layer(LAYER):
        remove_members_from_layer(LAYER)
    else:
        create_item_layer(LAYER)
    print('Detached', detached_object)
    add_item_layer(LAYER, detached_object)
    # default layer to temp
    non_layer_items = default_layer_items()
    print('NON', non_layer_items)
    if non_layer_items:
        if not check_item_layer(TMP_LAYER):
            create_item_layer(TMP_LAYER)
        add_item_layer(TMP_LAYER, non_layer_items)
    visible_layers(0)


'''End Detach'''


def set_align_tool():
    show_grid()
    cmds.setToolTo(cmds.snapTogetherCtx())
    in_view_message('USE: First click on face then press X and click somewhere on grid')
    Settings.info_line.setText('USE: First click on face then press X and click somewhere on grid')


'''Render'''


def set_render_resolution(width, height):
    cmds.setAttr('defaultResolution.pixelAspect', 1.0)
    cmds.setAttr('defaultResolution.width', width)
    cmds.setAttr('defaultResolution.height', height)


def set_camera_aov():
    cameras = cmds.ls(ca=True)
    for cam in cameras:
        cmds.camera(cam, e=1, hfv=38.0)
        # setAttr perspShape.horizontalFilmAperture ((`getAttr perspShape.verticalFilmAperture`)*1.5);


def get_color_node(meshes):
    # shading_group = cmds.listConnections(meshes[0], type='shadingEngine')
    material = get_material(meshes)
    color_node = cmds.listConnections(material + '.color', d=False, s=True)[0]
    return color_node


def get_material(meshes):
    shading_group = cmds.listConnections(meshes[0], type='shadingEngine')
    material = cmds.listConnections(shading_group[0] + '.surfaceShader')
    return material[0]


def render_image(type_image='color.png'):
    # render hw2
    file_render = cmds.ogsRender(w=1024, h=1024)
    # copy to resources dir
    image_render = copy_file(file_render, RESOURCE_DIR)
    # rename
    image_name = posixpath.join(RESOURCE_DIR, type_image)
    try:
        os.remove(image_name)
    except Exception:
        pass
    os.rename(image_render, image_name)
    return image_name


def render_command():
    meshes = cmds.ls(selection=True, dag=True, type="mesh", noIntermediate=True)
    if not meshes:
        in_view_message('WARNING: Select object for render')
        Settings.info_line.setText('WARNING: Select object for render')
        return

    mel.eval('setCurrentRenderer "mayaHardware2"')
    cmds.setAttr("hardwareRenderingGlobals.renderMode", 4)
    cmds.setAttr("defaultRenderGlobals.imageFormat", 32)

    try:
        file_node = get_color_node(meshes)
    except Exception:
        in_view_message('WARNING: Assign material')
        Settings.info_line.setText('WARNING: Assign material')
        return

    # set resolution
    # set_render_resolution(1024, 1024)
    # set angle of view
    set_camera_aov()

    # color
    color_image = render_image('color.png')
    Settings.color_render = color_image
    in_view_message('TIPS: Render color image')
    Settings.info_line.setText('TIPS: Render color image')

    # gray
    cmds.setAttr(file_node+'.disableFileLoad', 1)
    gray_image = render_image('gray.png')
    cmds.setAttr(file_node + '.disableFileLoad', 0)
    Settings.grey_render = gray_image
    in_view_message('TIPS: Render gray image')
    Settings.info_line.setText('TIPS: Render gray image')

    # import renders in photoshop if press chain button
    if Settings.chain:
        photoshop_command()


'''Photoshop'''


def photoshop_command():
    print('pathes', CURRENT_DIR, PARENT_DIR)
    # app, version = phs.running_photoshop()
    app = phs.run_photoshop()
    print('app', app)
    if app is None:
        in_view_message('WARNING: Run Photoshop')
        Settings.info_line.setText('WARNING: Run Photoshop')
        return
    else:
        in_view_message('TIPS: Photoshop Running')
        Settings.info_line.setText('TIPS: Photoshop Running')

    # copy template file to project dir
    project_path = Settings.export_path
    if project_path is None:
        in_view_message('WARNING: Set export directory')
        Settings.info_line.setText('WARNING: Set export directory')
        return
    psd = os.path.join(os.path.dirname(PARENT_DIR), 'resources/thumbnail.psd')
    template = copy_file(psd, project_path)
    print('TEMPLATE', template)

    # open copy file
    # phs.action_script(app, version, template, color_file=Settings.color_render)
    color_file = os.path.join(os.path.dirname(PARENT_DIR), 'resources/color.png')
    gray_file = os.path.join(os.path.dirname(PARENT_DIR), 'resources/gray.png')
    phs._action_script(app, template, color=color_file, gray=gray_file)


# add render image to layer


'''Material'''


def create_blinn(name):
    material = name.lower()
    shading_node = None
    if not cmds.objExists(name):
        material = cmds.shadingNode('blinn', asShader=True, name=name)
        shading_node = cmds.sets(name="%sSG" % name, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % shading_node)
        # cmds.defaultNavigation(connectToExisting=1, source=blinn_material, destination=shading_node)
        # cmds.sets(meshes, forceElement=shading_node)
    else:
        shading_node = cmds.listConnections(material, type='shadingEngine')
    return material, shading_node


def create_color_node(texture):
    texture_file = cmds.shadingNode('file', asTexture=True, name='item_file')
    cmds.setAttr('%s.fileTextureName' % texture_file, texture, type="string")
    node = cmds.shadingNode('place2dTexture', asUtility=True, n='item_2d')
    cmds.defaultNavigation(connectToExisting=1, source=node, destination=texture_file)
    return texture_file


def create_normal_node(texture):
    texture_file = create_color_node(texture)
    node = cmds.shadingNode('bump2d', asUtility=True, n='item_bump')
    cmds.defaultNavigation(connectToExisting=1, source=texture_file, destination=node)
    # alternative
    # connectAttr -f file1.outAlpha bump2d1.bumpValue;
    cmds.setAttr(node+'.bumpInterp', 1)
    return node


def shading_mode():
    set_render_resolution(1024, 1024)
    panels = cmds.getPanel(type='modelPanel')

    for panel in panels:
        cmds.modelEditor(panel, edit=True, displayAppearance='smoothShaded', displayTextures=True)
        set_viewport(panel)
        camera = cmds.modelPanel(panel, q=True, cam=True)
        show = cmds.getAttr(camera+'.displayResolution')
        if not cmds.getAttr(camera+'.orthographic'):
            cmds.setAttr(camera+'.displayResolution', not show)
            cmds.setAttr(camera+'.displayFilmGate', not show)
            cmds.setAttr(camera + '.overscan', 1.3)


def material_command():
    meshes = cmds.ls(selection=True, dag=True, type="mesh", noIntermediate=True)
    transform = cmds.ls(cmds.listRelatives(meshes, p=1))
    if not meshes:
        in_view_message('WARNING: Select object for assign material')
        Settings.info_line.setText('WARNING: Select object for assign material')
        return

    normal_map = Settings.normal_map
    albedo_map = Settings.albedo_map

    if not normal_map or not albedo_map:
        in_view_message('WARNING: Set path to texture')
        Settings.info_line.setText('WARNING: Set path to texture')
        return

    albedo_node = create_color_node(albedo_map)
    normal_node = create_normal_node(normal_map)

    material_node, shading_node = create_blinn(TMP_MATERIAL)

    cmds.connectAttr('%s.outColor' % albedo_node, '%s.color' % material_node, f=True)
    cmds.connectAttr('%s.outNormal' % normal_node, '%s.normalCamera' % material_node, f=True)

    cmds.sets(meshes, edit=True, forceElement=shading_node)
    cmds.select(transform)


def rename_material(mat, name):
    if cmds.objExists(name) and mat != name:
        cmds.delete(name)
        cmds.rename(mat, name)
        return
    if mat != TMP_MATERIAL:
        in_view_message('WARNING: Create/Assign material')
        Settings.info_line.setText('WARNING: Create/Assign material')
        cmds.error()
    else:
        cmds.rename(mat, name)


''' Export'''


def copy_textures(destination):
    texture = Settings.normal_map
    pattern = get_pattern(texture)[0]
    path = os.path.dirname(texture)
    all_textures = file_in_directories(path)
    filtered_texture = filter_file_name(all_textures, pattern)
    for file in filtered_texture:
        copy_file(file, destination)


def export_command(root_path):
    print('utils export', root_path)
    # load_fbx_plugin()
    # path = Settings.export_path
    Settings.export_path = root_path
    path = root_path
    name = Settings.name_object
    print('Name', name)
    if not path:
        in_view_message('WARNING: Set export directory')
        Settings.info_line.setText('WARNING: Set export directory')
        return

    if not name:
        in_view_message('WARNING: Set name object')
        Settings.info_line.setText('WARNING: Set name object')
        return

    check_write_access(path)

    items = cmds.ls(sl=True, tr=True, l=True)
    if items:


        cmds.select(items)

        try:
            meshes = cmds.ls(selection=True, dag=True, type="mesh", noIntermediate=True)
            material = get_material(meshes)
        except Exception:
            in_view_message('WARNING: Assign material')
            Settings.info_line.setText('WARNING: Assign material')
            return

        if len(items) > 1:
            items = cmds.group(items)
        else:
            items = items[0]

        rename_selected(items, name)
        capitalize_name = name.lower().capitalize()
        create_item_layer(capitalize_name)
        add_item_layer(capitalize_name, name)
        rename_material(material, name.lower()+'_mat')
        # cmds.rename(material, name.lower()+'_mat')

        # delete detached layer
        delete_layer(LAYER)

        # folders structure
        #
        # name folder
        path = create_folder(path, capitalize_name)

        # source and preview folders
        preview = create_folder(path, 'Preview')
        path = create_folder(path, 'Source')

        # model folder
        refs = create_folder(path, 'Refs')
        path = create_folder(path, 'Model')

        fbx_full_path = posixpath.join(path, capitalize_name + '.fbx')
        maya_full_path = posixpath.join(path, capitalize_name + '.mb')
        try:
            cmds.file(maya_full_path, force=True, pr=True, es=True, typ='mayaBinary')
        except:
            in_view_message('ERROR: Access is denied')
            Settings.info_line.setText('ERROR: Access is denied')
            cmds.error()
        cmds.file(fbx_full_path, force=1, options='v=0', typ='FBX export', pr=1, es=1)
        # copy_textures(path)

        in_view_message('TIP: Object exported')
        Settings.info_line.setText('TIP: Object exported')

    else:
        in_view_message('WARNING: Select object for export')
        Settings.info_line.setText('WARNING: Select object for export')
        return


class Settings():

    """ Texture Maps """
    normal_map = None
    albedo_map = None
    export_path = None
    name_object = None
    color_render = None
    grey_render = None
    chain = False
    info_line = None

    tools_help = 'Detach - отделяет выделенные полигоны \nот основного меша в отдельный объект\n\n' \
                 'Align - вызывает инструмент, позволяющий \nвыровнять обект от выделенного полигона\n' \
                 'к сетке (при нажатой клавише X)'

    material_help = 'Указать путь к текстурам: альбедо и нормал.\n' \
                    'Важно: текстуры должны содержать соответствующие индексы - AM и NM\n' \
                    'По кнопке создается материал с указанными текстурами и временным именем.\n' \
                    'Корректное имя материалу будет присвоено при экспорте в Fbx/Mb.'

    render_help = 'Кнопка фрейм отображает рамку в пределах которой рендерится объект\n\n' \
                  'Кнопка Render сохраняет цветную и серую версии рендеров во временную директорию\n\n' \
                  'Кнопка Send to PS открывает фотошоп с psd-темплейтом, в который загружаются рендеры\n\n' \
                  'Кнопка цепочка позволяет выполнить рендер и загрузки в фотошоп за одно действие'

    export_help = 'Необходимо добавить описание'
