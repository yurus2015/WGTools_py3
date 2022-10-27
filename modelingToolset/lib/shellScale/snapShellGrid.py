import maya.cmds as cmds
import maya.OpenMaya as om
import math


def removeList(fromList, thisList):
    resultList = [n for n in fromList if n not in thisList]
    resultList = list(resultList)

    return resultList


def removeDupplicateList(currentList):
    resultList = list(set(currentList))

    return resultList


def boundinBox(shell):
    uvals, vvals = cmds.polyEvaluate(shell, bc2=True)

    return uvals, vvals


def gridSteps(value):
    texWinName = cmds.getPanel(sty='polyTexturePlacementPanel')
    cmds.textureWindow(texWinName[0], e=True, d=value)


def findNearest(value, step):
    div = value / step
    frac, whole = math.modf(div)
    if math.fabs(frac) <= 0.5:
        nearest = whole * step
    elif frac > 0.0:
        nearest = (whole + 1.0) * step
    else:
        nearest = (whole - 1.0) * step

    return nearest


def getUvShelList(name):  # only uvmap = False
    selList = om.MSelectionList()
    selList.add(name)
    selListIter = om.MItSelectionList(selList, om.MFn.kMesh)
    pathToShape = om.MDagPath()
    selListIter.getDagPath(pathToShape)
    meshNode = pathToShape.fullPathName()
    uvSets = cmds.polyUVSet(meshNode, query=True, currentUVSet=True)
    allSets = []
    shellArray = []
    for uvset in uvSets:
        shapeFn = om.MFnMesh(pathToShape)
        shells = om.MScriptUtil()
        shells.createFromInt(0)
        nbUvShells = shells.asUintPtr()

        uArray = om.MFloatArray()  # array for U coords
        vArray = om.MFloatArray()  # array for V coords
        uvShellIds = om.MIntArray()  # The container for the uv shell Ids

        shapeFn.getUVs(uArray, vArray)
        shapeFn.getUvShellsIds(uvShellIds, nbUvShells, uvset)

        # shellCount = shells.getUint(shellsPtr)
        shells = {}
        for i, n in enumerate(uvShellIds):
            if n in shells:
                # shells[n].append([uArray[i],vArray[i]])
                shells[n].append('%s.map[%i]' % (name, i))
            else:
                # shells[n] = [[uArray[i],vArray[i]]]
                shells[n] = ['%s.map[%i]' % (name, i)]
    return shells


def scaleShell(shell, step):
    uvals, vvals = boundinBox(shell)
    gridUmin = findNearest(uvals[0], step)
    gridVmin = findNearest(vvals[0], step)
    gridUmax = findNearest(uvals[1], step)
    gridVmax = findNearest(vvals[1], step)

    scaleU = (uvals[1] - gridUmin) / (uvals[1] - uvals[0])
    scaleV = (vvals[1] - gridVmin) / (vvals[1] - vvals[0])
    if scaleU == 0.0:
        scaleU = 1.0
    if scaleV == 0.0:
        scaleV = 1.0
    cmds.polyEditUV(shell, pivotU=uvals[1], pivotV=vvals[1], scaleU=scaleU, scaleV=scaleV)

    scaleU = (gridUmax - gridUmin) / (uvals[1] - gridUmin)
    scaleV = (gridVmax - gridVmin) / (vvals[1] - gridVmin)

    if scaleU == 0.0:
        scaleU = 1.0
    if scaleV == 0.0:
        scaleV = 1.0
    cmds.polyEditUV(shell, pivotU=gridUmin, pivotV=gridVmin, scaleU=scaleU, scaleV=scaleV)


def snapShell(value=512, grid=False, small=False):
    unsnappedShell = []
    selectedMesh = cmds.filterExpand(ex=True, sm=12)
    selectedComp = cmds.filterExpand(ex=True, sm=(31, 32, 34, 35))
    convertedUV = cmds.ls(cmds.polyListComponentConversion(selectedComp, tuv=True), fl=1)
    if grid:
        gridSteps(value)
    step = 1.0 / value
    if selectedMesh:
        for mesh in selectedMesh:
            shells = getUvShelList(mesh)
            for key, shell in shells.items():
                try:
                    scaleShell(shell, step)
                except:
                    print("Divide zero")
                    unsnappedShell.extend(shell)
                    continue

    if convertedUV:
        for uv in convertedUV:
            shell = cmds.polyListComponentConversion(uv, tuv=True, uvs=1)
            try:
                scaleShell(shell, step)
            except:
                print("Divide zero")
                unsnappedShell.extend(shell)
                continue

    cmds.select(d=1)
    if unsnappedShell and small:
        cmds.select(unsnappedShell)

    if not selectedMesh and not selectedComp:
        return True
