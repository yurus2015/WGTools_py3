import glob
import os
import posixpath
import re
import shutil
import xml.etree.ElementTree as ElementTree

import maya.cmds as cmds
from PySide2.QtCore import *
from PySide2.QtGui import *

OBJECTTYPE = {'rw': 'Railway',
              'mle': 'MilitaryEnvironment',
              'mil': 'MillitaryInstallations',
              'bld': 'Buildings',
              'blr': 'BuildingsRare',
              'env': 'Environment',
              'gaf': 'GatesAndFences',
              'han': 'Hangars',
              'out': 'Outland',
              'dec': 'Decor',
              'prfb': '01_PrefabElements',
              'exp': 'Experimental_Models',
              'char': 'Characters'
              }

CONTENT = 'res/wot/content'
CONTENT_CW = 'res/wot/content_cw'
CONTENT_PREFIX = ['hd_', 'cw_']
REGION = ['CN', 'RU', 'NA', 'ASIA', 'CT']
BSP = 'bsp', 'wall', 'ramp'


class Utils:
    def __init__(self):
        pass

    @classmethod
    def load_visual_plugin(cls):
        if not cmds.pluginInfo('visual', query=True, l=True):
            try:
                cmds.loadPlugin('visual')
            except OSError:
                cls.confirm_console('Unable to load visual.mll!', False, True)
                raise MissingPluginError('Unable to load visual.mll!')

        path_plugin = cmds.pluginInfo('visual', query=True, p=True)
        path_plugin = os.path.dirname(path_plugin)
        cls.confirm_console('Plugin loaded', False, False)

        return path_plugin

    @classmethod
    def load_option_var(cls):
        current_branch = list_branches = None
        if cmds.optionVar(exists='current_branch'):
            current_branch = cmds.optionVar(q='current_branch')
        else:
            cmds.optionVar(sv=('current_branch', str(current_branch)))

        if cmds.optionVar(exists='list_branches'):
            list_branches = cmds.optionVar(q='list_branches')
        else:
            cmds.optionVar(sva=('list_branches', list_branches))

        return list_branches

    @classmethod
    def save_option_var(cls, path, delete=None):
        # delete path from combobox
        if delete:
            pathes = cmds.optionVar(q='list_branches')
            index = pathes.index(path)
            cmds.optionVar(rfa=('list_branches', index))
            return

        # add path to combobox
        if not delete:
            cmds.optionVar(sva=('list_branches', path))
            return

        # set selection path
        if delete is None:
            cmds.optionVar(sv=('current_branch', path))

    @classmethod
    def same_link(cls, link):
        links = cmds.optionVar(q='list_branches')

        for n in links:
            print('LNK', n, link)
            if n == link:
                return True
        return False

    @classmethod
    def remove_list(cls, fromList, thisList):
        result_list = [n for n in fromList if n not in thisList]
        result_list = list(result_list)
        return result_list

    @classmethod
    def copy_file_to(cls, source_dir, destination_dir, region=None):
        files = glob.iglob(os.path.join(source_dir, '*.*'))

        for file in files:
            if os.path.isfile(file) and region and region not in file:
                shutil.copy2(file, destination_dir)

    @classmethod
    def rename_file(cls, path, name, region, extension):
        original = posixpath.join(path, name + '.' + extension)
        region_name = posixpath.join(path, name + '.' + region + '.' + extension)

        # delete region file if exist
        cls.delete_file(region_name)
        os.rename(original, region_name)

    @classmethod
    def delete_file(cls, filename):
        try:
            os.remove(filename)
        except OSError:
            pass

    @classmethod
    def compare_visuals(cls, original, region):
        if os.path.isfile(original):
            vis_doc = ElementTree.parse(original)
            original_handle = open(original, "wb")
            metadata = vis_doc.find('metaData')

            if not metadata:
                region_doc = ElementTree.parse(region)
                region_handle = open(region, "wb")
                reg_metadata = region_doc.find('metaData')
                if reg_metadata:
                    if reg_metadata[0]:
                        reg_metadata.remove(reg_metadata[0])
                region_doc.write(region_handle, xml_declaration=False)
                region_handle.close()

            vis_doc.write(original_handle, xml_declaration=False)

    @classmethod
    def delete_history(cls):
        cmds.delete(ch=1, all=1)

    @classmethod
    def file_name(cls):
        file_name = cmds.file(query=True, sn=1, shn=True)
        name = os.path.splitext(file_name)[0]
        cls.log("File name:", name)
        return name

    @classmethod
    def file_path(cls):
        file_name = cmds.file(query=True, loc=True)
        return os.path.dirname(file_name)

    @classmethod
    def region(cls):
        file_path = cls.file_path()
        region = None
        for reg in REGION:
            realm_reg = posixpath.join('_realm', reg)
            if realm_reg in file_path:
                region = reg
                break
        return region

    @classmethod
    def log(cls, message="", value=None):
        print("[Log]: ", str(message), ' ', str(value))
        pass

    @classmethod
    def confirm_dialog(cls, message_string):
        win_name = "messageBox"
        if cmds.window(win_name, exists=True):
            cmds.deleteUI(win_name)
        win = cmds.window(win_name, title='Warning')
        result = cmds.confirmDialog(title='Warning',
                                    message=message_string,
                                    button=['Ok'],
                                    defaultButton='Ok',
                                    cancelButton='No',
                                    dismissString='No')

        return result

    @classmethod
    def content_path(cls):
        path_plugin = cls.load_visual_plugin()
        x = 1
        path_content = None
        while x is not 0:
            if re.findall('[A-Z]:/$', path_plugin):
                cls.log("RES directories not found")
                x = 0
            else:
                subfolders = os.walk(path_plugin).next()[1]
                if subfolders:
                    for sf in subfolders:
                        if 'res' == sf:
                            path_content = posixpath.join(path_plugin, CONTENT)

                            if 'cw_' in cls.file_name():
                                path_content = posixpath.join(path_plugin, CONTENT_CW)
                            x = 0
                            break
                path_plugin = os.path.dirname(path_plugin)

        cls.log("Content export path:", str(path_content))

        return path_content

    @classmethod
    def content_link(cls, link):
        file_name = cls.file_name()
        # todo check 'content' in path, if not - warning
        content_path = link
        if link.count('content'):
            before_content = link.split('content')[0]
            content_path = posixpath.join(before_content, 'content')
            if 'cw_' in file_name:
                content_path = posixpath.join(before_content, 'content_cw')

        return content_path

    @classmethod
    def create_export_dir(cls, typ, lod, external_path):
        file_name = cls.file_name()
        content_folder = cls.content_link(external_path)
        type_folder = cls.group_type()
        name_folder = 'hd_' + file_name
        for sfx in CONTENT_PREFIX:
            if sfx in file_name:
                name_folder = file_name
        if 'prfb' in name_folder:
            name_folder = name_folder.split('prfb_')[1]

        export_folder = posixpath.join(content_folder, type_folder, name_folder, typ, lod)
        cls.create_folder(export_folder)
        return export_folder

    @classmethod
    def create_folder(cls, path):
        if not os.path.exists(path):
            os.makedirs(path)

    @classmethod
    def delete_folder(cls, path):
        try:
            import shutil
            shutil.rmtree(path, ignore_errors=True)
        except OSError:
            pass

    @classmethod
    def path_exists(cls, path):
        if os.path.exists(path):
            return True
        return False

    @classmethod
    def bsp_layer_visible(cls):
        layers = cmds.ls(type='displayLayer')
        for layer in layers:
            if 'bsp' in layer.lower():
                try:
                    cmds.setAttr(layer + '.visibility', 1)
                except OSError:
                    pass
        cls.confirm_console('Layers set visible', False, False)

    @classmethod
    def group_type(cls):
        file_name = cls.file_name()
        typ = re.search(r'...\W*', file_name)
        for sfx in CONTENT_PREFIX:
            typ_sfx = re.search(sfx + r'...\W*', file_name)
            if typ_sfx:
                typ = typ_sfx
                break

        for key, value in OBJECTTYPE.items():
            if key in typ.group():
                return value

    @classmethod
    def object_type(cls, obj):
        object_dag = cmds.listRelatives(obj, c=True, f=True)[0]  # get object child[0]
        if cmds.nodeType(object_dag) == 'mesh':  # if it's low level transform node
            return 'mesh'
        else:
            if 'lod' in obj:  # ??? object has fullPathName, lod in this path anyway
                return 'lod'
            elif cmds.nodeType(object_dag) == 'transform':
                return 'object'

    @classmethod
    def hp_world(cls):
        hp_dag = cmds.ls('HP*', assemblies=True, l=True)
        return hp_dag

    @classmethod
    def hp_world_selected(cls):
        hp_dag = cmds.ls('HP*', assemblies=True, sl=True, l=True)
        return hp_dag

    @classmethod
    def hp_group(cls, node):
        obj_dag = cmds.listRelatives(node, c=True, typ='transform', f=True)
        hp = [s for s in obj_dag if "HP" in s]
        return hp

    @classmethod
    def obj_parent(cls, obj):
        parent = cmds.listRelatives(obj, p=True, f=True, typ='transform')
        return parent

    @classmethod
    def mesh_in_lod(cls, node):
        obj_dag = cmds.listRelatives(node, c=True, typ='transform', f=True)
        # cls.log("Children: " + str(objDag))
        return obj_dag

    @classmethod
    def lods_in_obj(cls, obj):
        lods = []
        elements = cls.mesh_in_lod(obj)
        for i in elements:
            if 'lod' in i:
                lods.append(i)
        return lods

    @classmethod
    def lods_in_scene(cls):
        lods = []
        world_dag = cmds.ls(assemblies=True, l=True)
        for i in world_dag:
            typ = cls.object_type(i)
            if typ and typ != 'mesh':  # this group
                export_lod = cls.lods_in_obj(i)
                lods.extend(export_lod)

        return lods

    @classmethod
    def bsp_in_scene(cls, node):
        bsp = []
        children = cmds.listRelatives(node, c=True, typ='transform', f=True)
        for r in BSP:
            for i in children:
                if r in i:
                    bsp.append(i)
        return bsp

    @classmethod
    def merged_split(cls, name):
        typ = 'normal'
        if 'merged' in name:
            typ = 'merged'
            name = name.split('_merged')[0]

        return typ, name

    @classmethod
    def clear_textures(cls):
        material_node = cmds.ls(mat=1)
        node_material_struct = {}
        for node in material_node:
            connected_attrs = cmds.listConnections(node, d=0, s=1, c=1)
            if connected_attrs:
                connected_attrs = connected_attrs[::2]
                for attr in connected_attrs:
                    plug_attr = cmds.connectionInfo(attr, sfd=True)
                    node_material_struct[attr] = plug_attr

        if node_material_struct:
            for i in node_material_struct:
                cmds.disconnectAttr(node_material_struct[i], i)
            cls.confirm_console('Textures detached', False, False)

        return node_material_struct

    @classmethod
    def reassign_textures(cls, node_material_struct=None):
        if not node_material_struct:
            return
        for i in node_material_struct:
            cmds.connectAttr(node_material_struct[i], i)
        cls.confirm_console('Textures assign', False, False)
        # cls.log("Re-assign Textures.... ")

    @classmethod
    def triangulate(cls, selected):
        triangulate_nodes = []
        mesh_list = cmds.listRelatives(selected, typ='mesh', f=1)
        if not mesh_list:
            mesh_list = cmds.ls(l=1, type="mesh", fl=1)

        if mesh_list:
            for i in mesh_list:
                node = cmds.polyTriangulate(i, ch=1)[0]
                triangulate_nodes.append(node)
            cmds.select(d=1)
        # cls.confirm_console('Meshes triangulate', False, False)
        return triangulate_nodes

    @classmethod
    def visible_list(cls, export_objects):
        visible_nodes = []
        if export_objects:
            for node in export_objects:
                if not cmds.getAttr(node + '.visibility'):
                    visible_nodes.append(node)
                    cmds.setAttr(node + '.visibility', True)
        return visible_nodes

    @classmethod
    def get_material(cls, export_objects):
        shape_selection = cmds.filterExpand(export_objects, sm=12, fp=True)
        engine = cmds.listConnections(shape_selection, type='shadingEngine')
        materials = cmds.ls(cmds.listConnections(engine), materials=True)
        return materials

    @classmethod
    def check_n_material(cls, export_objects):
        materials = cls.get_material(export_objects)
        print('MATERIALS', materials)
        for mat in materials:
            if re.findall('^n_\w', mat):
                return True

        return False

    @classmethod
    def browser_path(cls):
        export_path = None
        try:
            export_path = cmds.fileDialog2(fm=3, dialogStyle=1)[0]
        except ValueError:
            pass

        return export_path

    @classmethod
    def create_icon(cls, w, h):
        pixmap = QPixmap(QSize(w, h))
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        # draw icon
        polygon = QPolygon()
        pen = QPen(Qt.white, 2, Qt.SolidLine)
        painter.drawLines(0, 10)
        painter.end()
        return QIcon(pixmap)

    @classmethod
    def confirm_console(cls, msg, error, warning):
        main_window = QCoreApplication.instance()
        widgets = main_window.allWidgets()
        for widget in widgets:
            if str(widget.objectName()) == 'DockConsoleObjects':
                widget.raise_()
                widget.set_text_line(msg, error, warning)
                return

    @staticmethod
    def console_log(text, error, warning):
        widget = Utils.dock_console_widget()
        widget.raise_()
        widget.set_text_line(text, error, warning)

    @staticmethod
    def dock_console_widget():
        main_window = QCoreApplication.instance()
        widgets = main_window.allWidgets()
        for widget in widgets:
            if str(widget.objectName()) == 'DockConsoleObjects':
                return widget
