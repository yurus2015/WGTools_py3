import maya.cmds as cmds


def load_plugin():
    if not cmds.pluginInfo('techartAPI', query=True, loaded=True):
        try:
            cmds.loadPlugin('techartAPI')
        except IOError:
            print('Don`t load plugin')


def map_border_hard():
    load_plugin()
    objects = cmds.filterExpand(sm=12)
    if objects:
        cmds.delete(objects, ch=1)
        map_borders = cmds.selectUVBorderEdge(he=1)
        cmds.select(objects)
