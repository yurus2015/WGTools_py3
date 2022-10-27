import maya.cmds as cmds


def load_plugin():
    if not cmds.pluginInfo('techartAPI', query=True, l=True):
        try:
            cmds.loadPlugin('techartAPI')
            return True
        except:
            return False
    # raise MissingPluginError('Unable to load techartAPI2018.mll!')
    else:
        return True


def main():
    return_list = []
    if load_plugin():

        all_meshes = cmds.ls(type="mesh", l=1, fl=1)
        for mesh in all_meshes:
            cmds.select(mesh)
            flat_vertex = cmds.selectFlatPoint()
            cmds.select(d=1)
            if len(flat_vertex):
                tmp = []
                transform = cmds.listRelatives(mesh, p=1, type='transform', f=1)[0]
                tmp.append(transform + ' has unnecessary vertex')
                tmp.append(flat_vertex)

                return_list.append(tmp)

    return return_list
