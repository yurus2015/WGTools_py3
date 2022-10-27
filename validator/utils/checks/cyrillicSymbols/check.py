import maya.cmds as cmds

checkId = 100
checkLabel = "Check for cyrillic symbols in names"


def is_cyrillic(name):
    for symbol in name:
        if '\u0400' <= symbol <= '\u04FF' or '\u0500' <= symbol <= '\u052F':
            return True


def main():
    return_list = []
    all_list = []
    error_message = " - The name contains cyrillic symbol"
    # scene name
    scene_name = cmds.file(q=1, sn=1, shn=1)
    if scene_name:
        if is_cyrillic(scene_name):
            tmp = ["The scene name contains cyrillic symbol", ""]
            return_list.append(tmp)

    # dag objects name
    dag_objects = cmds.ls(dag=1, ap=1)
    if dag_objects:
        all_list.extend(dag_objects)

    # layers name
    layers_name = cmds.ls(type='displayLayer')
    if layers_name:
        all_list.extend(layers_name)

    # materials name
    materials_name = cmds.ls(mat=1)
    if materials_name:
        all_list.extend(materials_name)

    # textures name
    textures_name = cmds.ls(tex=1)
    if textures_name:
        all_list.extend(textures_name)

    # 2d file name
    file2d_name = cmds.ls(type='file')
    if file2d_name:
        all_list.extend(file2d_name)

    # check cyrillic symbols
    if all_list:
        for obj in all_list:
            # print 'OBJ', obj,
            if is_cyrillic(obj):
                tmp = [obj + error_message, obj]
                return_list.append(tmp)

    return return_list
