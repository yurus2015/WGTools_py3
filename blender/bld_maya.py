bl_info = {
    "name": "Maya Bridge",
    "author": "Yu Rus",
    "version": (0, 4),
    "blender": (2, 80, 0),
    "category": "Blender<->Maya",
}

import bpy
import tempfile
import os

# store keymaps here to access after registration
addon_keymaps = []


def fbx_export_all_selection(copy=None):
    selected = bpy.context.selected_objects
    count = len(selected)
    if count > 0:
        file = tempfile.gettempdir() + os.sep + "export.fbx"
        if copy:
            file = tempfile.gettempdir() + os.sep + "copy.fbx"
        bpy.ops.export_scene.fbx(filepath=file, use_selection=True)
        print('Info:  Copied ' + str(count) + ' selected object(s)\n', file)


def fbx_import():
    file = tempfile.gettempdir() + os.sep + "import.fbx"
    bpy.ops.import_scene.fbx(filepath=file)


class ConnectToMaya(bpy.types.Operator):
    """Connect"""
    bl_label = "Connect To Maya"
    bl_idname = "wm.maya_connect"

    def execute(self, context):
        print('Connect!')

        return {'FINISHED'}


class ExportAllToMaya(bpy.types.Operator):
    """Export all"""
    bl_label = "Export All"
    bl_idname = "wm.export_all"

    def execute(self, context):
        print('Export All!')

        return {'FINISHED'}


class ExportSelectionToMaya(bpy.types.Operator):
    """Export selection"""
    bl_label = "Export Selection"
    bl_idname = "wm.export_selected"

    def execute(self, context):
        print('Export Selected!')


        return {'FINISHED'}


class CopyToBuffer(bpy.types.Operator):
    """Copy"""
    bl_label = "Copy To Buffer"
    bl_idname = "wm.copy_buffer"

    def execute(self, context):
        print('Copied!')
        fbx_export_all_selection()
        return {'FINISHED'}


class PasteFromBuffer(bpy.types.Operator):
    """Paste"""
    bl_label = "Paste From Buffer"
    bl_idname = "wm.paste_buffer"

    def execute(self, context):
        print('Pasted!')
        fbx_import()
        return {'FINISHED'}


class MayaPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Maya Panel"
    bl_idname = "maya_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender<->Maya"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.operator("wm.maya_connect")

        row = layout.row()
        row.operator("wm.export_all")

        row = layout.row()
        row.operator("wm.export_selected")

        row = layout.row()
        row.operator("wm.copy_buffer")

        row = layout.row()
        row.operator("wm.paste_buffer")


def register():
    bpy.utils.register_class(MayaPanel)
    bpy.utils.register_class(ConnectToMaya)
    bpy.utils.register_class(ExportAllToMaya)
    bpy.utils.register_class(ExportSelectionToMaya)
    bpy.utils.register_class(CopyToBuffer)
    bpy.utils.register_class(PasteFromBuffer)

    # handle the keymap
    wm = bpy.context.window_manager
    # Note that in background mode (no GUI available), keyconfigs are not available either,
    # so we have to check this to avoid nasty errors in background case.
    kc = wm.keyconfigs.addon
    if kc:
        km_copy = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
        kmi_copy = km_copy.keymap_items.new(CopyToBuffer.bl_idname, 'C', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km_copy, kmi_copy))

        km_paste = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
        kmi_paste = km_paste.keymap_items.new(PasteFromBuffer.bl_idname, 'V', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km_paste, kmi_paste))


def unregister():
    # Note: when unregistering, it's usually good practice to do it in reverse order you registered.
    # Can avoid strange issues like keymap still referring to operators already unregistered...
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(MayaPanel)
    bpy.utils.unregister_class(ConnectToMaya)
    bpy.utils.unregister_class(ExportAllToMaya)
    bpy.utils.unregister_class(ExportSelectionToMaya)
    bpy.utils.unregister_class(CopyToBuffer)
    bpy.utils.unregister_class(PasteFromBuffer)


if __name__ == "__main__":
    register()
