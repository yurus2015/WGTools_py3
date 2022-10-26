import maya.cmds as cmds


def main():
    viewport = cmds.getPanel(withFocus=True)
    if 'modelPanel' in viewport:
        current_state = cmds.modelEditor(viewport, q=True, wireframeOnShaded=True)
        cmds.modelEditor(viewport, edit=True, wireframeOnShaded=not current_state)
