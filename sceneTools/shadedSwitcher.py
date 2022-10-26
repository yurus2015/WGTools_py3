import maya.cmds as cmds


def main():
    viewport = cmds.getPanel(withFocus=True)
    if 'modelPanel' in viewport:
        appearance = cmds.modelEditor(viewport, q=True, displayAppearance=True)
        if appearance != 'smoothShaded':
            cmds.modelEditor(viewport, e=True, displayAppearance='smoothShaded')
        else:
            cmds.modelEditor(viewport, e=True, displayAppearance='wireframe')
