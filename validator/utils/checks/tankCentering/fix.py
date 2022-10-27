import maya.cmds as cmds
import maya.OpenMaya as OpenMaya


def unlockMesh():
    allMesh = cmds.ls(typ='transform', fl=True)
    for trans in allMesh:
        cmds.setAttr((trans + '.tx'), l=False)
        cmds.setAttr((trans + '.ty'), l=False)
        cmds.setAttr((trans + '.tz'), l=False)
        cmds.setAttr((trans + '.rx'), l=False)
        cmds.setAttr((trans + '.ry'), l=False)
        cmds.setAttr((trans + '.rz'), l=False)

        cmds.setAttr((trans + '.sx'), l=False)
        cmds.setAttr((trans + '.sy'), l=False)
        cmds.setAttr((trans + '.sz'), l=False)


def traverseMesh():
    storedData = []
    dagIter = OpenMaya.MItDag(OpenMaya.MItDag.kBreadthFirst, OpenMaya.MFn.kInvalid)
    while not dagIter.isDone():
        dagPath = OpenMaya.MDagPath()
        stat = dagIter.getPath(dagPath)
        if not stat:
            dagNode = OpenMaya.MFnDagNode(dagPath)
            if dagNode.isIntermediateObject() == False \
                    and dagPath.hasFn(OpenMaya.MFn.kMesh) == True \
                    and dagPath.hasFn(OpenMaya.MFn.kTransform) == False:
                storedData.append(dagPath)
        next(dagIter)
    return storedData


def findDifference():
    lod0Tracks = [];
    storedData = traverseMesh()
    if len(storedData) > 0:
        for x in storedData:
            if x.fullPathName().find("lod0") != -1 and x.fullPathName().find("track") != -1:
                lod0Tracks.append(x);
    if len(lod0Tracks) > 1:
        track_bbox = cmds.polyEvaluate(lod0Tracks[0].fullPathName(), lod0Tracks[1].fullPathName(), b=True)
        # select = OpenMaya.MSelectionList()

        lowestPoints = []

        def getLowestVertices(track):
            dagNode = OpenMaya.MFnDagNode(track)
            bbox = dagNode.boundingBox()
            ground = bbox.min()
            iterVertexes = OpenMaya.MItMeshVertex(track)

            while not iterVertexes.isDone():
                position = OpenMaya.MPoint()
                position = iterVertexes.position(OpenMaya.MSpace.kWorld)
                if round(position.y, 3) >= round(ground.y, 3) - 0.7 and round(position.y, 3) <= round(ground.y,
                                                                                                      3) + 0.7:
                    lowestPoints.append(position)
                    # select.add(track, iterVertexes.currentItem())
                next(iterVertexes)

        # getLowestVertices(lod0Tracks[0])
        # getLowestVertices(lod0Tracks[1])
        for track in lod0Tracks:
            getLowestVertices(track)

        cBbox = OpenMaya.MBoundingBox()
        for x in lowestPoints:
            cBbox.expand(x)

        return [round(cBbox.center().x, 3), round(cBbox.center().y, 3), round(cBbox.center().z, 3)]

    else:
        return [0, 0, 0]


def centring(x, y, z):
    unlockMesh()
    lods = cmds.ls('|lod*', fl=True, l=True, typ='transform')
    cmds.select(cl=True)
    for lod in lods:

        cmds.move(x, y, z, lod, r=True, wd=True)
        cmds.makeIdentity(lod, apply=True, t=1, r=1, s=1, n=0)
        cmds.xform(lod, rp=(0, 0, 0), sp=(0, 0, 0))

        chassis = cmds.ls(lod + '|chassis', l=True, typ='transform')
        if chassis:
            for chass in chassis:
                cmds.xform(chass, rp=(0, 0, 0), sp=(0, 0, 0))

    tracks = cmds.ls('track*', l=True, typ='transform')
    if tracks:
        for track in tracks:
            cmds.xform(track, rp=(0, 0, 0), sp=(0, 0, 0))


def messageBox(messageString):
    winName = "messageBox"
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)
    win = cmds.window(
        winName,
        title='Warning',
    );

    cmds.confirmDialog(title='Warning', message=messageString, button=['Ok'], defaultButton='Ok', cancelButton='No',
                       dismissString='No')


def main(*args):
    centerTank = []
    centerTank = findDifference()
    if abs(round(centerTank[0], 3) / 100) > 0.001 or abs(round(centerTank[2], 3) / 100) > 0.001:
        centring(centerTank[0] / -100, 0, centerTank[2] / -100)
        messageBox("Centered successfully X: " + str(round(centerTank[0] / 100, 3)) + "; Z: " + str(
            round(centerTank[2] / 100, 3)))
    else:
        messageBox("Already centered")
