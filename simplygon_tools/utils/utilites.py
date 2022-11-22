import maya.cmds as cmds
import re
import os
import shutil
import traceback
import simplygon_tools.utils.fbx as fbx
from simplygon_tools.utils.constants import *


class Settings():
    auto_polycount = ('-', '-', '-', '-')
    manual_polycount = ('-', '-', '-', '-')

    lod1_count = 18000.0
    lod2_count = 10000.0
    lod3_count = 5000.0
    lod1_style_count = 22000.0

    lods_calculate = ['No tracks', 'No tracks', 'No tracks', 'No tracks']
    lods_manual = ['Enter value', 'Enter value', 'Enter value']


# function
def remove_list(from_list, this_list):
    result_list = [n for n in from_list if n not in this_list]
    result_list = list(result_list)
    return result_list


def remove_duplicate_list(current_list):
    result_list = list(set(current_list))
    return result_list


def confirm_dialog(text, do):
    result = cmds.confirmDialog(title='Tanks Simplygon',
                                message=text,
                                button=['   OK   ', 'Cancel'],
                                defaultButton='   OK   ',
                                cancelButton='Cancel',
                                dismissString='Cancel')
    if do == 'err':
        raise ValueError()
        return
    if result == '   OK   ':
        return True


def in_viewport_massage(message):
    cmds.inViewMessage(amg='In-view message <hl>' + message + '</hl>.', pos='botCenter', fade=True)


def load_plugin(plugin):
    loaded = cmds.pluginInfo('plugin', q=True, loaded=True)
    registered = cmds.pluginInfo(plugin, q=True, registered=True)

    if not registered or not loaded:
        cmds.loadPlugin(plugin)


# files
def exists_folder(path):
    return os.path.isdir(path)


def exists_file(file):
    return os.path.isfile(file)


def generate_lod_path(OUTPUT_FILES):
    result_path = None
    for it in os.scandir(OUTPUT_FILES):
        print('CHECK PATH', it.path)
        if it.is_dir() and it.name == 'export':
            print(it.path)
            result_path = it.path
            break

        generate_lod_path(it)
        print('WTF', result_path)

    return result_path


def generate_lod_fbx_path(path):
    for it in os.scandir(path):
        if it.is_file():
            print(it.name, it.path)
            return it.path


def clear_folder(path):
    if not os.path.isdir(path):
        return
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# scene validate
def maya_file_short_name():
    name = cmds.file(q=True, sn=1, shn=1)
    return name


def is_style():
    pattern_style = re.compile('_\dDst')
    file_name = maya_file_short_name()
    if pattern_style.findall(file_name):
        return True
    else:
        return False


def is_empty_scene():
    if cmds.ls(type='mesh'):
        return True
    else:
        return False


def is_tank_scene():
    if cmds.ls('hull*') and cmds.ls('turret*'):
        return True
    else:
        return False


# scene modification
def unlock_normals(meshes):
    pass


def restore_normals(meshes):
    cmds.select(meshes)
    objects = cmds.filterExpand(sm=12)
    if objects:
        cmds.delete(objects, ch=1)
        cmds.selectUVBorderEdge(he=1)  # techart plugin command
        cmds.select(objects)


def clear_textures():
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
    return node_material_struct


def reassign_textures(node_material=None):
    if not node_material:
        return
    for i in node_material:
        cmds.connectAttr(node_material[i], i)


def create_hierarchy():
    selection = cmds.ls(sl=True)
    lods = cmds.ls('|lod*', tr=1, l=1)
    predefine_lods = ('|lod0')
    remain_lod = remove_list(lods, predefine_lods)
    if remain_lod:
        result = confirm_dialog('Lods 1-4 exists. Delete them?', 'make')
        if result:
            cmds.delete(remain_lod)
            create_lods_group()
    else:
        create_lods_group()

    if selection:
        cmds.select(selection)


def create_lods_group():
    lods = ('lod1', 'lod2', 'lod3')
    tracks = cmds.ls('lod0|chassis*|track*', tr=1, l=1)
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
        confirm_dialog('Tracks in lod0 don`t exist', 'err')


def tracks_lod():
    lods = cmds.ls('|lod0', '|lod1', '|lod2', '|lod3', tr=1)
    lod_tracks = [[]] * len(lods)
    for i in range(len(lods)):
        children = cmds.listRelatives(lods[i], ad=1, typ='transform', f=1)
        tracks = []
        for c in children:
            if 'track_' in c:
                tracks.append(c)
        lod_tracks[i] = tracks
    lods_track_count = []
    for lod in lod_tracks:
        shapes = cmds.filterExpand(lod, sm=12, fp=1)
        polycount = cmds.polyEvaluate(shapes, t=1)
        lods_track_count.append(polycount)

    print('tracks', lod_tracks)
    print('polycount', lods_track_count)
    return lods_track_count


def validate_value(settings):
    try:
        m1 = int(settings[0])
        m2 = int(settings[1])
        m3 = int(settings[2])
        print([m1, m2, m3])
        return [m1, m2, m3]
    except ValueError:
        confirm_dialog('Not valid value in fields', 'err')


def type_exported(exported):  # type could be: mesh, group, or list(tuple)
    if isinstance(exported, (list, tuple)):
        return 'list'
    if cmds.listRelatives(exported, c=1, f=1, type="transform"):
        return 'group'
    if cmds.listRelatives(exported, c=1, f=1, type="mesh"):
        return 'mesh'


def coefficient_by_type(exported):
    if type_exported(exported) == 'list':
        exported = exported[0]
    print('L', exported)
    if 'gun' in exported or 'chassis' in exported:
        return 0.40
    if 'hull' in exported or 'turret' in exported:
        return 0.30


def lods_coefficient(type_reduce=None):
    if type_reduce:
        # check is int value
        lod_counts = validate_value(Settings.lods_manual)
        print('TYPE_MANUAL', lod_counts)
    else:
        lod_counts = validate_value(Settings.lods_calculate[1:])
        print('TYPE_AUTO', lod_counts)

    # calculate plycount for lods
    lods_coefficients = calculate_polycount()
    print('LODS/COEFF\n', lods_coefficients)

    lod_counts = list(map(str, lod_counts))
    return lods_coefficients


def calculate_polycount(*args):
    if not is_empty_scene() or not is_tank_scene():
        return

    print('Calculate', Settings.auto_polycount)
    count1 = Settings.lod1_count
    count2 = Settings.lod2_count
    count3 = Settings.lod3_count
    if is_style():
        count1 = Settings.lod1_style_count
    print('args ', args)
    if args:  # for manual
        count1 = args[0]
        count2 = args[1]
        count3 = args[2]

    def lod0_max_polycount():
        hull_turret = []
        gun_chassis = []
        turrets = []
        guns = []
        lod0 = cmds.ls('|lod0', tr=1)

        children = cmds.listRelatives(lod0[0], c=1, typ='transform', f=1)
        grand_children = cmds.listRelatives(lod0[0], ad=1, typ='mesh', f=1)
        grand_children = cmds.listRelatives(grand_children, p=1, typ='transform', f=1)

        children = cmds.listRelatives(lod0[0], c=1, typ='transform', f=1)
        grand_children = cmds.listRelatives(lod0[0], ad=1, typ='mesh', f=1)
        grand_children = cmds.listRelatives(grand_children, p=1, typ='transform', f=1)
        for child in children:
            if 'hull_' in child:
                hull_turret.append(child)
            if 'turret_' in child:
                mesh = cmds.filterExpand(child, sm=12)
                count = cmds.polyEvaluate(mesh, t=1)
                turrets.append([child, count])
            if 'gun_' in child:
                count = cmds.polyEvaluate(child, t=1)
                guns.append([child, count])

        for child in grand_children:
            if 'chassis' in child and 'track_' not in child:
                gun_chassis.append(child)

        if guns:
            guns = sorted(guns, key=lambda guns: guns[1])
            gun_chassis.append(guns[-1][0])

        if turrets:
            turrets = sorted(turrets, key=lambda turrets: turrets[1])
            hull_turret.append(turrets[-1][0])

        hull_turret = cmds.filterExpand(hull_turret, sm=12, fp=1)
        hull_turret_cnt = cmds.polyEvaluate(hull_turret, t=1)
        gun_chassis = cmds.filterExpand(gun_chassis, sm=12, fp=1)
        gun_chassis_cnt = cmds.polyEvaluate(gun_chassis, t=1)

        return hull_turret_cnt, gun_chassis_cnt

    tracks_lods_polycount = tracks_lod()
    hull_turret_polycount, gun_chassis_polycount = lod0_max_polycount()

    coef1 = 1.0
    coef2 = 1.0
    coef3 = 1.0

    if tracks_lods_polycount[0]:
        tracks_polycount = tracks_lods_polycount[0]
    else:
        tracks_polycount = 0
    lod0_auto_count = hull_turret_polycount + gun_chassis_polycount + tracks_polycount

    base_polycount = 0.3 * hull_turret_polycount + 0.4 * gun_chassis_polycount
    lod1_without_tracks = base_polycount * coef1

    # todo refactor/optimize
    try:
        cfc1 = (count1 - tracks_lods_polycount[1]) / base_polycount
        if args:
            coef1 = cfc1
        elif cfc1 < 1.0:
            coef1 = cfc1
        lod1_auto_count = int(base_polycount * coef1 + tracks_lods_polycount[1])
        lod1_without_tracks = base_polycount * coef1

    except Exception:
        if tracks_lods_polycount[0]:
            lod1_auto_count = 'No tracks'
        else:
            cfc1 = count1 / base_polycount
            if args:
                coef1 = cfc1
            elif cfc1 < 1.0:
                coef1 = cfc1
            lod1_auto_count = int(base_polycount * coef1)
        traceback.print_exc()

    try:
        cfc2 = (count2 - tracks_lods_polycount[2]) / (0.5 * lod1_without_tracks)
        if args:
            coef2 = cfc2
        elif cfc2 < 1.0:
            coef2 = cfc2

        lod2_auto_count = int(0.5 * lod1_without_tracks * coef2 + tracks_lods_polycount[2])
        lod2_without_tracks = lod2_auto_count - tracks_lods_polycount[2]

    except Exception:
        if tracks_lods_polycount[0]:
            lod2_auto_count = 'No tracks'
        else:
            cfc2 = count2 / (0.5 * lod1_auto_count)
            if args:
                coef2 = cfc2
            elif cfc2 < 1.0:
                coef2 = cfc2
            lod2_auto_count = int(0.5 * lod1_auto_count * coef2)
        traceback.print_exc()

    try:
        cfc3 = (count3 - tracks_lods_polycount[3]) / (0.5 * lod2_without_tracks)
        if args:
            coef3 = cfc3
        elif cfc3 < 1.0:
            coef3 = cfc3

        lod3_auto_count = int(0.5 * lod2_without_tracks * coef3 + tracks_lods_polycount[3])
        lod3_without_tracks = lod3_auto_count - tracks_lods_polycount[3]

    except Exception:
        if tracks_lods_polycount[0]:
            lod3_auto_count = 'No tracks'
        else:
            cfc3 = count3 / (0.5 * lod2_auto_count)
            if args:
                coef3 = cfc3
            elif cfc3 < 1.0:
                coef3 = cfc3
            lod3_auto_count = int(0.5 * lod2_auto_count * coef3)
        traceback.print_exc()

    print('Final Count', lod0_auto_count, lod1_auto_count, lod2_auto_count, lod3_auto_count, coef1, 0.5 * coef2,
          0.5 * coef3)
    # lod0_auto_count = int(lod0_auto_count)
    # lod1_auto_count = int(lod1_auto_count)
    # lod2_auto_count = int(lod2_auto_count)
    # lod3_auto_count = int(lod3_auto_count)
    Settings.lods_calculate = [lod0_auto_count, lod1_auto_count, lod2_auto_count, lod3_auto_count]
    return lod0_auto_count, lod1_auto_count, lod2_auto_count, lod3_auto_count, coef1, 0.5 * coef2, 0.5 * coef3


def export_data(selection):  # prepare data in legacy script
    simplygon_data = []
    chassis_l = []
    chassis_r = []

    # if 'lod0' selection
    if selection and len(selection) == 1:
        if re.match('.lod0$', selection[0]):
            selection = cmds.listRelatives("|lod0", c=1, type="transform", f=1)

    # nothing selected
    if not selection:
        # get relatives children
        selection = cmds.listRelatives("|lod0", c=1, type="transform", f=1)

    for i in selection:
        if cmds.listRelatives(i, c=1, type="transform"):
            if 'chassis' in i:
                chassis_parts = cmds.listRelatives(i, c=1, type="transform", f=1)
                for j in chassis_parts:
                    if '_L' in j:
                        chassis_l.append(j)
                    if '_R' in j:
                        chassis_r.append(j)
                if chassis_l:
                    simplygon_data.append(chassis_l)
                if chassis_r:
                    simplygon_data.append(chassis_r)
            else:
                simplygon_data.append(i)  # i don't now
        else:
            simplygon_data.append(i)

    return simplygon_data
