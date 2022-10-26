import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaRender as OpenMayaRender

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

from shiboken2 import wrapInstance

import math
import time


class KeyboardEvents(QObject):
    def __init__(self):
        super(KeyboardEvents, self).__init__()

        self.view = OpenMayaUI.M3dView.active3dView()
        self.K_Ctrl = False
        self.K_Esc = False
        self.K_Shift = False

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key_Control:
                self.K_Ctrl = True
                self.view.refresh(True, True)

            if event.key() == Qt.Key_Shift:
                self.K_Shift = True
                self.view.refresh(True, True)

            if event.key() == Qt.Key_Escape:
                self.K_Esc = True
                self.view.refresh(True, True)

        if event.type() == QEvent.Type.KeyRelease:
            if event.key() == Qt.Key_Control:
                self.K_Ctrl = False
                self.view.refresh(True, True)

            if event.key() == Qt.Key_Shift:
                self.K_Shift = False
                self.view.refresh(True, True)

            if event.key() == Qt.Key_Escape:
                self.K_Esc = False
                self.view.refresh(True, True)


class MouseEvents(QObject):
    def __init__(self):
        super(MouseEvents, self).__init__()

        self.view = OpenMayaUI.M3dView.active3dView()
        self.M_Button_Left = False
        self.M_Button_Right = False
        self.M_Move = False
        self.M_posX = 0
        self.M_posY = 0

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == 1:
                self.M_posX = event.pos().x()
                self.M_posY = event.pos().y()
                self.M_Button_Left = True
                self.view.refresh(True, True)

            if event.button() == 2:
                self.M_posX = event.pos().x()
                self.M_posY = event.pos().y()
                self.M_Button_Right = True
                self.view.refresh(True, True)

        if event.type() == QEvent.Type.MouseButtonRelease:
            if event.button() == 1:
                self.M_Button_Left = False
                self.view.refresh(True, True)

            if event.button() == 2:
                self.M_Button_Right = False
                self.view.refresh(True, True)


'''
Class MPxPainter
Main idea is to draw openGL without creating any type of node keeping a scene clean and tight
'''


class MPxPainter(object):

    def __init__(self):
        self.callback = None
        self.currentModelPanel = None
        self.view3D = None
        self.userKeyboardEvents = KeyboardEvents()
        self.userMouseEvents = MouseEvents()
        self.qt_Active_View = None
        self.qt_Maya_Window = None

        self.unit = 1.0

        self.GLRenderer = None
        self.GL = None

        self.initializeGL()
        self.initializeCallback()

    def initializeGL(self):
        # scene measure units
        unit = cmds.currentUnit(q=1, linear=1)
        if unit == "m":
            self.unit = float(self.unit) * 100.0

        self.GLRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
        self.GL = self.GLRenderer.glFunctionTable()

    def initializeCallback(self):
        # get current 3dView pointer
        self.view3D = OpenMayaUI.M3dView.active3dView()

        # get current model panel
        self.currentModelPanel = cmds.getPanel(vis=1)

        for i in self.currentModelPanel:
            if "modelPanel" in i:
                self.currentModelPanel = i

        # if "modelPanel" not in self.currentModelPanel:
        #     cmds.error("Set a 3DViewport active by clicking a mouse button on an empty space")
        #     return
        # try removing old callbacks from the memory
        try:
            OpenMayaUI.MUiMessage.removeCallback(self.callBack)
        except:
            pass

        # create a callback that is registered after a frame is drawn with a 3D content but before 2D content
        self.callback = OpenMayaUI.MUiMessage.add3dViewPostRenderMsgCallback(self.currentModelPanel, self.draw)
        self.view3D.refresh(True, True)

        # create QT maya window event filter
        main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        self.qt_Maya_Window = wrapInstance(int(main_window_ptr), QObject)
        self.qt_Maya_Window.installEventFilter(self.userKeyboardEvents)

        # create viewport event filter
        active_view_ptr = self.view3D.widget()
        self.qt_Active_View = wrapInstance(int(active_view_ptr), QObject)
        self.qt_Active_View.installEventFilter(self.userMouseEvents)

        inViewMessageEnable = cmds.optionVar(q='inViewMessageEnable')
        if inViewMessageEnable == 0:
            cmds.optionVar(iv=('inViewMessageEnable', 1))
        cmds.inViewMessage(
            amg='<hl>Angle Measuring Tool:</hl> Use <hl>"Left CTRL"</hl> + <hl>"Mouse Click"</hl> to span the Tool to the face.',
            pos='botLeft', fade=True)

    def uninitializeCallback(self):
        OpenMayaUI.MUiMessage.removeCallback(self.callback)  # remove 3dView Render Callback

        self.qt_Maya_Window.removeEventFilter(self.userKeyboardEvents)  # remove QT Callback
        self.qt_Active_View.removeEventFilter(self.userMouseEvents)  # remove QT Callback

        OpenMayaUI.M3dView.active3dView().refresh(True, True)
        OpenMayaUI.M3dView.active3dView().refresh(True, True)

        print("Tool has been uninitialized")

    def getMouseIntersect(self):
        sourcePnt = OpenMaya.MPoint(0, 0, 0)
        rayDir = OpenMaya.MVector(0, 0, 0)
        maximumDistance = 9999999999
        viewHeight = self.view3D.portHeight()
        intersectedPoint = OpenMaya.MFloatPoint()
        hitNormal = OpenMaya.MVector()
        intersectedObject = ""

        intersectedFace = 0
        hitFace = OpenMaya.MScriptUtil()
        hitFace.createFromInt(0)
        hitFacePtr = hitFace.asIntPtr()

        hitDistance = OpenMaya.MScriptUtil(0.0)
        hitDistancePtr = hitDistance.asFloatPtr()

        self.view3D.viewToWorld(int(self.userMouseEvents.M_posX), int(viewHeight - self.userMouseEvents.M_posY),
                                sourcePnt, rayDir)

        source = OpenMaya.MFloatPoint(sourcePnt.x, sourcePnt.y, sourcePnt.z)
        direction = OpenMaya.MFloatVector(rayDir.x, rayDir.y, rayDir.z).normal()

        iter = OpenMaya.MItDependencyNodes(OpenMaya.MFn.kMesh)

        while not iter.isDone():
            node = iter.thisNode()
            dagPath = OpenMaya.MDagPath.getAPathTo(node)

            hitPoint = OpenMaya.MFloatPoint()
            source = OpenMaya.MFloatPoint(source.x, source.y, source.z)
            direction = OpenMaya.MFloatVector(direction.x, direction.y, direction.z)

            if dagPath.isVisible():
                mesh = OpenMaya.MFnMesh(dagPath)
                intersected = mesh.closestIntersection(source, direction, None, None, False, OpenMaya.MSpace.kWorld,
                                                       9999999999, True, None, hitPoint, hitDistancePtr, hitFacePtr,
                                                       None, None, None, 0.0001)

                if intersected:
                    intersectionDistance = hitDistance.getFloat(hitDistancePtr)
                    if intersectionDistance < maximumDistance:
                        maximumDistance = intersectionDistance
                        intersectedPoint = hitPoint
                        intersectedFace = OpenMaya.MScriptUtil(hitFacePtr).asInt()
                        mesh.getClosestNormal(OpenMaya.MPoint(intersectedPoint), hitNormal, OpenMaya.MSpace.kWorld)
                        intersectedObject = dagPath.fullPathName()

            iter.next()

        if intersectedPoint.x + intersectedPoint.y + intersectedPoint.z == 0:
            return False, False, False
        else:
            return intersectedPoint, intersectedFace, intersectedObject

    def draw(self, *args):
        pass


'''
Overriden MPxPainter class: Angle Tool
'''


class AngleTool(MPxPainter):
    def __init__(self):
        self.hitPoint = OpenMaya.MFloatPoint(0, 0, 0)
        self.hitFace = None
        self.hitObjectName = None

        super(AngleTool, self).__init__()

    def getpolyFaceCenter(self, face):
        resultCenter = OpenMaya.MFloatPoint()
        resultNormal = OpenMaya.MVector()

        selectionList = OpenMaya.MSelectionList()
        selectionList.clear()
        selectionList.add(face)

        dagPath = OpenMaya.MDagPath()
        mObject = OpenMaya.MObject()

        selectionList.getDagPath(0, dagPath, mObject)

        iter = OpenMaya.MItMeshPolygon(dagPath, mObject)

        while not iter.isDone():
            resultCenter = iter.center(OpenMaya.MSpace.kWorld)
            iter.getNormal(resultNormal, OpenMaya.MSpace.kWorld)

            iter.next()

        return resultCenter, resultNormal

    def drawOffset(self, rotX=0, rotY=0, rotZ=0, angX=0, angY=0, angZ=0, rad=0, dirX_1=1, dirX_2=1, dirZ_1=1, dirZ_2=1,
                   polyFaceCenter=None, polyFaceVector=None):
        # angX = 62.393321991
        # angY = 10.4186573029
        # angZ = 19.3723316193
        # rad = 50
        posX = polyFaceCenter.x
        posY = polyFaceCenter.y
        posZ = polyFaceCenter.z

        trX = 0
        trY = 0
        trZ = 0

        slX = 1
        slY = 1
        slZ = 1

        # dirX_1 = 1
        # dirX_2 = -1
        # dirZ_1 = 1
        # dirZ_2 = 1
        seg = 100

        '''DRAW X________________________________________________________________________________'''

        self.GL.glEnable(OpenMayaRender.MGL_BLEND)
        self.GL.glBlendFunc(OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA)
        self.GL.glColor4f(1, 0, 0, 0.5)

        '''circle X'''
        self.GL.glBegin(OpenMayaRender.MGL_TRIANGLE_FAN)

        for i in range(seg):  # seg
            x = math.cos(math.radians((angX / 100) * float(i)))
            y = math.sin(math.radians((angX / 100) * float(i)))
            x1 = math.cos(math.radians((angX / 100) * float(i + 1)))
            y1 = math.sin(math.radians((angX / 100) * float(i + 1)))

            self.GL.glVertex3f(trX + posX, trY + posY, trZ + posZ)
            self.GL.glVertex3f(dirX_1 * (x * slX * rad + trX) + posX, dirX_2 * (y * slY * rad + trY) + posY,
                               0.0 * slZ + trZ + posZ)
            self.GL.glVertex3f(dirX_1 * (x1 * slX * rad + trX) + posX, dirX_2 * (y1 * slY * rad + trY) + posY,
                               0.0 * slZ + trZ + posZ)

        self.GL.glEnd()

        # '''lines X'''
        self.GL.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_LINE)
        self.GL.glLineWidth(3)

        self.GL.glColor4f(1, 0, 0, 1)
        self.GL.glBegin(OpenMayaRender.MGL_LINES)

        x = math.cos(math.radians((angX / 100) * float(0)))
        y = math.sin(math.radians((angX / 100) * float(0)))
        # static coordinate
        self.GL.glVertex3f(trX + posX, trY + posY, trZ + posZ)
        self.GL.glVertex3f(dirX_1 * (2 * x * slX * rad + trX) + posX, 0.0 * slY * rad + trY + posY,
                           dirX_2 * (2 * y * slZ * rad + trZ) + posZ)
        self.GL.glEnd()

        self.GL.glBegin(OpenMayaRender.MGL_LINES)
        x = math.cos(math.radians(angX))
        y = math.sin(math.radians(angX))
        x1 = math.cos(math.radians(angX))
        y1 = math.sin(math.radians(angX))
        self.GL.glVertex3f(trX + posX, trY + posY, trZ + posZ)
        self.GL.glVertex3f(dirX_1 * (2 * x1 * slX * rad + trX) + posX, dirX_2 * (2 * y1 * slY * rad + trY) + posY,
                           0.0 * slZ + trZ + posZ)
        self.GL.glEnd()

        '''text X'''
        # self.GL.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
        self.GL.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_FILL)

        x1 = math.cos(math.radians((angX / 100) * float(50)))
        y1 = math.sin(math.radians((angX / 100) * float(50)))

        textPos = math.sqrt(math.fabs(500 - math.fabs(angX)) / 100)

        textX = dirX_1 * (x1 * slX * rad * textPos + trX)
        textY = dirX_2 * (y1 * slY * rad * textPos + trY)
        textZ = 0.0 * slZ * rad * textPos + trZ

        fixedTextX = textX
        fixedTextY = textY
        fixedTextZ = textZ

        if rotY == 90:
            fixedTextX = textZ
            fixedTextZ = -textX
        elif rotY == -90:
            fixedTextX = -textZ
            fixedTextZ = textX
        elif rotY == 180:
            fixedTextZ = -textZ
            fixedTextX = -textX
        else:
            fixedTextZ = -textZ
            fixedTextX = textX
            fixedTextY = textY

        if rotZ == -180:
            fixedTextY = -textY
            if rotY == 90:
                fixedTextZ = textX
            elif rotY == -90:
                fixedTextX = textZ
                fixedTextZ = -textX
            elif rotY == -180:
                fixedTextX = -textZ
            else:
                fixedTextX = -textX
                fixedTextY = -textY

        fixedTextX += posX
        fixedTextY += posY
        fixedTextZ += posZ

        self.view3D.drawText(round(angX, 2), OpenMaya.MPoint(fixedTextX, fixedTextY, fixedTextZ), self.view3D.kCenter)

        '''DRAW Y________________________________________________________________________________'''

        self.GL.glEnable(OpenMayaRender.MGL_BLEND)
        self.GL.glBlendFunc(OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA)
        self.GL.glColor4f(0, 1, 0, 0.5)

        '''circle Y'''

        self.GL.glBegin(OpenMayaRender.MGL_TRIANGLE_FAN)

        for i in range(seg):
            x = math.cos(math.radians((angY / 100) * float(i)))
            y = math.sin(math.radians((angY / 100) * float(i)))
            x1 = math.cos(math.radians((angY / 100) * float(i + 1)))
            y1 = math.sin(math.radians((angY / 100) * float(i + 1)))

            self.GL.glVertex3f(0 * slX + trX + posX, 0 * slY + trY + posY, 0 * slZ + trZ + posZ)
            self.GL.glVertex3f(0.0 * slX + trX + posX, x * slY * rad + trY + posY, y * slZ * rad + trZ + posZ)
            self.GL.glVertex3f(0.0 * slX + trX + posX, x1 * slY * rad + trY + posY, y1 * slZ * rad + trZ + posZ)

        self.GL.glEnd()

        '''lines Y'''
        self.GL.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_LINE)
        self.GL.glLineWidth(3)

        self.GL.glColor4f(0, 1, 0, 1)

        self.GL.glBegin(OpenMayaRender.MGL_LINES)

        x = math.cos(math.radians((angY / 100) * float(0)))
        y = math.sin(math.radians((angY / 100) * float(0)))
        # static coordinate
        self.GL.glVertex3f(0 * slX + trX + posX, 0 * slY + trY + posY, 0 * slZ + trZ + posZ)
        self.GL.glVertex3f(0.0 * slX + trX + posX, 2 * x * slY * rad + trY + posY, y * slZ * rad + trZ + posZ)

        self.GL.glEnd()

        self.GL.glBegin(OpenMayaRender.MGL_LINES)

        x = math.cos(math.radians(angY))
        y = math.sin(math.radians(angY))
        x1 = math.cos(math.radians(angY))
        y1 = math.sin(math.radians(angY))

        self.GL.glVertex3f(0.0 * slX + trX + posX, 0.0 * slY * rad + trY + posY, 0.0 * y * slZ * rad + trZ + posZ)
        self.GL.glVertex3f(0.0 * slX + trX + posX, 2 * x1 * slY * rad + trY + posY, 2 * y1 * slZ * rad + trZ + posZ)

        self.GL.glEnd()

        self.GL.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_FILL)

        # compute position for deegres values
        x1 = math.cos(math.radians((angY / 100) * float(49 + 1)))
        y1 = math.sin(math.radians((angY / 100) * float(49 + 1)))

        # function y(x)= x2*100-420
        textPos = math.sqrt(math.fabs(420 - math.fabs(angY)) / 100)

        textX = 0.0 * slX * textPos + trX
        textY = x1 * slY * rad * textPos + trY
        textZ = y1 * slZ * rad * textPos + trZ

        fixedTextX = textX
        fixedTextY = textY
        fixedTextZ = textZ

        if rotY == 90:
            fixedTextX = textZ
            fixedTextZ = -textX
        elif rotY == -90:
            fixedTextX = -textZ
            fixedTextZ = textX
        elif rotY == 180:
            fixedTextZ = -textZ
            fixedTextX = -textX
        else:
            # fixedTextZ = -textZ
            fixedTextX = textX
            fixedTextY = textY

        if rotZ == -180:
            fixedTextY = -textY
            if rotY == 90:
                fixedTextZ = textX
            elif rotY == -90:
                fixedTextX = textZ
                fixedTextZ = -textX
            elif rotY == -180:
                fixedTextX = -textZ
            else:
                fixedTextX = -textX
                fixedTextY = -textY
                # fixedTextZ = textZ

        fixedTextX += posX
        fixedTextY += posY
        fixedTextZ += posZ

        self.view3D.drawText(round(angY, 2), OpenMaya.MPoint(fixedTextX, fixedTextY, fixedTextZ), self.view3D.kCenter)

        '''DRAW Z________________________________________________________________________________'''
        self.GL.glEnable(OpenMayaRender.MGL_BLEND)
        self.GL.glBlendFunc(OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA)
        self.GL.glColor4f(0, 0, 1, 0.5)

        '''circle Z'''
        self.GL.glBegin(OpenMayaRender.MGL_TRIANGLE_FAN)

        for i in range(seg):
            x = math.cos(math.radians((angZ / 100) * float(i)))
            y = math.sin(math.radians((angZ / 100) * float(i)))
            x1 = math.cos(math.radians((angZ / 100) * float(i + 1)))
            y1 = math.sin(math.radians((angZ / 100) * float(i + 1)))

            self.GL.glVertex3f(0 * slX + trX + posX, 0 * slY + trY + posY, 0 * slZ + trZ + posZ)
            self.GL.glVertex3f(dirZ_1 * (x * slX * rad + trX) + posX, 0.0 * slY + trY + posY,
                               dirZ_2 * (y * slZ * rad + trZ) + posZ)
            self.GL.glVertex3f(dirZ_1 * (x1 * slX * rad + trX) + posX, 0.0 * slY + trY + posY,
                               dirZ_2 * (y1 * slZ * rad + trZ) + posZ)

        self.GL.glEnd()

        self.GL.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_LINE)
        self.GL.glLineWidth(3)

        '''lines Z'''
        self.GL.glColor4f(0, 0, 1, 1)
        self.GL.glBegin(OpenMayaRender.MGL_LINES)

        x = math.cos(math.radians((angZ / 100) * float(0)))
        y = math.sin(math.radians((angZ / 100) * float(0)))

        # static coordinate
        self.GL.glVertex3f(0 * slX + trX + posX, 0 * slY + trY + posY, 0 * slZ + trZ + posZ)
        self.GL.glVertex3f(dirZ_1 * (2 * x * slX * rad + trX) + posX, 0.0 * slY + trY + posY,
                           dirZ_2 * (2 * y * slZ * rad + trZ) + posZ)

        self.GL.glEnd()

        self.GL.glBegin(OpenMayaRender.MGL_LINES)

        x = math.cos(math.radians(angZ))
        y = math.sin(math.radians(angZ))
        x1 = math.cos(math.radians(angZ))
        y1 = math.sin(math.radians(angZ))

        self.GL.glVertex3f(0.0 * slX + trX + posX, 0.0 * slY * rad + trY + posY, 0.0 * y * slZ * rad + trZ + posZ)
        self.GL.glVertex3f(dirZ_1 * (2 * x1 * slX * rad + trX) + posX, 0.0 * slY + trY + posY,
                           dirZ_2 * (2 * y1 * slZ * rad + trZ) + posZ)

        self.GL.glEnd()

        '''text Z'''
        self.GL.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_FILL)

        x1 = math.cos(math.radians((angZ / 100) * float(49 + 1)))
        y1 = math.sin(math.radians((angZ / 100) * float(49 + 1)))

        # function y(x)= x2*100-420
        textPos = math.sqrt(math.fabs(420 - math.fabs(angZ)) / 100)

        textX = dirZ_1 * (x1 * slX * rad * textPos + trX)
        textY = 0.0 * slY * rad * textPos + trY
        textZ = dirZ_2 * (y1 * slZ * rad * textPos + trZ)

        fixedTextX = textX
        fixedTextY = textY
        fixedTextZ = textZ

        if rotY == 90:
            fixedTextX = textZ
            fixedTextZ = -textX
        elif rotY == -90:
            fixedTextX = -textZ
            fixedTextZ = textX
        elif rotY == 180:
            fixedTextZ = -textZ
            fixedTextX = -textX
        else:
            fixedTextZ = textZ
            fixedTextX = textX
            fixedTextY = -textY

        if rotZ == -180:
            fixedTextY = -textY
            if rotY == 90:
                fixedTextZ = textX
            elif rotY == -90:
                fixedTextX = textZ
                fixedTextZ = -textX
            elif rotY == -180:
                fixedTextX = -textZ
            else:
                fixedTextX = -textX
                fixedTextY = -textY

        fixedTextX += posX
        fixedTextY += posY
        fixedTextZ += posZ

        self.view3D.drawText(round(angZ, 2), OpenMaya.MPoint(fixedTextX, fixedTextY, fixedTextZ), self.view3D.kCenter)

    def calculateOffset(self, polyFaceCenter=None, polyFaceVector=None):
        angleX = 0
        angleY = 0
        angleZ = 0
        directionX_1 = 1
        directionX_2 = 1
        directionZ_1 = 1
        directionZ_2 = 1

        rotX = 0
        rotY = 0
        rotZ = 0

        # get yaw angle
        a = OpenMaya.MVector()
        a.x = polyFaceVector.x
        a.y = 0
        a.z = polyFaceVector.z
        yaw = round(math.degrees(a.angle(OpenMaya.MVector.zAxis)), 3)

        # determine face vector y coordinate d = (1) - positive; d = (-1)-negative;
        d = 1
        if polyFaceVector.y < 0:
            rotZ = -180
            d = -1

        '''X'''
        if yaw <= 45:
            a.x = polyFaceVector.x
            a.y = polyFaceVector.y
            a.z = 0;

            angleX = math.degrees(a.angle(OpenMaya.MVector.xAxis));
            angleX = abs(-90 + angleX)

        elif yaw <= 180 and yaw >= 135:
            a.x = polyFaceVector.x
            a.y = polyFaceVector.y
            a.z = 0
            angleX = math.degrees(a.angle(OpenMaya.MVector.xAxis))
            angleX = abs(-90 + angleX)



        elif yaw > 45 and yaw < 135:
            a.x = 0
            a.y = polyFaceVector.y
            a.z = polyFaceVector.z
            angleX = math.degrees(a.angle(OpenMaya.MVector.zAxis))
            angleX = abs(-90 + angleX)

        '''Y'''
        if yaw <= 45:
            a.x = 0
            a.y = polyFaceVector.y
            a.z = polyFaceVector.z
            angleY = math.degrees(a.angle(OpenMaya.MVector.zAxis))
            if angleY > 90:
                angleY = 180 - (math.degrees(a.angle(OpenMaya.MVector.zAxis)))
            rotY = 180 * d


        elif yaw <= 180 and yaw >= 135:
            a.x = 0
            a.y = polyFaceVector.y
            a.z = polyFaceVector.z
            angleY = math.degrees(a.angle(OpenMaya.MVector.zAxis))
            if angleY > 90:
                angleY = 180 - (math.degrees(a.angle(OpenMaya.MVector.zAxis)))


        elif yaw > 45 and yaw < 135:
            a.x = polyFaceVector.x
            a.y = polyFaceVector.y
            a.z = 0
            angleY = math.degrees(a.angle(OpenMaya.MVector.xAxis))
            if angleY > 90:
                angleY = 180 - (math.degrees(a.angle(OpenMaya.MVector.xAxis)))

            if polyFaceVector.x > 0:  # face normal directed +X
                rotY = -90
            else:  # face normal
                rotY = 90

        '''Z'''
        if yaw <= 45:
            a.x = polyFaceVector.x
            a.y = 0
            a.z = polyFaceVector.z
            angleZ = math.degrees(a.angle(OpenMaya.MVector.zAxis))
            if angleZ > 90:
                angleZ = 180 - (math.degrees(a.angle(OpenMaya.MVector.zAxis)))



        elif yaw >= 135:
            a.x = polyFaceVector.x
            a.y = 0
            a.z = polyFaceVector.z

            angleZ = math.degrees(a.angle(-OpenMaya.MVector.zAxis))
            if angleZ > 90:
                angleZ = 180 - (math.degrees(a.angle(-OpenMaya.MVector.zAxis)))

        elif yaw > 45 and yaw < 135:
            a.x = polyFaceVector.x
            a.y = 0
            a.z = polyFaceVector.z
            angleZ = math.degrees(a.angle(OpenMaya.MVector.xAxis))
            if angleZ > 90:
                angleZ = 180 - (math.degrees(a.angle(OpenMaya.MVector.xAxis)))

        X = polyFaceVector.x
        Y = polyFaceVector.y
        Z = polyFaceVector.z

        if Z > 0 and X > 0 and Y > 0:
            quadrant = 1
            if yaw <= 45:
                directionZ_1 = -1
                directionX_1 = -1
                directionX_2 = -1
            elif yaw > 45 and yaw < 90:
                directionX_2 = -1

        if Z < 0 and X > 0 and Y > 0:
            quadrant = 2
            if yaw > 90 and yaw < 135:
                directionZ_1 = -1
                directionX_1 = -1
                directionX_2 = -1
            elif yaw >= 135 and yaw < 180:
                directionX_2 = -1

        if Z < 0 and X < 0 and Y > 0:
            quadrant = 3
            if yaw >= 135 and yaw < 180:
                directionZ_1 = -1
                directionX_1 = -1
                directionX_2 = -1
            elif yaw >= 90 and yaw < 135:
                directionX_2 = -1

        if Z > 0 and X < 0 and Y > 0:
            quadrant = 4
            if yaw > 45 and yaw < 90:
                directionZ_1 = -1
                directionX_1 = -1
                directionX_2 = -1
            elif yaw <= 45:
                directionX_2 = -1

        if Z > 0 and X > 0 and Y < 0:
            quadrant = 5
            if yaw <= 45:
                directionX_2 = -1
            elif yaw > 45 and yaw < 90:
                directionZ_1 = -1
                directionX_1 = -1
                directionX_2 = -1

        if Z < 0 and X > 0 and Y < 0:
            quadrant = 6
            if yaw > 90 and yaw < 135:
                directionX_2 = -1
            elif yaw >= 135 and yaw < 180:
                directionZ_1 = -1
                directionX_1 = -1
                directionX_2 = -1

        if Z < 0 and X < 0 and Y < 0:
            quadrant = 7
            if yaw >= 135 and yaw < 180:
                directionX_2 = -1
            elif yaw >= 90 and yaw < 135:
                directionZ_1 = -1
                directionX_1 = -1
                directionX_2 = -1

        if Z > 0 and X < 0 and Y < 0:
            quadrant = 8
            if yaw > 45 and yaw < 90:
                directionX_2 = -1
            elif yaw <= 45:
                directionZ_1 = -1
                directionX_1 = -1
                directionX_2 = -1

        return angleX, angleY, angleZ, directionX_1, directionX_2, directionZ_1, directionZ_2, rotX, rotY, rotZ

    def draw(self, *args):
        ''' callback processing '''
        if self.userKeyboardEvents.K_Esc:
            self.uninitializeCallback()
            return

        if self.userMouseEvents.M_Button_Left:
            if self.userKeyboardEvents.K_Ctrl:
                self.hitPoint, self.hitFace, self.hitObjectName = self.getMouseIntersect()

        if self.hitFace == None or self.hitObjectName == None: return

        '''Get intersected MFloatPoint and intersected faceId'''

        polyFaceCenter, polyFaceVector = self.getpolyFaceCenter(self.hitObjectName + ".f[" + str(self.hitFace) + "]")

        polyFaceCenter.x = round(polyFaceCenter.x, 3)
        polyFaceCenter.y = round(polyFaceCenter.y, 3)
        polyFaceCenter.z = round(polyFaceCenter.z, 3)

        polyFaceVector.x = round(polyFaceVector.x, 3)
        polyFaceVector.y = round(polyFaceVector.y, 3)
        polyFaceVector.z = round(polyFaceVector.z, 3)

        '''Calculate offset angles'''

        angXVal, angYVal, angZVal, dirX_1Val, dirX_2Val, dirZ_1Val, dirZ_2Val, rotX, rotY, rotZ = self.calculateOffset(
            polyFaceCenter=polyFaceCenter, polyFaceVector=polyFaceVector)

        '''__OpenGL__'''

        self.GL.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
        self.view3D.beginGL()

        self.GL.glClearDepth(0.0)
        self.GL.glDepthFunc(OpenMayaRender.MGL_ALWAYS)

        self.GL.glPushMatrix()
        self.GL.glTranslatef(polyFaceCenter.x, polyFaceCenter.y, polyFaceCenter.z)
        self.GL.glRotatef(rotY, 0, 1, 0)
        self.GL.glRotatef(rotZ, 0, 0, 1)
        self.GL.glTranslatef(-polyFaceCenter.x, -polyFaceCenter.y, -polyFaceCenter.z)

        # self.drawOffset(angX = 62.393321991,
        # angY = 45.4186573029,
        # angZ = 19.3723316193,
        # rad = 50,
        # dirX_1 = 1,
        # dirX_2 = -1,
        # dirZ_1 = 1,
        # dirZ_2 = 1,
        # polyFaceCenter = polyFaceCenter)

        self.drawOffset(rotX=rotX, rotY=rotY, rotZ=rotZ, angX=angXVal, angY=angYVal, angZ=angZVal, rad=0.5 * self.unit,
                        dirX_1=dirX_1Val, dirX_2=dirX_2Val, dirZ_1=dirZ_1Val, dirZ_2=dirZ_2Val,
                        polyFaceCenter=polyFaceCenter)
        self.GL.glPopMatrix()

        self.view3D.endGL()
        self.GL.glPopAttrib()


def main():
    instance = AngleTool()
