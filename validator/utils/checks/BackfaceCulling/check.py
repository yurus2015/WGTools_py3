import maya.cmds as cmds


def main():
    #

    # objList = vl_listAllTransforms()
    return_list = []

    shape_array = cmds.ls(type='mesh', dag=1, l=True)
    if shape_array:
        poly_array = list(set(cmds.listRelatives(shape_array, p=1, type="transform", f=True)))

        for obj in poly_array:
            try:
                bc_status = cmds.getAttr(obj + ".backfaceCulling")
                if bc_status != 0:
                    tmp = [obj + " has the .backfaceCulling argument turned on", obj]
                    return_list.append(tmp)
            except ValueError:
                pass

    return return_list
