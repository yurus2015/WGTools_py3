import maya.cmds as cmds
from maya.mel import eval as meval


def confirmDialog(msg, title=None):
    cmds.confirmDialog(title=title, message=msg, button=['   OK   '], defaultButton='   OK   ')


def combineObject(first=True):
    selected = cmds.ls(sl=True, fl=True, l=True, o=True)
    selected = cmds.filterExpand(sm=[12])
    if not selected:
        confirmDialog('Select two or more meshes', 'Error')
        return
    if len(selected) < 2:
        confirmDialog('Select two or more meshes', 'Error')
        return

    master = selected[0]
    masterShapes = cmds.listRelatives(master, s=True, path=True)
    combine = cmds.polyUnite(selected, ch=True)
    childShapes = cmds.listRelatives(combine[0], s=True, path=True)
    finalShape = cmds.rename(childShapes[0], masterShapes[0])
    finalShape = cmds.parent(finalShape, master, s=True)
    cmds.delete(master, ch=True)
    cmds.delete(combine[0])

    parentTransform = cmds.listRelatives(finalShape[0], f=True, p=True)
    cmds.makeIdentity(parentTransform, apply=True, t=1, r=1, s=1, n=0)
    cmds.parent(finalShape[0], master, s=True, addObject=True)
    cmds.delete(parentTransform)
    selected.remove(master)
    for unit in selected:
        if cmds.objExists(unit):
            cmds.delete(unit)

    shortName = master.split('|')[-1]
    masterShapes = cmds.listRelatives(master, s=True, path=True)
    cmds.select(masterShapes)
    evalCMD = 'renameSelectionList("' + shortName + 'Shape")'
    meval(evalCMD)
    cmds.select(master)
