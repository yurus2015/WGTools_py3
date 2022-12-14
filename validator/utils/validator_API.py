# ------------------------------------------------------------------------------------
#
#	This is set of useful functions. Each one provides information
#	required for almost every script and validator as well. To use it
#   you only need refer to this file. Each function return information
#   given in function name.
#
#	-------------------------------------------------------------------
#	All code below given only for informational purposes.
#	Do not make any changes, it may cause issues.
#   For more information contact with me v_chebonenko@wargaming.net
#	-------------------------------------------------------------------
#
# ------------------------------------------------------------------------------------
#                               REFERENCE
#
#    help_directory
#    root_directory
#    vl_tanksValidNames
#    vl_tankGroupsValidNames()
#    vl_tanksMatValidNames
#    vl_tanksTxtValidNames(Tankname)
#    vl_tanksHPValidNames()
#    vl_tanksLayersValidNames()
#    vl_objectsValidNames()
#    vl_objectsMatValidNames()
#    listAllMat()
#    vl_listAllTransforms()
#    vl_listAllGroups()
#    vl_listHPModules()
#    vl_listLodsGroups()
#    vl_findTracksInLods()
#    vl_objMeshData()
#    vl_objMaterialsData()
#    vl_lambert1Info()
#

import maya.cmds as cmds
import re
import traceback
import operator
import maya.OpenMaya as om
import os
import json


def help_directory():
    return os.path.dirname(os.path.dirname(__file__)) + "/ui/help/"


def root_directory():
    return os.path.dirname(__file__)


def API_aboutInfo():
    print(" validator_API; ver 2.0; 29.08.2014 ")


def vl_original_tank_name():
    name = cmds.file(q=True, sn=True, shn=True)
    short_name = os.path.splitext(name)[0]

    if 'crash' in short_name:
        short_name = short_name.split('_crash')[0]

    return short_name


def vl_tanksValidNames():
    listMeshSearchNames = []
    # ------------------------------ tanks HD ---------------------------------#

    hull_ = re.compile('^hull');
    listMeshSearchNames.append(hull_)
    hull_havok = re.compile('^hull_havok\Z');
    listMeshSearchNames.append(hull_havok)
    hull_inside = re.compile('^hull_inside\Z');
    listMeshSearchNames.append(hull_inside)

    turret = re.compile('^turret\Z');
    listMeshSearchNames.append(turret)
    turret_havok = re.compile('^turret_havok\Z');
    listMeshSearchNames.append(turret_havok)

    chassis_L_ = re.compile('^chassis_L\Z');
    listMeshSearchNames.append(chassis_L_)
    chassis_R_ = re.compile('^chassis_R\Z');
    listMeshSearchNames.append(chassis_R_)

    wd_L = re.compile('^wd_L\d\d\Z');
    listMeshSearchNames.append(wd_L)
    w_L = re.compile('^w_L\d\d\Z');
    listMeshSearchNames.append(w_L)
    wd_R = re.compile('^wd_R\d\d\Z');
    listMeshSearchNames.append(wd_R)
    w_R = re.compile('^w_R\d\d\Z');
    listMeshSearchNames.append(w_R)

    track_L = re.compile('^track_L\Z');
    listMeshSearchNames.append(track_L)
    track_R = re.compile('^track_R\Z');
    listMeshSearchNames.append(track_R)

    gun = re.compile('^gun_\d\d\Z');
    listMeshSearchNames.append(gun)
    gun = re.compile('^gun_\d\d_bsp\Z');
    listMeshSearchNames.append(gun)

    return listMeshSearchNames


def vl_tanksValidNames_techArt():
    listMeshSearchNames = []
    # ------------------------------ tanks HD ---------------------------------#

    hull_ = re.compile('^hull\Z');
    listMeshSearchNames.append(hull_)
    hull_havok = re.compile('^hull_havok\Z');
    listMeshSearchNames.append(hull_havok)
    hull_inside = re.compile('^hull_inside\Z');
    listMeshSearchNames.append(hull_inside)

    turret = re.compile('^turret\Z');
    listMeshSearchNames.append(turret)
    turret_havok = re.compile('^turret_havok\Z');
    listMeshSearchNames.append(turret_havok)

    chassis_L_ = re.compile('^chassis_L\Z');
    listMeshSearchNames.append(chassis_L_)
    chassis_R_ = re.compile('^chassis_R\Z');
    listMeshSearchNames.append(chassis_R_)

    wd_L = re.compile('^wd_L\d\d\Z');
    listMeshSearchNames.append(wd_L)
    w_L = re.compile('^w_L\d\d\Z');
    listMeshSearchNames.append(w_L)
    wd_R = re.compile('^wd_R\d\d\Z');
    listMeshSearchNames.append(wd_R)
    w_R = re.compile('^w_R\d\d\Z');
    listMeshSearchNames.append(w_R)

    track_L = re.compile('^track_L\Z');
    listMeshSearchNames.append(track_L)
    track_R = re.compile('^track_R\Z');
    listMeshSearchNames.append(track_R)

    gun = re.compile('^gun_\d\d\Z');
    listMeshSearchNames.append(gun)
    gun = re.compile('^gun_\d\d_bsp\Z');
    listMeshSearchNames.append(gun)

    wd_Ldd = re.compile('^wd_L\Z');
    listMeshSearchNames.append(wd_Ldd)
    w_Ldd = re.compile('^w_L\Z');
    listMeshSearchNames.append(w_Ldd)
    wd_Rdd = re.compile('^wd_R\Z');
    listMeshSearchNames.append(wd_Rdd)
    w_Rdd = re.compile('^w_R\Z');
    listMeshSearchNames.append(w_Rdd)
    gundd = re.compile('^gun_\Z');
    listMeshSearchNames.append(gundd)
    gunbspdd = re.compile('^gun_bsp\Z');
    listMeshSearchNames.append(gunbspdd)

    return listMeshSearchNames


def vl_tankGroupsValidNames():
    listGroupSearchNames = []

    lod = re.compile('^[|]lod\d\Z');
    listGroupSearchNames.append(lod)
    hull = re.compile('[|]hull_\d\d\Z');
    listGroupSearchNames.append(hull)
    turret = re.compile('[|]turret_\d\d\Z');
    listGroupSearchNames.append(turret)
    chassis = re.compile('[|]chassis_\d\d\Z');
    listGroupSearchNames.append(chassis)
    R_loc = re.compile('^[|]R_loc\Z');
    listGroupSearchNames.append(R_loc)
    L_loc = re.compile('^[|]L_loc\Z');
    listGroupSearchNames.append(L_loc)

    return listGroupSearchNames


def vl_tankGroupsValidNames_techArt():
    listGroupSearchNames = []

    lod = re.compile('^[|]lod\d\Z');
    listGroupSearchNames.append(lod)
    hull = re.compile('[|]hull_\d\d\Z');
    listGroupSearchNames.append(hull)
    turret = re.compile('[|]turret_\d\d\Z');
    listGroupSearchNames.append(turret)
    chassis = re.compile('[|]chassis_\d\d\Z');
    listGroupSearchNames.append(chassis)
    R_loc = re.compile('^[|]R_loc\Z');
    listGroupSearchNames.append(R_loc)
    L_loc = re.compile('^[|]L_loc\Z');
    listGroupSearchNames.append(L_loc)

    loddd = re.compile('^[|]lod\Z');
    listGroupSearchNames.append(loddd)
    hulldd = re.compile('[|]hull\Z');
    listGroupSearchNames.append(hulldd)
    turretdd = re.compile('[|]turret\Z');
    listGroupSearchNames.append(turretdd)
    chassisdd = re.compile('[|]chassis\Z');
    listGroupSearchNames.append(chassisdd)
    R_locdd = re.compile('^[|]R_loc\Z');
    listGroupSearchNames.append(R_locdd)
    L_locdd = re.compile('^[|]L_loc\Z');
    listGroupSearchNames.append(L_locdd)

    return listGroupSearchNames


def vl_tanksMatValidNames():
    listSearchNames = []

    # NOTE: the first letter always is capitalized for all materials name
    lambert = re.compile('^lambert1');
    listSearchNames.append(lambert)
    pCloud = re.compile('^particleCloud1');
    listSearchNames.append(pCloud)

    # ------------------------------ Materials HD ---------------------------------#

    Tank_hull_ = re.compile('^tank_hull_\d\d\Z');
    listSearchNames.append(Tank_hull_)
    Tank_mat_inside = re.compile('^tank_mat_inside\Z');
    listSearchNames.append(Tank_mat_inside)
    Tank_guns = re.compile('^tank_guns\Z');
    listSearchNames.append(Tank_guns)
    Tank_turret_ = re.compile('^tank_turret_\d\d\Z');
    listSearchNames.append(Tank_turret_)
    Tank_chassis = re.compile('^tank_chassis_\d\d\Z');
    listSearchNames.append(Tank_chassis)
    Track_mat_L = re.compile('^track_mat_L\Z');
    listSearchNames.append(Track_mat_L)
    Track_mat_R = re.compile('^track_mat_R\Z');
    listSearchNames.append(Track_mat_R)

    Tank_proxy = re.compile('^tank_proxy\Z');
    listSearchNames.append(Tank_proxy)  # check for lod4
    # Track_mat_L = re.compile('track');         listSearchNames.append(Track_mat_L)
    # Track_mat_R = re.compile('track');         listSearchNames.append(Track_mat_R)
    return listSearchNames


def vl_tanksMatValidNames_techArt():
    listSearchNames = []

    # NOTE: the first letter always is capitalized for all materials name
    lambert = re.compile('^lambert1');
    listSearchNames.append(lambert)
    pCloud = re.compile('^particleCloud1');
    listSearchNames.append(pCloud)

    # ------------------------------ Materials HD ---------------------------------#

    Tank_hull_ = re.compile('^tank_hull_\d\d\Z');
    listSearchNames.append(Tank_hull_)
    Tank_mat_inside = re.compile('^tank_mat_inside\Z');
    listSearchNames.append(Tank_mat_inside)
    Tank_guns = re.compile('^tank_guns\Z');
    listSearchNames.append(Tank_guns)
    Tank_turret_ = re.compile('^tank_turret_\d\d\Z');
    listSearchNames.append(Tank_turret_)
    Tank_chassis = re.compile('^tank_chassis_\d\d\Z');
    listSearchNames.append(Tank_chassis)
    Track_mat_L = re.compile('^track_mat_L\Z');
    listSearchNames.append(Track_mat_L)
    Track_mat_R = re.compile('^track_mat_R\Z');
    listSearchNames.append(Track_mat_R)
    # Track_mat_L = re.compile('track');         listSearchNames.append(Track_mat_L)
    # Track_mat_R = re.compile('track');         listSearchNames.append(Track_mat_R)

    Tank_hull_dd = re.compile('^tank_hull\Z');
    listSearchNames.append(Tank_hull_dd)
    Tank_turret_dd = re.compile('^tank_turret\Z');
    listSearchNames.append(Tank_turret_dd)
    Tank_chassisdd = re.compile('^tank_chassis\Z');
    listSearchNames.append(Tank_chassisdd)

    Tank_proxy = re.compile('^tank_proxy\Z');
    listSearchNames.append(Tank_proxy)  # check for lod4

    return listSearchNames


def vl_tank_textures_names(tank_name):
    texture_names_list = []
    texture_type = ['AM', 'GM', 'MM', 'NM', 'AO', 'BM', 'ID', 'CM', 'PM', 'ANM', 'GMM']
    tank_digit_parts = ['hull', 'turret', 'chassis']
    tank_parts = ['guns', 'proxy']

    names = []
    for texture in texture_type:
        for part in tank_digit_parts:
            names.append('^' + tank_name + '_' + part + '_\d\d_' + texture + '\Z')
        for part in tank_parts:
            names.append('^' + tank_name + '_' + part + '_' + texture + '\Z')

    names.append('^' + tank_name + '_HangarShadowMap\Z')

    for x in names:
        texture_names_list.append(re.compile(x))

    return texture_names_list


def vl_tanksTxtValidNames(Tankname):  # for tga
    listSearchNames = []

    # ------------------------------ Textures old ---------------------------------#

    names = [ \
        "^" + Tankname + '_hull_\d\d_AM\Z', \
        "^" + Tankname + "_hull_\d\d_GM\Z", \
        "^" + Tankname + "_hull_\d\d_MM\Z", \
        "^" + Tankname + "_hull_\d\d_NM\Z", \
        "^" + Tankname + "_hull_\d\d_AO\Z", \
        "^" + Tankname + "_hull_\d\d_BM\Z", \
        "^" + Tankname + "_hull_\d\d_ID\Z", \
        "^" + Tankname + "_hull_\d\d_ANM\Z", \
        "^" + Tankname + "_hull_\d\d_GMM\Z", \
        "^" + Tankname + "_hull_\d\d_crash_AM\Z", \
        "^" + Tankname + "_hull_\d\d_crash_AO\Z", \
        "^" + Tankname + "_hull_\d\d_crash_ANM\Z", \
        "^" + Tankname + "_hull_\d\d_crash_GMM\Z", \
 \
        "^" + Tankname + "_turret_\d\d_AM\Z", \
        "^" + Tankname + "_turret_\d\d_GM\Z", \
        "^" + Tankname + "_turret_\d\d_MM\Z", \
        "^" + Tankname + "_turret_\d\d_NM\Z", \
        "^" + Tankname + "_turret_\d\d_AO\Z", \
        "^" + Tankname + "_turret_\d\d_BM\Z", \
        "^" + Tankname + "_turret_\d\d_ID\Z", \
        "^" + Tankname + "_turret_\d\d_ANM\Z", \
        "^" + Tankname + "_turret_\d\d_GMM\Z", \
        "^" + Tankname + "_turret_\d\d_crash_AM\Z", \
        "^" + Tankname + "_turret_\d\d_crash_AO\Z", \
        "^" + Tankname + "_turret_\d\d_crash_ANM\Z", \
        "^" + Tankname + "_turret_\d\d_crash_GNM\Z", \
 \
        "^" + Tankname + "_guns_AM\Z", \
        "^" + Tankname + "_guns_GM\Z", \
        "^" + Tankname + "_guns_MM\Z", \
        "^" + Tankname + "_guns_NM\Z", \
        "^" + Tankname + "_guns_AO\Z", \
        "^" + Tankname + "_guns_BM\Z", \
        "^" + Tankname + "_guns_ID\Z", \
        "^" + Tankname + "_guns_ANM\Z", \
        "^" + Tankname + "_guns_GMM\Z", \
        "^" + Tankname + "_guns_crash_AM\Z", \
        "^" + Tankname + "_guns_crash_AO\Z", \
        "^" + Tankname + "_guns_crash_ANM\Z", \
        "^" + Tankname + "_guns_crash_GMM\Z", \
 \
        "^" + Tankname + "_gun_\d\d_AM\Z", \
        "^" + Tankname + "_gun_\d\d_GM\Z", \
        "^" + Tankname + "_gun_\d\d_MM\Z", \
        "^" + Tankname + "_gun_\d\d_NM\Z", \
        "^" + Tankname + "_gun_\d\d_AO\Z", \
        "^" + Tankname + "_gun_\d\d_BM\Z", \
        "^" + Tankname + "_gun_\d\d_ID\Z", \
        "^" + Tankname + "_gun_\d\d_ANM\Z", \
        "^" + Tankname + "_gun_\d\d_GMM\Z", \
        "^" + Tankname + "_gun_\d\d_crash_AM\Z", \
        "^" + Tankname + "_gun_\d\d_crash_AO\Z", \
        "^" + Tankname + "_gun_\d\d_crash_ANM\Z", \
        "^" + Tankname + "_gun_\d\d_crash_GMM\Z", \
 \
        "^" + Tankname + "_chassis_\d\d_AM\Z", \
        "^" + Tankname + "_chassis_\d\d_GM\Z", \
        "^" + Tankname + "_chassis_\d\d_MM\Z", \
        "^" + Tankname + "_chassis_\d\d_NM\Z", \
        "^" + Tankname + "_chassis_\d\d_AO\Z", \
        "^" + Tankname + "_chassis_\d\d_BM\Z", \
        "^" + Tankname + "_chassis_\d\d_ID\Z", \
        "^" + Tankname + "_chassis_\d\d_ANM\Z", \
        "^" + Tankname + "_chassis_\d\d_GMM\Z", \
        "^" + Tankname + "_chassis_\d\d_crash_AM\Z", \
        "^" + Tankname + "_chassis_\d\d_crash_AO\Z", \
        "^" + Tankname + "_chassis_\d\d_crash_ANM\Z", \
        "^" + Tankname + "_chassis_\d\d_crash_GMM\Z", \
 \
        "track", \
        "Track", \
        "^" + Tankname + "_track_L_\d\d_AM\Z", \
        "^" + Tankname + "_track_L_\d\d_GM\Z", \
        "^" + Tankname + "_track_L_\d\d_MM\Z", \
        "^" + Tankname + "_track_L_\d\d_NM\Z", \
        "^" + Tankname + "_track_L_\d\d_AO\Z", \
        "^" + Tankname + "_track_L_\d\d_ANM\Z", \
        "^" + Tankname + "_track_L_\d\d_GMM\Z", \
        "^" + Tankname + "_track_L_\d\d_crash_AM\Z", \
        "^" + Tankname + "_track_L_\d\d_crash_AO\Z", \
        "^" + Tankname + "_track_L_\d\d_crash_ANM\Z", \
        "^" + Tankname + "_track_L_\d\d_crash_GMM\Z", \
 \
        "^" + Tankname + "_track_R_\d\d_AM\Z", \
        "^" + Tankname + "_track_R_\d\d_GM\Z", \
        "^" + Tankname + "_track_R_\d\d_MM\Z", \
        "^" + Tankname + "_track_R_\d\d_NM\Z", \
        "^" + Tankname + "_track_R_\d\d_AO\Z", \
        "^" + Tankname + "_track_R_\d\d_ANM\Z", \
        "^" + Tankname + "_track_R_\d\d_GMM\Z", \
        "^" + Tankname + "_track_R_\d\d_crash_AM\Z", \
        "^" + Tankname + "_track_R_\d\d_crash_AO\Z", \
        "^" + Tankname + "_track_R_\d\d_crash_ANM\Z", \
        "^" + Tankname + "_track_R_\d\d_crash_GMM\Z", \
 \
        # "^" + Tankname + "_track_L_\d\d_AM\Z",\
        # "^" + Tankname + "_track_L_\d\d_GM\Z",\
        # "^" + Tankname + "_track_L_\d\d_MM\Z",\
        # "^" + Tankname + "_track_L_\d\d_NM\Z",\
        # "^" + Tankname + "_track_L_\d\d_AO\Z",\
        # "^" + Tankname + "_track_L_\d\d_ANM\Z",\
        # "^" + Tankname + "_track_L_\d\d_GMM\Z",\
        # "^" + Tankname + "_track_L_\d\d_crash_AM\Z",\
        # "^" + Tankname + "_track_L_\d\d_crash_AO\Z",\
        # "^" + Tankname + "_track_L_\d\d_crash_ANM\Z",\
        # "^" + Tankname + "_track_L_\d\d_crash_GMM\Z",\

        # "^" + Tankname + "_track_R_\d\d_AM\Z",\
        # "^" + Tankname + "_track_R_\d\d_GM\Z",\
        # "^" + Tankname + "_track_R_\d\d_MM\Z",\
        # "^" + Tankname + "_track_R_\d\d_NM\Z",\
        # "^" + Tankname + "_track_R_\d\d_AO\Z",\
        # "^" + Tankname + "_track_R_\d\d_ANM\Z",\
        # "^" + Tankname + "_track_R_\d\d_GMM\Z",\
        # "^" + Tankname + "_track_R_\d\d_crash_AM\Z",\
        # "^" + Tankname + "_track_R_\d\d_crash_AO\Z",\
        # "^" + Tankname + "_track_R_\d\d_crash_ANM\Z",\
        # "^" + Tankname + "_track_R_\d\d_crash_GMM\Z",\

        "^" + Tankname + "_hull_\d\d_CM\Z", \
        "^" + Tankname + "_turret_\d\d_CM\Z", \
        "^" + Tankname + "_guns_CM\Z", \
        "^" + Tankname + "_HangarShadowMap\Z", \
 \
        "^" + Tankname + "_proxy_AM", \
        "^" + Tankname + "_proxy_GM", \
        "^" + Tankname + "_proxy_MM", \
        "^" + Tankname + "_proxy_NM", \
        "^" + Tankname + "_proxy_CM", \
        "^" + Tankname + "_proxy_AO", \
        "^" + Tankname + "_proxy_BM", \
        "^" + Tankname + "_proxy_ID", \
        "^" + Tankname + "_proxy_ANM", \
        "^" + Tankname + "_proxy_GMM", \
 \
        # CRASH INSIDE
        #
        "^crash_inside_AM", \
        "^crash_inside_GMM", \
        "^crash_inside_NM", \
        "^crash_inside_AO", \
 \
        ]

    # Trackname+ "_track_AM",\
    # Trackname+ "_track_GM",\
    # Trackname+ "_track_MM",\
    # Trackname+ "_track_NM",\

    # Trackname+ "_segment_track_AM",\
    # Trackname+ "_segment_track_GM",\
    # Trackname+ "_segment_track_MM",\
    # Trackname+ "_segment_track_NM",\
    # Trackname+ "_segment_track_AO"

    for x in names:
        listSearchNames.append(re.compile(x))

    return listSearchNames


def vl_tanksHPValidNames():
    listMeshSearchNames = []

    # This is the list of all possible names for tank HP objects inside the scene

    HP_Track_LFront = re.compile('HP_Track_LFront\Z');
    listMeshSearchNames.append(HP_Track_LFront)
    HP_Track_LRear = re.compile('HP_Track_LRear\Z');
    listMeshSearchNames.append(HP_Track_LRear)
    HP_Track_RFront = re.compile('HP_Track_RFront\Z');
    listMeshSearchNames.append(HP_Track_RFront)
    HP_Track_RRear = re.compile('HP_Track_RRear\Z');
    listMeshSearchNames.append(HP_Track_RRear)
    HP_gui = re.compile('HP_gui\Z');
    listMeshSearchNames.append(HP_gui)
    HP_turretJoint = re.compile('HP_turretJoint\Z');
    listMeshSearchNames.append(HP_turretJoint)
    HP_Fire = re.compile('HP_Fire_\d');
    listMeshSearchNames.append(HP_Fire)
    HP_TrackUp_LFront = re.compile('HP_TrackUp_LFront\Z');
    listMeshSearchNames.append(HP_TrackUp_LFront)
    HP_TrackUp_LRear = re.compile('HP_TrackUp_LRear\Z');
    listMeshSearchNames.append(HP_TrackUp_LRear)
    HP_TrackUp_RFront = re.compile('HP_TrackUp_RFront\Z');
    listMeshSearchNames.append(HP_TrackUp_RFront)
    HP_TrackUp_RRear = re.compile('HP_TrackUp_RRear\Z');
    listMeshSearchNames.append(HP_TrackUp_RRear)
    HP_Track_Exhaus = re.compile('HP_Track_Exhaus_\d');
    listMeshSearchNames.append(HP_Track_Exhaus)
    HP_gunJoint = re.compile('HP_gunJoint_\d');
    listMeshSearchNames.append(HP_gunJoint)
    HP_gunFire = re.compile('HP_gunFire_\d');
    listMeshSearchNames.append(HP_gunFire)

    return listMeshSearchNames


def vl_tanksLayersValidNames():
    listMeshSearchNames = []

    # This is the list of all possible names for tank HP objects inside the scene

    defaultLayer = re.compile('^defaultLayer');
    listMeshSearchNames.append(defaultLayer)
    Hull = re.compile('^Hull_\d\d\Z');
    listMeshSearchNames.append(Hull)
    Turret = re.compile('^Turret_\d\d\Z');
    listMeshSearchNames.append(Turret)
    Gun = re.compile('^Gun_\d\d\Z');
    listMeshSearchNames.append(Gun)
    Chassis = re.compile('^Chassis_\d\d\Z');
    listMeshSearchNames.append(Chassis)

    return listMeshSearchNames


def vl_tanksLayersValidNames_techArt():
    listMeshSearchNames = []

    # This is the list of all possible names for tank HP objects inside the scene

    defaultLayer = re.compile('^defaultLayer');
    listMeshSearchNames.append(defaultLayer)
    Hull = re.compile('^Hull\Z');
    listMeshSearchNames.append(Hull)
    Turret = re.compile('^Turret\Z');
    listMeshSearchNames.append(Turret)
    Gun = re.compile('^Gun\Z');
    listMeshSearchNames.append(Gun)
    Chassis = re.compile('^Chassis\Z');
    listMeshSearchNames.append(Chassis)
    Hulldd = re.compile('^Hull_\d\d\Z');
    listMeshSearchNames.append(Hulldd)
    Turretdd = re.compile('^Turret_\d\d\Z');
    listMeshSearchNames.append(Turretdd)
    Gundd = re.compile('^Gun_\d\d\Z');
    listMeshSearchNames.append(Gundd)
    Chassisdd = re.compile('^Chassis_\d\d\Z');
    listMeshSearchNames.append(Chassisdd)

    return listMeshSearchNames


def vl_objectsValidNames():
    listMeshSearchNames = []

    d = re.compile('^d\d');
    listMeshSearchNames.append(d)

    n = re.compile('^n\d$');
    listMeshSearchNames.append(n)
    n = re.compile('^n\d_\d$');
    listMeshSearchNames.append(n)
    n = re.compile('^n\d_bsp$');
    listMeshSearchNames.append(n)
    n = re.compile('^n\d+_\d+_bsp$');
    listMeshSearchNames.append(n)

    s = re.compile('^s\d{1,2}$');
    listMeshSearchNames.append(s)
    s = re.compile('^s\d_bsp$');
    listMeshSearchNames.append(s)
    s = re.compile('^s\d+_\d+$');
    listMeshSearchNames.append(s)
    s = re.compile('^s\d+_\d+_bsp$');
    listMeshSearchNames.append(s)

    ramp = re.compile('^s_ramp\d$');
    listMeshSearchNames.append(ramp)
    ramp = re.compile('^s_ramp\d_bsp$');
    listMeshSearchNames.append(ramp)

    sWall1 = re.compile('^s_wall\d$');
    listMeshSearchNames.append(sWall1)
    sWall3 = re.compile('^s_wall\d_\d+$');
    listMeshSearchNames.append(sWall3)
    sWall2 = re.compile('^s_wall\d_bsp$');
    listMeshSearchNames.append(sWall2)
    sWall4 = re.compile('^s_wall\d_\d+_bsp$');
    listMeshSearchNames.append(sWall4)

    lod = re.compile('^lod\d$');
    listMeshSearchNames.append(lod)
    hpModule1 = re.compile('^HP_module\d');
    listMeshSearchNames.append(hpModule1)

    return listMeshSearchNames


def vl_objectsMatValidNames():
    listMatSearchNames = []

    lambert = re.compile('^lambert1');
    listMatSearchNames.append(lambert)
    pCloud = re.compile('^particleCloud1');
    listMatSearchNames.append(pCloud)

    n_wood = re.compile('^n_wood_\d');
    listMatSearchNames.append(n_wood)
    n_stone = re.compile('^n_stone_\d');
    listMatSearchNames.append(n_stone)
    n_metal = re.compile('^n_metal_\d');
    listMatSearchNames.append(n_metal)
    n_metal = re.compile('^n_glass_\d');
    listMatSearchNames.append(n_metal)

    d_wood = re.compile('^d_wood_\d');
    listMatSearchNames.append(d_wood)
    d_stone = re.compile('^d_stone_\d');
    listMatSearchNames.append(d_stone)
    d_metal = re.compile('^d_metal_\d');
    listMatSearchNames.append(d_metal)

    s_wood = re.compile('^s_wood_\d');
    listMatSearchNames.append(s_wood)
    s_stone = re.compile('^s_stone_\d');
    listMatSearchNames.append(s_stone)
    s_metal = re.compile('^s_metal_\d');
    listMatSearchNames.append(s_metal)

    nd = re.compile('^s_nd_\d');
    listMatSearchNames.append(nd)
    ramp = re.compile('^s_ramp_\d');
    listMatSearchNames.append(ramp)
    wall = re.compile('^s_wall_\d');
    listMatSearchNames.append(wall)

    return listMatSearchNames


def listAllMat():
    objMat = cmds.ls(mat=True)
    return objMat


def vl_listAllTransforms():
    list_poly_meshes = cmds.ls(type='mesh', l=True)
    # maya bag fix - transform has strange shape - no visible in outliner
    real_meshes_list = cmds.filterExpand(list_poly_meshes, sm=12, fp=1)
    # maya bag fix end
    if not real_meshes_list:
        return []

    list_meshes_transform = []
    hp_modules = []
    for x in real_meshes_list:
        tr_full_path = cmds.listRelatives(x, p=True, f=True)
        check = tr_full_path[0].find("HP_")
        if check == -1:
            list_meshes_transform.append(tr_full_path[0])
        else:
            hp_modules.append(tr_full_path[0])

    list_meshes_transform = list(set(list_meshes_transform))

    return list_meshes_transform


def vl_listAllGroups():
    listTransformes = cmds.ls(type='transform', l=True)
    listAllGroups = []
    for x in listTransformes:
        if cmds.objectType(x) == "transform":
            temp = cmds.listRelatives(x, shapes=True)
            if temp == None:
                listAllGroups.append(x)
    return listAllGroups


def vl_listRootGroups():
    root_nodes = []
    for x in vl_listAllGroups():
        root_nodes.append(x.split("|")[1])

    return set(root_nodes)


def vl_listHPModules():
    listPolyMeshes = cmds.ls(type='mesh', l=True)
    hpModules = []
    for x in listPolyMeshes:
        trFullPath = cmds.listRelatives(x, p=True, f=True)
        check = trFullPath[0].find("HP_")
        if check != -1:
            hpModules.append(trFullPath[0])
    return hpModules


def vl_listLodsGroups():
    listTransforms = cmds.ls(type='transform')
    lodName = re.compile('lod\d', re.S)
    listLodsGroups = []

    for x in listTransforms:
        if lodName.match(x) and len(x) == 4:
            listLodsGroups.append(x)
    return listLodsGroups


def vl_findTracksInLods():
    cmds.bakePartialHistory(all=True)

    listHullsObject = []
    listTrackNames = []
    listTracks_R = []
    listTracks_L = []

    track_L = re.compile('track_L');
    listTrackNames.append(track_L)
    track_R = re.compile('track_R');
    listTrackNames.append(track_R)
    x_R = re.compile("_R")
    x_L = re.compile("_L")

    for z in vl_listLodsGroups():  # For each group found in vl_listLodsGroups()

        # List only track objects
        listObjects = cmds.listRelatives(z, c=True, f=True, ad=True)
        for x in listObjects:  # traversing lod group and trying to find track and hull objects
            for y in listTrackNames:
                if y.search(x):  # trying to find track_L or track_R mathes, and if succes:
                    if cmds.listRelatives(x, s=True) != None:  # if transform have connections it's mean it's mesh
                        if x_R.search(x):
                            listTracks_R.append(x)  # add founded track mesh to list

                        if x_L.search(x):
                            listTracks_L.append(x)

    return listTracks_R, listTracks_L


def vl_objMeshData():
    """   splited list format [groups_count, full_path, polycount, name, group, group, group, ... ]    """
    """                                                                                                """
    """   example:    [3, |env039_EngineerBridge_unique|lod0|s_0,  2732,   s_0,  env0,  lod0...]       """
    """                |                     |                       |      |      |      |            """
    """        parents group count       full path              polycount  name  group1 group2         """
    """               [0]                   [1]                    [2]     [3]    [4]    [5]           """

    meshDataList = []
    for x in vl_listAllTransforms():
        objPolycount = cmds.polyEvaluate(x, t=True)
        splitedList = x.split("|")
        del splitedList[0]
        length = len(splitedList)
        splitedList.append(objPolycount)
        splitedList.append(x)
        splitedList.append(length)
        list.reverse(splitedList)
        meshDataList.append(splitedList)
    # print  splitedList

    return meshDataList


# vl_objMaterialsData
#
#
#
#

def vl_objMaterialsData():
    # if object with index 3 (material name) = noMaterial

    """                                      matDataList[]                                              """
    """   splited list format [materials_count, full_path, obj_name, material, material, ... ]          """
    """                                                                                                 """
    """   example:    [2, |env039_EngineerBridge_unique|lod0|n_0,   n_0,   n_wood_0,  n_metal_0, ...]   """
    """                |                     |                       |        |           |             """
    """        materials count         obj full path              obj name   mat         mat            """
    """               [0]                   [1]                     [2]      [3]         [4]            """

    listTransforms = vl_listAllTransforms()
    matDataList = [[] for i in listTransforms]

    # Get all shape connections from transform:
    for x in range(len(listTransforms)):
        shapes = cmds.listRelatives(listTransforms[x], shapes=True, f=True)
        # Get surface shader from object Shading Engine
        # temp = cmds.listConnections (shapes, s=False, type = "shadingEngine")
        tmp = cmds.listHistory(shapes, f=1, ag=1)
        temp = []
        for obj in tmp:
            if cmds.nodeType(obj) == "shadingEngine":
                temp.append(obj)

        if temp != None:
            SG = temp
            SG = list(set(SG))
            for i in range(len(SG)):
                temp1 = cmds.listConnections(SG[i] + ".surfaceShader")
                if temp1 != None:
                    for y in temp1:
                        if y != None:
                            matDataList[x].append(y)
                        else:
                            matDataList[x].append("noMaterial!")
                else:
                    matDataList[x].append("noMaterial!")
        else:
            matDataList[x].append("noMaterial!")
        # errorText = " object doesn't have shadingEngine: " + listTransforms[x]
        # vl_appendToTextList(errorText, listTransforms[x])

        splitedList = listTransforms[x].split("|")
        # create list information about material in the scene. Described above ^^^.
        list.reverse(splitedList)
        matDataList[x].append(splitedList[0])
        matDataList[x].append(listTransforms[x])
        matDataList[x].append(len(SG))
        list.reverse(matDataList[x])
    # print  matDataList[x]
    return matDataList


def vl_lambert1Info():
    lambert1SG = cmds.listConnections("lambert1", type="shadingEngine")
    return lambert1SG


def vl_read_json(path=None, file_name=None):
    if not path or not file_name:
        return None
    json_file = open(("%s//%s") % (path, file_name))
    json_string = json_file.read()
    return json.loads(json_string)


def vl_scene_name(extension=False):
    rawFilePath = cmds.file(q=True, exn=True)
    name = rawFilePath.split("/")
    name = name[-1]
    return name[:-3]
