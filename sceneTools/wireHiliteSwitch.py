import maya.cmds as cmds


def main():
    viewport = cmds.getPanel(withFocus=True)
    if 'modelPanel' in viewport:
        current_state = cmds.modelEditor(viewport, q=True, selectionHiliteDisplay=True)
        cmds.modelEditor(viewport, edit=True,
                         selectionHiliteDisplay=not current_state,
                         wireframeOnShaded=not current_state)
