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
        self.K_Alt = False

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

            if event.key() == Qt.Key_Alt:
                self.K_Alt = True
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

            if event.key() == Qt.Key_Alt:
                self.K_Alt = False
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
        self.editMode = False

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

        if event.type() == QEvent.Type.MouseMove:
            self.M_posX = event.pos().x()
            self.M_posY = event.pos().y()
            self.M_Move = True
            self.view.refresh(True, True)

        if self.editMode:
            return True


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

        self.glFT = None

        self.initializeGL()
        self.initializeCallback()

    def initializeGL(self):
        # scene measure units
        unit = cmds.currentUnit(q=1, linear=1)
        if unit == "m":
            self.unit = float(self.unit) * 100.0

        self.glFT = OpenMayaRender.MHardwareRenderer.theRenderer().glFunctionTable()

    def initializeCallback(self):
        # get current 3dView pointer
        self.view3D = OpenMayaUI.M3dView.active3dView()

        # get current model panel
        self.currentModelPanel = cmds.getPanel(vis=1)

        for i in self.currentModelPanel:
            if "modelPanel" in i:
                self.currentModelPanel = i

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
            amg='<hl>Ruller Tool:</hl>\n<span style=\"color:#FFFFFF;\"> Use </span><hl>"Left CTRL"</hl> + <hl>"Mouse Click"</hl><span style=\"color:#FFFFFF;\"> to snap the Tool to an object. </span>\n<span style=\"color:#FFFFFF;\">Use </span><hl>"Esc"</hl><span style=\"color:#FFFFFF;\"> for tool exist.</span>',
            fst=10000, pos='botLeft', fade=True)

    def uninitializeCallback(self):
        OpenMayaUI.MUiMessage.removeCallback(self.callback)  # remove 3dView Render Callback

        self.qt_Maya_Window.removeEventFilter(self.userKeyboardEvents)  # remove QT Callback
        self.qt_Active_View.removeEventFilter(self.userMouseEvents)  # remove QT Callback

        # OpenMayaUI.M3dView.active3dView().refresh(True, True)
        # OpenMayaUI.M3dView.active3dView().refresh(True, True)
        OpenMayaUI.M3dView.active3dView().scheduleRefresh()

        print("Tool has been uninitialized")

    def getMouseIntersect(self):
        sourcePnt = OpenMaya.MPoint(0, 0, 0)
        rayDir = OpenMaya.MVector(0, 0, 0)
        maximumDistance = 9999999999
        viewHeight = self.view3D.portHeight()
        intersectedPoint = OpenMaya.MFloatPoint()
        hitNormal = OpenMaya.MVector()
        intersectedObject = None

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
            return None, None, None
        else:
            return intersectedPoint, intersectedFace, intersectedObject

    def draw(self, *args):
        pass


'''
Overriden MPxPainter class: Angle Tool
'''


class RullerTool(MPxPainter):
    def __init__(self):
        self.mousePressState = False
        self.hitPoint = None
        self.hitFace = None
        self.hitObject = None
        self.editing = False
        self.closestX = None
        self.closestY = None
        self.closestIndex = None

        '''
        ruler draw data struct(array){
            dagPath
            hitFaceID
            uCoord | vCoord
            hitPoint
        }
        '''
        self.structData = []

        super(RullerTool, self).__init__()

    def drawDistance(self):
        self.glFT.glEnable(OpenMayaRender.MGL_BLEND)
        self.glFT.glBlendFunc(OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA)

        fnMesh = None
        rullerPoints = []

        for i in self.structData:
            fnMesh = OpenMaya.MFnMesh(i[0])

            point = OpenMaya.MPoint(0, 0, 0)

            u = i[2][0]
            v = i[2][1]
            util = OpenMaya.MScriptUtil()
            util.createFromList([u, v], 2)
            uvFloat2Ptr = util.asFloat2Ptr()

            fnMesh.getPointAtUV(i[1], point, uvFloat2Ptr, OpenMaya.MSpace.kWorld)

            rullerPoints.append(point)

        if rullerPoints:
            t = 2
            if self.unit == 1:
                t = 0.03

            self.glFT.glColor4f(1, 0, 0, 1)
            for i in rullerPoints:
                self.glFT.glBegin(OpenMayaRender.MGL_LINES)
                self.glFT.glVertex3f(i.x - t, i.y, i.z)
                self.glFT.glVertex3f(i.x + t, i.y, i.z)
                self.glFT.glVertex3f(i.x, i.y + t, i.z)
                self.glFT.glVertex3f(i.x, i.y - t, i.z)
                self.glFT.glVertex3f(i.x, i.y, i.z + t)
                self.glFT.glVertex3f(i.x, i.y, i.z - t)
                self.glFT.glEnd()

        if len(rullerPoints) > 1:
            for i in range(len(rullerPoints) - 1):
                p1 = rullerPoints[i]
                p2 = rullerPoints[i + 1]

                vector = OpenMaya.MVector(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
                distance = vector.length()
                distanceX = abs(round(float(vector.x) / float(self.unit), 2))
                distanceY = abs(round(float(vector.y) / float(self.unit), 2))
                distanceZ = abs(round(float(vector.z) / float(self.unit), 2))

                if self.unit == 1:
                    distanceX = abs(round(vector.x, 2))
                    distanceY = abs(round(vector.y, 2))
                    distanceZ = abs(round(vector.z, 2))

                direction = vector.normal()
                if self.closestX and self.closestY:
                    if self.closestIndex == 0:
                        if i == self.closestIndex:
                            self.glFT.glColor4f(1, 1, 0, 1)
                            self.glFT.glBegin(OpenMayaRender.MGL_LINES)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)
                            self.glFT.glEnd()
                        else:
                            self.glFT.glColor4f(1, 1, 0, 0.3)
                            self.glFT.glBegin(OpenMayaRender.MGL_LINES)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)
                            self.glFT.glEnd()

                    elif self.closestIndex == len(self.structData) - 1:
                        if i == self.closestIndex - 1:
                            self.glFT.glColor4f(1, 1, 0, 1)
                            self.glFT.glBegin(OpenMayaRender.MGL_LINES)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)
                            self.glFT.glEnd()
                        else:
                            self.glFT.glColor4f(1, 1, 0, 0.3)
                            self.glFT.glBegin(OpenMayaRender.MGL_LINES)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)
                            self.glFT.glEnd()

                    else:
                        if i == self.closestIndex or i == self.closestIndex - 1:
                            self.glFT.glColor4f(1, 1, 0, 1)
                            self.glFT.glBegin(OpenMayaRender.MGL_LINES)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)
                            self.glFT.glEnd()
                        else:
                            self.glFT.glColor4f(1, 1, 0, 0.3)
                            self.glFT.glBegin(OpenMayaRender.MGL_LINES)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)
                            self.glFT.glEnd()

                else:
                    self.glFT.glColor4f(1, 1, 0, 1)
                    self.glFT.glBegin(OpenMayaRender.MGL_LINES)
                    self.glFT.glVertex3f(p1.x, p1.y, p1.z)
                    self.glFT.glVertex3f(p2.x, p2.y, p2.z)
                    self.glFT.glEnd()

                self.glFT.glColor4f(1, 1, 1, 1)
                textX = p1.x + direction.x * distance / 2
                textY = p1.y + direction.y * distance / 2 + 2
                textZ = p1.z + direction.z * distance / 2
                if self.unit == 1.0:
                    textX = p1.x + direction.x * distance / 2
                    textY = p1.y - (p1.y - p2.y) / 2
                    textZ = p1.z + direction.z * distance / 2

                if not self.closestX and not self.closestY:
                    self.view3D.drawText(round(float(distance) / float(self.unit), 2),
                                         OpenMaya.MPoint(textX, textY, textZ), self.view3D.kCenter)
                else:
                    # draw text
                    if self.closestIndex == 0:
                        if i == self.closestIndex:
                            self.glFT.glLineStipple(2, 0x00FF)
                            self.glFT.glEnable(OpenMayaRender.MGL_LINE_STIPPLE)

                            self.glFT.glBegin(OpenMayaRender.MGL_LINES)

                            self.glFT.glColor4f(1, 0, 0, 0.2)
                            self.glFT.glLineWidth(2)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)
                            self.glFT.glVertex3f(p2.x, p2.y, p1.z)
                            self.glFT.glLineWidth(1)
                            self.glFT.glColor4f(1, 0, 0, 0.2)
                            self.glFT.glVertex3f(p2.x, p2.y, p1.z)
                            self.glFT.glVertex3f(p2.x, p1.y, p1.z)
                            self.glFT.glColor4f(1, 0, 0, 1)
                            self.glFT.glVertex3f(p2.x, p1.y, p1.z)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)

                            self.glFT.glLineWidth(2)
                            self.glFT.glColor4f(0, 1, 0, 0.4)
                            self.glFT.glVertex3f(p1.x, p2.y, p2.z)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)
                            self.glFT.glLineWidth(1)
                            self.glFT.glColor4f(0, 1, 0, 0.4)
                            self.glFT.glVertex3f(p1.x, p2.y, p2.z)
                            self.glFT.glVertex3f(p1.x, p2.y, p1.z)
                            self.glFT.glColor4f(0, 1, 0, 1)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)
                            self.glFT.glVertex3f(p1.x, p2.y, p1.z)

                            self.glFT.glColor4f(0.5, 0.5, 1, 0.2)
                            self.glFT.glLineWidth(2)
                            self.glFT.glVertex3f(p2.x, p1.y, p2.z)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)
                            self.glFT.glLineWidth(1)
                            self.glFT.glColor4f(0.5, 0.5, 1, 0.2)
                            self.glFT.glVertex3f(p2.x, p1.y, p2.z)
                            self.glFT.glVertex3f(p1.x, p1.y, p2.z)
                            self.glFT.glColor4f(0.5, 0.5, 1, 1)
                            self.glFT.glVertex3f(p1.x, p1.y, p2.z)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)

                            self.glFT.glEnd()

                            self.glFT.glDisable(OpenMayaRender.MGL_LINE_STIPPLE)

                            self.glFT.glColor4f(0.7, 0, 0, 1)
                            self.view3D.drawText(distanceX, OpenMaya.MPoint(p2.x - (p2.x - p1.x) / 2, p1.y, p1.z),
                                                 self.view3D.kLeft)
                            self.glFT.glColor4f(0, 0.9, 0, 1)
                            self.view3D.drawText(distanceY, OpenMaya.MPoint(p1.x, p2.y - (p2.y - p1.y) / 2, p1.z),
                                                 self.view3D.kLeft)
                            self.glFT.glColor4f(0.5, 0.5, 1.0, 1)
                            self.view3D.drawText(distanceZ, OpenMaya.MPoint(p1.x, p1.y, p2.z - (p2.z - p1.z) / 2),
                                                 self.view3D.kLeft)
                        else:
                            self.view3D.drawText(round(float(distance) / float(self.unit), 2),
                                                 OpenMaya.MPoint(textX, textY, textZ), self.view3D.kCenter)

                    elif self.closestIndex == len(self.structData) - 1:
                        if i == self.closestIndex - 1:
                            self.glFT.glLineStipple(2, 0x00FF)
                            self.glFT.glEnable(OpenMayaRender.MGL_LINE_STIPPLE)

                            self.glFT.glBegin(OpenMayaRender.MGL_LINES)
                            self.glFT.glLineWidth(2)
                            self.glFT.glColor4f(1, 0, 0, 1)
                            self.glFT.glVertex3f(p1.x, p2.y, p2.z)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)
                            self.glFT.glLineWidth(1)
                            self.glFT.glColor4f(1, 0, 0, 0.2)
                            self.glFT.glVertex3f(p1.x, p2.y, p2.z)
                            self.glFT.glVertex3f(p1.x, p2.y, p1.z)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)
                            self.glFT.glVertex3f(p1.x, p2.y, p1.z)

                            self.glFT.glColor4f(0, 1, 0, 1)
                            self.glFT.glLineWidth(2)
                            self.glFT.glVertex3f(p2.x, p1.y, p2.z)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)
                            self.glFT.glLineWidth(1)
                            self.glFT.glColor4f(0, 1, 0, 0.3)
                            self.glFT.glVertex3f(p2.x, p1.y, p2.z)
                            self.glFT.glVertex3f(p1.x, p1.y, p2.z)
                            self.glFT.glVertex3f(p1.x, p1.y, p2.z)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)

                            self.glFT.glColor4f(0.5, 0.5, 1, 1)
                            self.glFT.glLineWidth(2)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)
                            self.glFT.glVertex3f(p2.x, p2.y, p1.z)
                            self.glFT.glLineWidth(1)
                            self.glFT.glColor4f(0.5, 0.5, 1, 0.2)
                            self.glFT.glVertex3f(p2.x, p2.y, p1.z)
                            self.glFT.glVertex3f(p2.x, p1.y, p1.z)
                            self.glFT.glVertex3f(p2.x, p1.y, p1.z)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)
                            self.glFT.glEnd()

                            self.glFT.glDisable(OpenMayaRender.MGL_LINE_STIPPLE)

                            self.glFT.glColor4f(0.7, 0, 0, 1)
                            self.view3D.drawText(distanceX, OpenMaya.MPoint(p2.x - (p2.x - p1.x) / 2, p2.y, p2.z),
                                                 self.view3D.kLeft)
                            self.glFT.glColor4f(0, 0.9, 0, 1)
                            self.view3D.drawText(distanceY, OpenMaya.MPoint(p2.x, p2.y - (p2.y - p1.y) / 2, p2.z),
                                                 self.view3D.kLeft)
                            self.glFT.glColor4f(0.5, 0.5, 1, 1)
                            self.view3D.drawText(distanceZ, OpenMaya.MPoint(p2.x, p2.y, p2.z - (p2.z - p1.z) / 2),
                                                 self.view3D.kLeft)
                        else:
                            self.view3D.drawText(round(float(distance) / float(self.unit), 2),
                                                 OpenMaya.MPoint(textX, textY, textZ), self.view3D.kCenter)

                    else:
                        if i == self.closestIndex:  # or i == self.closestIndex - 1:
                            self.glFT.glLineStipple(2, 0x00FF)
                            self.glFT.glEnable(OpenMayaRender.MGL_LINE_STIPPLE)
                            self.glFT.glBegin(OpenMayaRender.MGL_LINES)

                            self.glFT.glColor4f(0, 1, 0, 0.5)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)
                            self.glFT.glVertex3f(p2.x, p1.y, p2.z)

                            self.glFT.glColor4f(0.5, 0.5, 1, 0.5)
                            self.glFT.glVertex3f(p2.x, p2.y, p1.z)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)

                            self.glFT.glColor4f(1, 0, 0, 0.5)
                            self.glFT.glVertex3f(p1.x, p2.y, p2.z)
                            self.glFT.glVertex3f(p2.x, p2.y, p2.z)

                            self.glFT.glEnd()
                            self.glFT.glDisable(OpenMayaRender.MGL_LINE_STIPPLE)

                            self.glFT.glColor4f(0.7, 0, 0, 1)
                            self.view3D.drawText(distanceX, OpenMaya.MPoint(p2.x - (p2.x - p1.x) / 2, p2.y, p2.z),
                                                 self.view3D.kLeft)
                            self.glFT.glColor4f(0, 0.9, 0, 1)
                            self.view3D.drawText(distanceY, OpenMaya.MPoint(p2.x, p2.y - (p2.y - p1.y) / 2, p2.z),
                                                 self.view3D.kLeft)
                            self.glFT.glColor4f(0.5, 0.5, 1, 1)
                            self.view3D.drawText(distanceZ, OpenMaya.MPoint(p2.x, p2.y, p2.z - (p2.z - p1.z) / 2),
                                                 self.view3D.kLeft)

                        elif i == self.closestIndex - 1:
                            self.glFT.glLineStipple(2, 0x00FF)
                            self.glFT.glEnable(OpenMayaRender.MGL_LINE_STIPPLE)
                            self.glFT.glBegin(OpenMayaRender.MGL_LINES)

                            self.glFT.glColor4f(0, 1, 0, 0.5)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)
                            self.glFT.glVertex3f(p1.x, p2.y, p1.z)

                            self.glFT.glColor4f(0.5, 0.5, 1, 0.5)
                            self.glFT.glVertex3f(p1.x, p1.y, p2.z)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)

                            self.glFT.glColor4f(1, 0, 0, 0.5)
                            self.glFT.glVertex3f(p2.x, p1.y, p1.z)
                            self.glFT.glVertex3f(p1.x, p1.y, p1.z)

                            self.glFT.glEnd()
                            self.glFT.glDisable(OpenMayaRender.MGL_LINE_STIPPLE)

                            self.glFT.glColor4f(0.7, 0, 0, 1)
                            self.view3D.drawText(distanceX, OpenMaya.MPoint(p2.x - (p2.x - p1.x) / 2, p1.y, p1.z),
                                                 self.view3D.kLeft)
                            self.glFT.glColor4f(0, 0.9, 0, 1)
                            self.view3D.drawText(distanceY, OpenMaya.MPoint(p1.x, p2.y - (p2.y - p1.y) / 2, p1.z),
                                                 self.view3D.kLeft)
                            self.glFT.glColor4f(0.5, 0.5, 1, 1)
                            self.view3D.drawText(distanceZ, OpenMaya.MPoint(p1.x, p1.y, p2.z - (p2.z - p1.z) / 2),
                                                 self.view3D.kLeft)
                        else:
                            self.view3D.drawText(round(float(distance) / float(self.unit), 2),
                                                 OpenMaya.MPoint(textX, textY, textZ), self.view3D.kCenter)

        ''' Draw 2D '''
        if self.closestX and self.closestY:
            radius = 15
            xcoord = self.closestX
            ycoord = self.closestY

            # self.view3D.beginGL()
            # self.glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS )
            self.glFT.glPushMatrix()

            # self.glFT.glDrawBuffer( OpenMayaRender.MGL_FRONT )
            self.glFT.glDisable(OpenMayaRender.MGL_DEPTH_TEST)

            # Setup the Orthographic projection Matrix.
            self.glFT.glMatrixMode(OpenMayaRender.MGL_PROJECTION)
            self.glFT.glLoadIdentity()
            self.glFT.glOrtho(0.0, float(self.view3D.portWidth()), 0.0, float(self.view3D.portHeight()), -1.0, 1.0)
            self.glFT.glMatrixMode(OpenMayaRender.MGL_MODELVIEW)
            self.glFT.glLoadIdentity()
            self.glFT.glTranslatef(0.375, 0.375, 0.0)

            self.glFT.glColor4f(1, 1, 1, 0.2)  # 0.2
            self.glFT.glBegin(OpenMayaRender.MGL_TRIANGLE_FAN)
            for i in range(120):  # seg
                x = math.cos(math.radians((360 / 100) * float(i)))
                y = math.sin(math.radians((360 / 100) * float(i)))
                x1 = math.cos(math.radians((360 / 100) * float(i + 1)))
                y1 = math.sin(math.radians((360 / 100) * float(i + 1)))
                self.glFT.glVertex2f(xcoord, ycoord)
                self.glFT.glVertex2f(xcoord + x * radius, ycoord + y * radius)
                self.glFT.glVertex2f(xcoord + x1 * radius, ycoord + y1 * radius)
            self.glFT.glEnd()

            self.glFT.glColor4f(1, 1, 1, 0.6)  # 0.6
            self.glFT.glBegin(OpenMayaRender.MGL_LINES)
            for i in range(120):  # seg
                x = math.cos(math.radians((360 / 100) * float(i)))
                y = math.sin(math.radians((360 / 100) * float(i)))
                x1 = math.cos(math.radians((360 / 100) * float(i + 1)))
                y1 = math.sin(math.radians((360 / 100) * float(i + 1)))
                # self.glFT.glVertex2f(xcoord, ycoord)
                self.glFT.glVertex2f(xcoord + x * radius, ycoord + y * radius)
                self.glFT.glVertex2f(xcoord + x1 * radius, ycoord + y1 * radius)
            self.glFT.glEnd()

            # Restore the state of the matrix from stack
            self.glFT.glMatrixMode(OpenMayaRender.MGL_MODELVIEW)
            self.glFT.glPopMatrix()
            # Restore the previous state of these attributes
            self.glFT.glPopAttrib()
            # self.view3D.endGL()

    def draw(self, *args):
        ''' callback processing '''
        if self.userKeyboardEvents.K_Esc:
            self.uninitializeCallback()
            return

        self.hitObject = None

        if self.userKeyboardEvents.K_Ctrl:
            if self.userMouseEvents.M_Button_Left:
                # get mouse intersection
                self.hitPoint, self.hitFace, self.hitObject = self.getMouseIntersect()

                # check intersected
                if self.hitObject:
                    # get UV at hitPoint
                    dagPath = OpenMaya.MDagPath()
                    selectionList = OpenMaya.MSelectionList()
                    selectionList.clear()
                    selectionList.add(self.hitObject)
                    selectionList.getDagPath(0, dagPath)
                    self.hitObjectDag = dagPath
                    fnMesh = OpenMaya.MFnMesh(dagPath)
                    util = OpenMaya.MScriptUtil()
                    util.createFromList([0.0, 0.0], 2)
                    uvPoint = util.asFloat2Ptr()
                    fnMesh.getUVAtPoint(OpenMaya.MPoint(self.hitPoint.x, self.hitPoint.y, self.hitPoint.z), uvPoint,
                                        OpenMaya.MSpace.kWorld, "map1", None)
                    u = OpenMaya.MScriptUtil.getFloat2ArrayItem(uvPoint, 0, 0)
                    v = OpenMaya.MScriptUtil.getFloat2ArrayItem(uvPoint, 0, 1)

                    # fill up StructData with a New Element
                    uv = []
                    uv.append(u)
                    uv.append(v)
                    data = []
                    data.append(dagPath)
                    data.append(self.hitFace)
                    data.append(uv)
                    data.append(self.hitPoint)

                    if self.editing == False and self.closestIndex == None and not self.userKeyboardEvents.K_Alt:
                        self.structData.append(data)  # we add a new element to StructData

                    elif self.editing == True and self.closestIndex == None and not self.userKeyboardEvents.K_Alt:
                        self.userMouseEvents.editMode = True
                        self.structData[-1] = data  # we assign new values to the last added element

                    elif self.editing == True and (
                            self.closestIndex or self.closestIndex == 0) and not self.userKeyboardEvents.K_Alt:
                        self.userMouseEvents.editMode = True
                        self.structData[self.closestIndex] = data  # we assign new values to the last added element

                    elif self.editing == False and (
                            self.closestIndex or self.closestIndex == 0) and self.userKeyboardEvents.K_Alt:
                        del self.structData[self.closestIndex]

                    self.mousePressState = True
                    self.editing = True

            if not self.userMouseEvents.M_Button_Left and self.mousePressState == True:
                self.mousePressState = False
                self.editing = False  # stop editing, next time we will add a new element
                self.userMouseEvents.editMode = False

            if self.userMouseEvents.M_Move:
                if True:
                    if self.structData:  # if w already have a ruller in the scene
                        # current mouse position
                        viewHeight = self.view3D.portHeight()
                        mouseX = self.userMouseEvents.M_posX
                        mouseY = viewHeight - self.userMouseEvents.M_posY

                        # find closest point position by 2D screen coordinates
                        self.closestX = None
                        self.closestY = None
                        self.closestIndex = None

                        for idx, i in enumerate(self.structData):
                            point = i[3]
                            pointFix = OpenMaya.MPoint(point.x, point.y, point.z)

                            # get point from UV
                            fnMesh = OpenMaya.MFnMesh(i[0])
                            util = OpenMaya.MScriptUtil()
                            util.createFromList([i[2][0], i[2][1]], 2)
                            uvPoint = util.asFloat2Ptr()
                            fnMesh.getPointAtUV(i[1], pointFix, uvPoint, OpenMaya.MSpace.kWorld, "map1", 0.001)

                            xPtrInit = OpenMaya.MScriptUtil()
                            yPtrInit = OpenMaya.MScriptUtil()
                            xPtr = xPtrInit.asShortPtr()
                            yPtr = yPtrInit.asShortPtr()

                            # print pointFix.x, pointFix.y, pointFix.z
                            # print cv2D_XPtr, cv2D_YPtr
                            pointFix2 = OpenMaya.MPoint(float(round(pointFix.x, 2)), float(round(pointFix.y, 2)),
                                                        float(round(pointFix.z, 2)))
                            # pointFix2 = OpenMaya.MPoint(0.0,0.0,0.0)
                            self.view3D.worldToView(pointFix2, xPtr, yPtr)

                            cv2D_X = OpenMaya.MScriptUtil().getShort(xPtr)
                            cv2D_Y = OpenMaya.MScriptUtil().getShort(yPtr)

                            if abs(abs(mouseX) - abs(cv2D_X)) < 15 and abs(abs(mouseY) - abs(cv2D_Y)) < 15:
                                self.closestX = cv2D_X
                                self.closestY = cv2D_Y
                                self.closestIndex = idx
                                break

        else:
            self.closestX = None
            self.closestY = None
            self.closestIndex = None

        if len(self.structData) == 0: return

        '''__OpenGL__'''

        self.glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
        self.view3D.beginGL()

        self.glFT.glClearDepth(0.0)
        self.glFT.glDepthFunc(OpenMayaRender.MGL_ALWAYS)

        self.drawDistance()

        self.view3D.endGL()
        self.glFT.glPopAttrib()


def main():
    # check engine render
    '''
    renderEngine = cmds.optionVar(q='vp2RenderingEngine')
    if renderEngine != "OpenGL":
        cmds.inViewMessage( amg='<hl>Choose OpenGL Legacy in Preferences->Display->RenderingEngine</hl>', pos='botLeft', fade=True )
        return
    '''

    instance = RullerTool()
