import maya.cmds as cmds
from maya.mel import eval as meval

checkId = 412
checkLabel = "6.4 Group & Object Pivot"


def checkNameMesh(item):
    exeptNames = ['HP']
    # exeptMesh = []
    for name in exeptNames:
        if name in item:
            return True
    return False


def main():
    returnList = []
    onlyTransform = []

    listAlltransform = cmds.ls(type='transform')
    listAllMesh = cmds.ls(type='mesh', l=1)
    for tr in listAlltransform:
        shape = cmds.listRelatives(tr, s=1, f=1)
        if shape == None:
            onlyTransform.append(tr)
            # print 'TRANSFORM GROUP', tr

    for mesh in listAllMesh:
        tr = cmds.listRelatives(mesh, p=1, type='transform', f=1)
        if checkNameMesh(tr[0]) == False:
            onlyTransform.append(tr[0])
            # print 'TRANSFORM MESH', tr

    if onlyTransform:
        for obj in onlyTransform:
            rotatePivot = cmds.xform(obj, q=1, ws=1, rp=1)
            scalePivot = cmds.xform(obj, q=1, ws=1, sp=1)
            rotatePivot[0] = round(rotatePivot[0], 3)
            rotatePivot[1] = round(rotatePivot[1], 3)
            rotatePivot[2] = round(rotatePivot[2], 3)
            scalePivot[0] = round(scalePivot[0], 3)
            scalePivot[1] = round(scalePivot[1], 3)
            scalePivot[2] = round(scalePivot[2], 3)

            if rotatePivot != [0, 0, 0] or scalePivot != [0, 0, 0]:
                tmp = []
                tmp.append(obj + " has incorrect pivots world coordinates")
                tmp.append(obj)
                returnList.append(tmp)

    return returnList
