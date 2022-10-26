from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import sys
import maya.OpenMayaRender as OpenMayaRender
import maya.mel as mel
from maya.mel import eval as meval
from math import fmod
import time

toolId = 5004
toolLabel = "Overlap Find"


class overlapFindTool(QWidget):
    def __init__(self, parent=None):
        super(overlapFindTool, self).__init__(parent)

        self.initUI()

    def initUI(self):
        # create main layout
        self.mainLayout = QHBoxLayout(self)
        # self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        # self.mainLayout.setColumnMinimumWidth(1, 10)
        self.btn = QPushButton('Overlap Move ->')
        self.btn.resize(self.btn.sizeHint())
        self.mainLayout.addWidget(self.btn)
        self.connections()

    def connections(self):
        self.connect(self.btn, QtCore.SIGNAL("clicked()"), lambda: overlap_find())


def removeList(fromList, thisList):
    resultList = [n for n in fromList if n not in thisList]
    resultList = list(resultList)
    return resultList


def getDagPath(name):
    selectionList = OpenMaya.MSelectionList()
    selectionList.add(name)
    dagPath = OpenMaya.MDagPath()
    selectionList.getDagPath(0, dagPath)
    return dagPath


def intersect_(mesh, source, direction, testBothDirections=False, maxDist=9999999999):
    # Get meshFn
    meshFn = OpenMaya.MFnMesh(getDagPath(mesh))

    # Get source point
    sourcePt = OpenMaya.MFloatPoint(source[0] * 100, source[1] * 100, source[2] * 100)
    sourcePt2 = OpenMaya.MPoint(source[0] * 100, source[1] * 100, source[2] * 100)
    # Get direction vector
    directionVec = OpenMaya.MFloatVector(direction[0], direction[1], direction[2])
    directionVec2 = OpenMaya.MVector(direction[0], direction[1], direction[2])

    # Calculate intersection
    hitPtArray = OpenMaya.MFloatPointArray()
    hitPtArray2 = OpenMaya.MPointArray()
    hitFcArray = OpenMaya.MIntArray()

    meshFn.allIntersections(
        sourcePt, directionVec,
        None, None,
        False, OpenMaya.MSpace.kWorld,
        150, False,
        None,  # replace none with a mesh look up accelerator if needed
        False,
        hitPtArray,
        None, hitFcArray,
        None, None,
        None, 0.00001
    )

    # Return intersection hit faces

    return [hitFcArray[i] for i in range(hitFcArray.length())]


def deformMeshToUVSetLayout():
    # get the active selection
    selection = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selection)
    iterSel = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kGeometric)

    # go through selection
    while not iterSel.isDone():
        # get dagPath
        dagPath = OpenMaya.MDagPath()
        iterSel.getDagPath(dagPath)

        # create empty point array & float arrays
        inMeshMPointArray = OpenMaya.MPointArray()
        U_MFloatArray = OpenMaya.MFloatArray()
        V_MFloatArray = OpenMaya.MFloatArray()
        vertexCountMIntArray = OpenMaya.MIntArray()
        vertexListMIntArray = OpenMaya.MIntArray()
        uvCountsMIntArray = OpenMaya.MIntArray()
        uvIdsMIntArray = OpenMaya.MIntArray()

        # create function set, get points in world space & UVs
        meshFn = OpenMaya.MFnMesh(dagPath)
        meshFn.getPoints(inMeshMPointArray, OpenMaya.MSpace.kWorld)
        meshFn.getUVs(U_MFloatArray, V_MFloatArray)
        meshFn.getVertices(vertexCountMIntArray, vertexListMIntArray)
        meshFn.getAssignedUVs(uvCountsMIntArray, uvIdsMIntArray)

        # write UV postions to inMeshMPointArray
        for i in range(vertexListMIntArray.length()):
            inMeshMPointArray[vertexListMIntArray[i]].x = U_MFloatArray[uvIdsMIntArray[i]] * 100
            inMeshMPointArray[vertexListMIntArray[i]].y = V_MFloatArray[uvIdsMIntArray[i]] * 100
            inMeshMPointArray[vertexListMIntArray[i]].z = 0.001 * i

        # apply new point positions to mesh
        meshFn.setPoints(inMeshMPointArray, OpenMaya.MSpace.kWorld)

        iterSel.next()


def shellSelectMove(mesh, id):
    face = mesh + '.f[' + str(id) + ']'

    uvs = cmds.polyListComponentConversion(face, tuv=True)

    u_val = cmds.polyEditUV(uvs, query=True, u=1)

    if u_val[0] < 1:
        cmds.select(uvs)
        mel.eval('polySelectBorderShell 0')
        cmds.polyEditUV(u=1.0)


def shellMove(mesh, list_big):
    # s = list(set(list_small))
    b = list(set(list_big))

    f_b = []

    for id in b:
        f_bn = mesh + '.f[' + str(id) + ']'
        f_b.append(f_bn)

    if f_b:
        uvs = cmds.polyListComponentConversion(f_b, tuv=True)
        u_val = cmds.polyEditUV(uvs, query=True, u=1)

        # if u_val[0] < 1:
        cmds.select(uvs)
        mel.eval('polySelectBorderShell 0')
        cmds.polyEditUV(u=1.0)


def createRayDuplicate(baseMesh):
    # baseMesh = cmds.ls(sl =1, tr =1)
    refMesh = cmds.duplicate(baseMesh)
    cmds.polySplitVertex(refMesh[0])
    cmds.select(refMesh[0])
    deformMeshToUVSetLayout()
    cmds.setAttr(refMesh[0] + '.doubleSided', 1)

    return refMesh[0]


def createMaterialAlpha():
    shader = cmds.shadingNode('lambert', asShader=True, n="alphaHWShader")
    cmds.setAttr(shader + '.transparency', 0.5, 0.5, 0.5, type='double3')

    return shader


def createCameraAlpha():
    cameraName = cmds.camera(o=True, n='alphaHWCam')
    cmds.setAttr(cameraName[0] + '.translateX', 0.5)
    cmds.setAttr(cameraName[0] + '.translateY', 0.5)
    cmds.setAttr(cameraName[0] + '.translateZ', 10.0)
    return cameraName


def renderHW(camera, size):
    cmds.setAttr('defaultRenderGlobals.imageFormat', 7)
    fileName = cmds.hwRender(cam=camera,
                             width=size * 2, height=size * 2,
                             rs=True,
                             fixFileNameNumberPattern=True
                             )
    print('TEXTURE', fileName)
    return fileName


def faceIterator():
    # the OpenMaya module has many of the general Maya classes
    # note that some Maya classes require extra modules to use which is noted in the API docs
    # import maya.OpenMaya as OpenMaya
    baseMesh = cmds.ls(sl=1, tr=1)
    refMesh = createRayDuplicate(baseMesh[0])
    # This shows how to use the MSelectionList and MGlobal class
    # Get the selection and create a selection list of all the nodes meshes
    selection = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selection);

    # Create an MItSelectionList class to iterate over the selection
    # Use the MFn class to as a filter to filter node types
    iter = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kGeometric);

    polyList = []
    # This uses build in functions of the MItSelectionList class to loop through the list of objects
    # Note this is not a basic array you must use its built in functions iterate on its objects
    # Iterate through selection
    while not iter.isDone():

        # Get MDagPath from current iterated node
        dagPath = OpenMaya.MDagPath()
        iter.getDagPath(dagPath)

        # Get the selection as an MObject
        mObj = OpenMaya.MObject()
        iter.getDependNode(mObj)

        # This shows how to use the MItMeshPolygon class to work with meshes
        # Create an iterator for the polygons of the mesh
        iterPolys = OpenMaya.MItMeshPolygon(mObj)

        # Iterate through polys on current mesh
        while not iterPolys.isDone():
            centr = OpenMaya.MPoint
            # Get current polygons index
            centr = iterPolys.center()
            point = [centr.x, centr.y, centr.z]
            polyList.append(point)

            iterPolys.next()

        iter.next()

    direction = (0, 0, -1.0)
    allFaces = []
    for point in polyList:
        source = (point[0] / 100, point[1] / 100, 1.0)

        faces = intersect_(refMesh, source, direction)
        if len(faces) > 1:
            allFaces.extend(faces)

    cmds.delete(refMesh)
    shellMove(baseMesh[0], allFaces)
    cmds.select(baseMesh)


def pixelAlpha(sampling):
    ###################
    baseMesh = cmds.ls(sl=1, tr=1)
    shader = createMaterialAlpha()
    camera = createCameraAlpha()
    refMesh = createRayDuplicate(baseMesh[0])
    cmds.hyperShade(assign=shader)

    cmds.setAttr(camera[1] + '.orthographicWidth', 1.0)

    renderFilePath = renderHW(camera[1], sampling)

    direction = (0, 0, -1.0)

    firstFace = []
    allFaces = []
    ###################

    image = OpenMaya.MImage()
    # image.readFromTextureNode(file)
    image.readFromFile(renderFilePath)

    # grab the pixel array pointer
    pixelCharPtr = image.pixels()

    # get the size of the image
    scriptUtil = OpenMaya.MScriptUtil()

    widthPtr = scriptUtil.asUintPtr()
    heightPtr = scriptUtil.asUintPtr()

    scriptUtil.setUint(widthPtr, 0)
    scriptUtil.setUint(heightPtr, 0)

    image.getSize(widthPtr, heightPtr)

    width = scriptUtil.getUint(widthPtr)
    height = scriptUtil.getUint(heightPtr)
    size = width * height
    resulution = sampling
    for l in range(1, resulution):
        for m in range(1, resulution):
            u = l * (1.0 / resulution)
            v = m * (1.0 / resulution)

            # sample the correct pixel based on u and v coords
            x = int((width * u) + 0.5)
            y = int((height * v) + 0.5)

            i = (y * width) + x
            i = int(4 * (i - 1))  # pixels a stored in 4 byte blocks: rgba rgba rgba

            # read the colors (0-255) from the pixel char array
            # r = OpenMaya.MScriptUtil.getUcharArrayItem(pixelCharPtr, i)
            # g = OpenMaya.MScriptUtil.getUcharArrayItem(pixelCharPtr, i+1)
            # b = OpenMaya.MScriptUtil.getUcharArrayItem(pixelCharPtr, i+2)
            a = OpenMaya.MScriptUtil.getUcharArrayItem(pixelCharPtr, i + 3)

            # debug
            if a > 128:
                source = (u, v, 1.0)
                faces = intersect_(refMesh, source, direction)

                if len(faces) > 1:
                    allFaces.extend(faces)

    cmds.delete(refMesh)
    cmds.delete(shader)
    cmds.delete(camera)
    shellMove(baseMesh[0], allFaces)
    cmds.select(baseMesh)


def overlap_find():
    pixelAlpha(250)
    pixelAlpha(1000)
