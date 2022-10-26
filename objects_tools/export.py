import importlib
import objects_tools.utils as utl
importlib.reload(utl)
from objects_tools.utils import *
import objects_tools.ui.gui as gui
importlib.reload(gui)

ARGUMENTS = 'noPrompt=1;bumpMapped=1;keep_material=1;copyExternalTextures=1;copyTexturesTo'
EXPORT_MODE = 'exportMode=2;'
VISUAL_SETTINGS = 'exportMode=static_with_nodes', 'keepMaterials', 'fixNodeTreeLOD'
# CONSOLE = None


def main(export_path=None):

    exporter = ObjectsExporter(export_path)
    exporter.run_export()


class ObjectsExporter:
    def __init__(self, export_path=None):
        self.export_path = export_path

    def export_command(self, export_objects, export_mode, arguments, path, name):
        path_export = posixpath.join(path, name)
        # command = 'file -op "'+ exportmode + arguments +'"  -typ "BigWorldAsset" -pr -es "' + path +'";'
        arguments = export_mode + arguments
        region = Utils.region()
        extension = ['visual', 'primitives', 'model']

        def export_selection():
            cmds.delete(export_objects, ch=1)
            tri_nodes = Utils.triangulate(export_objects)
            Utils.visible_list(export_objects)
            cmds.select(export_objects)
            cmds.file(path_export, force=False, type="BigWorldAsset", pr=True, es=True, options=str(arguments))
            cmds.delete(tri_nodes)

        if region:
            temp_dir = posixpath.join(path, 'tmp')
            Utils.create_folder(temp_dir)
            Utils.copy_file_to(path, temp_dir, region)
            export_selection()

            # rename region to region
            for ext in extension:
                Utils.rename_file(path, name, region, ext)

            # copy original from tmp
            Utils.copy_file_to(temp_dir, path, region)

            # delete tmp dir
            Utils.delete_folder(temp_dir)

        else:
            export_selection()

    def filter_output(self):
        output = self.gather_data_export()
        output = list(set(output))
        output.sort(key=lambda x: str(x.split("|")[1]))
        output_filtered = []
        for i in output:
            pattern = i.split("|")[1]
            temp = list(filter(lambda x: pattern in x, output))
            temp.sort(key=lambda x: str(x.split("|")[-1]))
            if temp not in output_filtered:
                output_filtered.append(temp)

        return output_filtered

    def gather_data_export(self):
        selection = cmds.ls(sl=True, l=True)
        output = []
        self.hp_selected = Utils.hp_world_selected()

        if selection:
            selection = Utils.remove_list(selection, self.hp_selected)

        if selection:
            for i in selection:
                object_type = Utils.object_type(i)

                if object_type == 'mesh':
                    export_lod = Utils.obj_parent(i)
                    if export_lod:
                        output.extend(export_lod)

                elif object_type == 'lod':
                    output.append(i)

                elif object_type == 'object':
                    export_lod = Utils.lods_in_obj(i)
                    output.extend(export_lod)

        else:
            output = Utils.lods_in_scene()

        return output

    def hierachy_names(self, lod):
        """
        user = 'username'
        host = 'host'
        '%s@%s' % (user, host)
        """
        names = lod.split('|')
        lod_null = '%s|%s|lod0' % (names[0], names[1])
        object_current = '%s|%s' % (names[0], names[1])

        return names[1], lod_null, object_current, names[2]

    def run_export(self):

        """Start console log"""
        console = Utils.dock_console_widget()
        console.clear_console()
        console.raise_()
        console.set_text_line('Start Export!\n')

        # check correct path
        if not utl.Utils.path_exists(self.export_path):
            console.set_text_line('Current path not exists!', True, False)
            console.set_text_line('<-Set export path!', True, False)
            return

        if not self.export_path.count('content'):
            console.set_text_line('Export to user directory', False, True)

        # gather data for export
        data_to_export = self.filter_output()
        if not data_to_export:
            console.set_text_line('Nothing to export ', True, False)
            return

        # prepare maya scene
        Utils.load_visual_plugin()
        Utils.bsp_layer_visible()
        scene_textures = Utils.clear_textures()

        # store selected for return after export
        selected = cmds.ls(sl=True, l=True)

        hp_world = Utils.hp_world()
        for model in data_to_export:
            export_hp = False
            export_mode = EXPORT_MODE

            for lod in model:
                meshes = Utils.mesh_in_lod(lod)
                name, lod0, object_name, export_name = self.hierachy_names(lod)
                # if _merged in file`s name
                typ, name = Utils.merged_split(name)
                export_objects = Utils.hp_group(lod0)
                hp_object = Utils.hp_group(object_name)
                export_objects.extend(hp_object)

                bsp = Utils.bsp_in_scene(lod)
                if not bsp:
                    bsp = Utils.bsp_in_scene(lod0)

                if not export_objects:
                    export_objects.extend(self.hp_selected)
                    if not export_objects:
                        export_objects.extend(hp_world)

                def general_commands():
                    export_objects.extend(bsp)
                    export_objects.extend(meshes)

                    # create export tree folders for export:
                    dir_path = Utils.create_export_dir(typ, export_name, self.export_path)
                    if not dir_path:
                        return False
                    self.export_command(export_objects, export_mode, ARGUMENTS, dir_path, name)

                # check destructible material. If it isn't - don't need warning hp message
                check_n_materials = Utils.check_n_material(meshes)
                if not check_n_materials:
                    export_hp = True

                if export_objects or export_hp:
                    general_commands()

                elif not export_objects and export_hp is False:
                    result = cmds.confirmDialog(title='Warning: Not HP!', button=['Continue Export', 'Cancel'],
                                                message='Press "Continue Export" for export without HP OR press '
                                                        '"Cancel" for select HP', defaultButton='Continue Export',
                                                cancelButton='Cancel', dismissString='Cancel')

                    if result == 'Continue Export':
                        export_hp = True
                        export_mode = 'exportMode=1;'

                        general_commands()
                    else:
                        return False

                console.set_text_line(lod + ' exported')

        # return to original state
        Utils.reassign_textures(scene_textures)

        # deselect current selection and restore selection before export
        cmds.select(d=1)
        if selected:
            cmds.select(selected)

        console.set_text_line('\nExport completed!')
