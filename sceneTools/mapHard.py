import maya.cmds as cmds


def loadPlugin():
    if not cmds.pluginInfo('techartAPI', query=True, loaded=True):
        try:
            cmds.loadPlugin('techartAPI')
        except:
            print('Don`t load plugin')


def mapToHard():
    loadPlugin()
    objects = cmds.filterExpand(sm=12)
    if objects:
        # for obj in objects:
        # cmds.polySoftEdge(obj, a = 180, ch = 0)
        cmds.delete(objects, ch=1)
        map_borders = cmds.selectUVBorderEdge(he=1)
        cmds.select(objects)
