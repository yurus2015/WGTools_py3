# cmds.deleteUI('small_wnd')
# windows = cmds.window('small_wnd')
# cmds.paneLayout()
# pan = cmds.modelPanel()
# cam = cmds.modelPanel(pan, q=1, cam=1)
# cmds.modelEditor(pan, e=1, hud=0, displayAppearance = 'smoothShaded', wos=0)
# #modelEditor -edit -displayAppearance smoothShaded -activeOnly false modelPanel14;
# cam_copy = cmds.duplicate(cam)
# cmds.lookThru(cam_copy, pan)
# cmds.window(windows, e=1, wh = [400, 300])
# cmds.showWindow( windows )
import maya.cmds as cmds


def main(*args):
    try:
        cmds.deleteUI('small_wnd')
    except:
        pass

    try:
        cmds.delete('copy_cam')
    except:
        pass

    width = 400
    height = 300

    if args:
        width = args[0]
        height = args[1]

    windows = cmds.window('small_wnd')
    cmds.paneLayout()
    pan = cmds.modelPanel()
    cam = cmds.modelPanel(pan, q=1, cam=1)
    cmds.modelEditor(pan, e=1, hud=0, displayAppearance='smoothShaded', wos=0, sel=0)
    cam_copy = cmds.duplicate(cam, n='copy_cam')
    cmds.lookThru(cam_copy, pan)
    cmds.window(windows, e=1, wh=[width, height])
    cmds.showWindow(windows)

    if args:
        if args[2]:
            cmds.window(windows, e=1, le=args[2])
        if args[3]:
            cmds.window(windows, e=1, te=args[3])
