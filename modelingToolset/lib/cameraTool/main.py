import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaRender as OpenMayaRender

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

import os
import os, sys
import math as M

from shiboken2 import wrapInstance

description = "Creates cameras for viewing a tank as like as in a game"
buttonType = "opt"
beautyName = "Camera Tool"
iconName = "Game Camera"

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# get maya window as qt object
main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
qt_maya_window = wrapInstance(long(main_window_ptr), QtCore.QObject)

# get active view port as openmaya object and qt object
active_view = OpenMayaUI.M3dView.active3dView()
active_view_ptr = active_view.widget()
qt_active_view = wrapInstance(long(active_view_ptr), QtCore.QObject)


def getActiveCamera():
    try:
        pan = cmds.getPanel(wf=True)
        cam = cmds.modelPanel(pan, q=True, camera=True)
        return cam
    except:
        return None


class firstCameraContext(QtCore.QObject):
    def __init__(self):
        super(firstCameraContext, self).__init__()

        '''init data'''

        self.start = False
        self.startMousPos = None
        self.prevMousePos = 0

        self.phy = 0
        self.zoomSpeed = 50
        self.rotateXSpeed = 0.5
        self.rotateYSpeed = 1.5
        self.rotX = 0
        self.rotY = 0

        # limits==============================================================
        self.UpDownLimits = [-79, 90]
        # self.UpDownLimits=[-180,180]
        self.theta = self.UpDownLimits[1]
        self.ZoomInOutLimits = [8.3, 11.7]

        self.theta = 0

        '''refresh camera position'''
        self.refreshCameraPos()  # call this to set start pos in start

    def refreshCameraPos(self):
        # print "game first refresh"
        # camX=M.sin(self.theta)*M.cos(self.phy)*self.Radius
        # camY=M.cos(self.theta)*self.Radius
        # camZ=M.sin(self.theta)*M.sin(self.phy)*self.Radius
        # camZ = M.sin(self.phy) * 1

        camRotX = self.theta
        camRotY = self.phy * -1

        camZ = M.cos(self.phy / 57.5) * -2.65
        camX = M.sin(self.phy / 57.5) * 2.5

        cmds.setAttr('|cameraRoof.rotateX', camRotX)  # up Down

        cmds.setAttr('|cameraRoof.rotateY', camRotY)

        cmds.setAttr('|cameraRoof.translateX', camX)
        cmds.setAttr('|cameraRoof.translateZ', camZ)

        # print "UpDown Rotation Angle: ", camRotX , ", Transform Z value: ", camZ

    def eventFilter(self, obj, event):

        camera = getActiveCamera()

        if camera == "cameraRoof":

            if event.type() == QtCore.QEvent.Wheel:
                # self.refreshCameraPos()
                return True
                # delta=event.delta()/abs(event.delta())*self.zoomSpeed
            #     if self.ZoomInOutLimits[0]<self.Radius-delta<self.ZoomInOutLimits[1]:
            #          self.Radius-=delta
            #     else:
            #         if self.Radius-delta < self.ZoomInOutLimits[0]:
            #             self.Radius = self.ZoomInOutLimits[0]
            #         elif  self.Radius-delta > self.ZoomInOutLimits[1]:
            #             self.Radius = self.ZoomInOutLimits[1]
            #     self.refreshCameraPos()
            #     return True  # it have to be True!

            if event.type() == QtCore.QEvent.MouseMove:  # DO MouseToCam PROC
                if self.start:
                    delta = event.pos() - self.startMousPos

                    # theta - up and down
                    if self.UpDownLimits[0] < (self.theta - delta.y() * self.rotateXSpeed) < self.UpDownLimits[1]:
                        self.theta -= delta.y() * self.rotateXSpeed

                    # phy  - left right
                    self.phy += delta.x() * self.rotateYSpeed

                    if (self.phy > 2000 or self.phy < -2000) and (int(self.phy) / 360 - self.phy / 360.0) == 0:
                        self.phy = 0

                    self.refreshCameraPos()
                    self.startMousPos = event.pos()

                return True

            if event.type() == QtCore.QEvent.MouseButtonPress:  # BEGIN MouseToCam PROC
                self.start = True
                self.startMousPos = event.pos()
                self.prevMousePos = event.pos()
                return True

            if event.type() == QtCore.QEvent.MouseButtonRelease:  # END MouseToCam PROC
                self.start = False
                return True

        return event


class gameCameraContext(QtCore.QObject):
    def __init__(self):
        super(gameCameraContext, self).__init__()
        self.startPos = None
        self.movePos = None
        self.endPos = None
        self.start = False
        self.startMousPos = None
        self.direction = None
        self.button = None
        self.initialPosition = OpenMaya.MPoint(0.0, 2.0, 0.0)
        self.phy = 0
        self.zoomSpeed = 50
        self.rotateSpeed = 0.01
        # limits==============================================================
        self.UpDownLimits = [0.0, 1.5]
        self.theta = self.UpDownLimits[1]

        # self.ZoomInOutLimits=[5.5,10]
        self.ZoomInOutLimits = [5.2, 11.2]
        self.Radius = self.ZoomInOutLimits[0] + 2
        # print "initial Radius: ", self.Radius
        # =====================================================================
        self.refreshCameraPos()  # call this to set start pos in start

    def refreshCameraPos(self, stretchZ=1, stretchY=1):

        # translate angles to xzy
        camX = M.sin(self.theta) * M.cos(self.phy) * self.Radius
        camY = M.cos(self.theta) * self.Radius * stretchY
        camZ = M.sin(self.theta) * M.sin(self.phy) * self.Radius

        # move camera
        cmds.setAttr('|cameraGameGrp|cameraGame.translateX', camX)
        cmds.setAttr('|cameraGameGrp|cameraGame.translateY', camY)
        cmds.setAttr('|cameraGameGrp|cameraGame.translateZ', camZ)

    def eventFilter(self, obj, event):
        self.modifier = False

        camera = getActiveCamera()
        if camera == "cameraGame":

            # get camera 3D position and mouse 2D position
            if event.type() == QtCore.QEvent.MouseButtonPress:  # we press mouse button
                self.button = event.button()  # get mouse button id that was pressed
                self.start = True
                self.startMousPos = event.pos()
                return True  # it have to be True!

            if event.type() == QtCore.QEvent.Wheel:  # changes radius

                delta = event.delta() / abs(event.delta()) * self.zoomSpeed  # = -50/50

                # print self.Radius, delta, self.Radius - delta

                # if self.ZoomInOutLimits[0]<self.Radius-delta<self.ZoomInOutLimits[1]:
                #     self.Radius-=delta

                pos = cmds.xform("|cameraGameGrp|cameraGame", q=True, t=True, ws=True)
                print(pos[1], self.Radius, delta)

                if self.ZoomInOutLimits[0] < self.Radius - delta < self.ZoomInOutLimits[1]:
                    pass
                    # if pos[1] > 6 and self.Radius < 5.5 and delta > 0:
                    #     self.Radius-=delta
                else:
                    if self.Radius - delta < self.ZoomInOutLimits[0]:
                        if pos[1] < 10:
                            self.Radius = self.ZoomInOutLimits[0]

                    elif self.Radius - delta > self.ZoomInOutLimits[1]:
                        if pos[1] < 10:
                            self.Radius = self.ZoomInOutLimits[1]

                if self.Radius <= 5.5:
                    self.refreshCameraPos(stretchZ=1.0, stretchY=2.7)
                else:
                    self.refreshCameraPos(stretchZ=1.0, stretchY=1)

                return True  # it have to be True!

            # we move mouse
            if event.type() == QtCore.QEvent.MouseMove:  # if we move mouse
                if self.start:
                    delta = event.pos() - self.startMousPos
                    # define sector to up and down camera------------------
                    if self.UpDownLimits[0] < (self.theta - delta.y() * self.rotateSpeed) < self.UpDownLimits[1]:
                        # calc camera movement up to down
                        self.theta -= delta.y() * self.rotateSpeed

                    # calc camera movement  left to right
                    self.phy += delta.x() * self.rotateSpeed

                    # update camera position
                    pos = cmds.xform("|cameraGameGrp|cameraGame", q=True, t=True, ws=True)

                    # print self.Radius
                    if self.Radius <= 5.5:

                        self.refreshCameraPos(stretchZ=1.0, stretchY=2.7)
                    else:
                        self.refreshCameraPos(stretchZ=1.0, stretchY=1)

                    self.startMousPos = event.pos()
                return True  #

            if event.type() == QtCore.QEvent.MouseButtonRelease:
                self.start = False
                return True

        return event  # it have to be True!


class hangarCameraContext(QtCore.QObject):
    def __init__(self):
        super(hangarCameraContext, self).__init__()
        self.startPos = None
        self.movePos = None
        self.endPos = None
        self.start = False
        self.startMousPos = None
        self.direction = None
        self.button = None
        self.initialPosition = OpenMaya.MPoint(0.0, 2.0, 0.0)
        self.phy = 0
        self.zoomSpeed = 50
        self.rotateSpeed = 0.01
        # limits==============================================================
        self.UpDownLimits = [0.4, 1.5]
        self.theta = self.UpDownLimits[1]

        # self.ZoomInOutLimits=[8.2,20]
        self.ZoomInOutLimits = [8.3, 11.7]
        self.Radius = self.ZoomInOutLimits[0] + 5
        # =====================================================================
        self.refreshCameraPos()  # call this to set start pos in start

    def refreshCameraPos(self, stretchZ=1):
        # translate angles to xzy
        camX = M.sin(self.theta) * M.cos(self.phy) * self.Radius
        camY = M.cos(self.theta) * self.Radius
        camZ = M.sin(self.theta) * M.sin(self.phy) * self.Radius * stretchZ

        # move camera
        cmds.setAttr('cameraHangarGrp|cameraHangar.translateX', camX)
        cmds.setAttr('cameraHangarGrp|cameraHangar.translateY', camY)
        cmds.setAttr('cameraHangarGrp|cameraHangar.translateZ', camZ)

    def eventFilter(self, obj, event):
        self.modifier = False

        camera = getActiveCamera()
        if camera == "cameraHangar":

            # get camera 3D position and mouse 2D position
            if event.type() == QtCore.QEvent.MouseButtonPress:  # we press mouse button
                self.button = event.button()  # get mouse button id that was pressed
                self.start = True
                # pos = cmds.xform("|cameraHangarGrp|cameraHangar", q=True, t=True, ws=True)  #current camera position when we press button
                # self.startPos = OpenMaya.MPoint(round(pos[0], 3), round(pos[1],3), round(pos[2],3)) #put it to MPoint
                self.startMousPos = event.pos()
                return True  # it have to be True!

            if event.type() == QtCore.QEvent.Wheel:  # changes radius
                delta = event.delta() / abs(event.delta()) * self.zoomSpeed

                # if self.ZoomInOutLimits[0]<self.Radius-delta<self.ZoomInOutLimits[1]:
                #     self.Radius-=delta

                if self.ZoomInOutLimits[0] < self.Radius - delta < self.ZoomInOutLimits[1]:
                    self.Radius -= delta
                else:
                    if self.Radius - delta < self.ZoomInOutLimits[0]:
                        self.Radius = self.ZoomInOutLimits[0]
                    elif self.Radius - delta > self.ZoomInOutLimits[1]:
                        self.Radius = self.ZoomInOutLimits[1]
                # print self.Radius, delta, self.Radius - delta

                # print self.Radius
                self.refreshCameraPos()

                return True  # it have to be True!

            # we move mouse
            if event.type() == QtCore.QEvent.MouseMove:  # if we move mouse

                if self.start:
                    delta = event.pos() - self.startMousPos

                    # define sector to up and down camera------------------
                    if self.UpDownLimits[0] < (self.theta - delta.y() * self.rotateSpeed) < self.UpDownLimits[1]:
                        # calc camera movement up to down
                        self.theta -= delta.y() * self.rotateSpeed

                    # calc camera movement  left to right
                    self.phy += delta.x() * self.rotateSpeed

                    # update camera position
                    pos = cmds.xform("|cameraHangarGrp|cameraHangar", q=True, t=True, ws=True)

                    if pos[2] < 0 and self.Radius <= self.ZoomInOutLimits[0] + 0.5:
                        self.refreshCameraPos(stretchZ=1 - 0.07792)
                    else:
                        self.refreshCameraPos(stretchZ=1.0)
                    # self.refreshCameraPos(stretchZ = 1.0)
                    # print self.Radius

                    # set parametr for next mouse delta
                    self.startMousPos = event.pos()
                return True  # it have to be True!

            # we release mouse button - get 3D Camera Pos and 2D Mouse Pos
            if event.type() == QtCore.QEvent.MouseButtonRelease:  # if we released mouse
                self.start = False
                return True  # it have to be True!
            #   endPos = cmds.xform("|cameraHangarGrp|cameraHangar", q=True, t=True, ws=True)
            #   self.endPos = OpenMaya.MPoint(endPos[0], endPos[1], endPos[2])

        return event  # it have to be True!


def start_context(mesh=None):
    # install event filters to get a shift+click menu on the time line

    global minecraft_click_filter

    minecraft_click_filter = hangarCameraContext()  # create camera move event filter

    # remove and install event filters again
    try:
        qt_active_view.removeEventFilter(minecraft_click_filter)
    except:
        pass

    qt_active_view.installEventFilter(minecraft_click_filter)


def start_game_context(mesh=None):
    # install event filters to get a shift+click menu on the time line

    global game_minecraft_click_filter
    # global game_shift_key_filter

    # game_shift_key_filter = ShiftKeyFilter() #create alt_press event filter
    game_minecraft_click_filter = gameCameraContext()  # create camera move event filter

    # remove and install event filters again
    try:
        # qt_maya_window.removeEventFilter(game_shift_key_filter)
        qt_active_view.removeEventFilter(game_minecraft_click_filter)
    except:
        pass
    # qt_maya_window.installEventFilter(game_shift_key_filter)
    qt_active_view.installEventFilter(game_minecraft_click_filter)


def start_firstGame_context(mesh=None):
    global game_first_context_filter

    game_first_context_filter = firstCameraContext()
    try:
        qt_active_view.removeEventFilter(game_first_context_filter)
    except:
        pass
    qt_active_view.installEventFilter(game_first_context_filter)


def end_context():
    try:
        qt_active_view.removeEventFilter(game_minecraft_click_filter)
    except:
        pass

    try:
        qt_active_view.removeEventFilter(game_first_context_filter)
    except:
        pass

    try:
        qt_active_view.removeEventFilter(minecraft_click_filter)
    except:
        pass


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

dir = str(os.path.dirname(__file__))


def getMayaWindow():
    main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)


def comprehensionList(A, B):
    return list(set(A) - set(B))


class ToolOptions(QWidget):

    def __init__(self, parent=None):

        super(ToolOptions, self).__init__(parent)

        """ DATA """
        self.camGroup = None
        self.hangarCameraGrp = None
        self.hangarCameraTransform = None
        self.hangarCameraShape = None
        self.hangarCameraAim = None

        # self.setMinimumWidth(330)
        self.setLayout(self.createUI())

    def createUI(self):

        self.mainLayout = QVBoxLayout()

        """ hangar cam layout """
        self.hangar_layout = QHBoxLayout()
        self.hr_button = QPushButton("Hangar Cam")
        self.hr_button.clicked.connect(self.createHangarCam)
        self.hangar_layout.addWidget(self.hr_button)

        """ game cam layout """
        self.game_layout = QHBoxLayout()
        self.gm_button = QPushButton("Game Cam 3d")
        self.gm_button.clicked.connect(self.createGameCam)
        self.game_layout.addWidget(self.gm_button)

        self.game_layout_f = QHBoxLayout()
        self.gm_button_f = QPushButton("Game Cam 1st")
        self.gm_button_f.clicked.connect(self.createGameCamFirst)
        self.game_layout.addWidget(self.gm_button_f)

        """ clean up """
        self.clean_button = QPushButton("Delete cameras")
        self.clean_button.clicked.connect(self.cleanCameras)

        """ main layout """
        self.mainLayout.addLayout(self.hangar_layout)
        self.mainLayout.addLayout(self.game_layout)
        self.mainLayout.addWidget(self.clean_button)

        return self.mainLayout

    # @classmethod
    def main(self):

        cmds.inViewMessage(amg='<hl>Please open the tool options to select which camera you want to create</hl>',
                           pos='topLeft', fade=True, fot=1000)

    def cleanCameras(self):
        end_context()
        hangar = cmds.ls("cameraHangarGrp", l=1)
        if hangar:
            cmds.delete(hangar[0])

        game = cmds.ls("cameraGameGrp", l=1)
        if game:
            cmds.delete(game[0])

        gameF = cmds.ls("cameraRoof", l=1)
        if gameF:
            cmds.delete(gameF[0])

        allVisPanels = cmds.getPanel(vis=1)
        modelPanelsList = []
        for i in allVisPanels:
            if i.find("model") != -1:
                cmds.lookThru("perspShape", i)
                break

    def findCamera(self, cameraname):
        result = None
        resultShape = None
        result = cmds.ls(cameraname, l=1)
        if result:
            result = result[0]
            resultShape = cmds.listRelatives(result, c=1, f=1)[0]
            return result, resultShape
        else:
            return None, None

    def getBiggestShapeBBox(self, target):
        duplicate = cmds.ls(cmds.duplicate(target), l=1)[0]
        group = cmds.ls(cmds.group(n="temporary", empty=1), l=1)[0]
        target = cmds.ls(cmds.parent(duplicate, group), l=1)

        try:
            separatedObjects = cmds.ls(cmds.polySeparate(target, ch=0), l=1)
        except:
            separatedObjects = target

        biggestPart_BBox = None

        objectList = OpenMaya.MSelectionList()

        for i in separatedObjects:
            objectList.clear()
            objectList.add(i)
            dagpath = OpenMaya.MDagPath()
            objectList.getDagPath(0, dagpath)
            fnDagNode = OpenMaya.MFnDagNode(dagpath)
            bbox = fnDagNode.boundingBox()

            if biggestPart_BBox == None:
                biggestPart_BBox = bbox
            else:
                biggestPart_width = biggestPart_BBox.max().x - biggestPart_BBox.min().x
                biggestPart_height = biggestPart_BBox.max().y - biggestPart_BBox.min().y
                biggestPart_length = biggestPart_BBox.max().z - biggestPart_BBox.min().z

                width = bbox.max().x - bbox.min().x
                height = bbox.max().y - bbox.min().y
                length = bbox.max().z - bbox.min().z

                if width > biggestPart_width and length > biggestPart_length:
                    biggestPart_BBox = bbox

        cmds.delete(group)

        return biggestPart_BBox

    def getTankTwoThirdHeight(self, cameraType=None):
        result = None
        lod0 = cmds.ls("lod0", type="transform", l=1)
        if lod0:

            base = None
            relatives = cmds.listRelatives(lod0[0], type="mesh", f=1, c=1, ad=1)
            for i in relatives:
                if "turret" in i and not "havok" in i:
                    base = cmds.listRelatives(i, f=1, p=1, type="transform")[0]
                    break
            if base == None:
                for i in relatives:
                    if "hull" in i and not "havok" in i:
                        base = cmds.listRelatives(i, f=1, p=1, type="transform")[0]
                        break

            # if no turrent no hull found
            if base == None:
                if cameraType == "Hangar":
                    result = 4
                elif cameraType == "Game":
                    result = 3.5
                else:
                    result = 4

                return

            bbox = self.getBiggestShapeBBox(base)
            heightOneThird = (bbox.max().y - bbox.min().y) / 3

            if cameraType == "Hangar":
                result = bbox.max().y - heightOneThird  # + (bbox.max().y - bbox.min().y) / 4

            elif cameraType == "Game":
                result = bbox.max().y + heightOneThird
            else:
                result = bbox.max().y + heightOneThird

            if result > 20:
                result = round(result / 100, 5)

        return result

    def doFirstPersonCam(self):
        cameraTemp = None

        if not cmds.ls("cameraRoof"):
            print("create a new cameraRoof")
            # create camera
            cameraTemp = cmds.camera(centerOfInterest=5, \
                                     focalLength=26, \
                                     lensSqueezeRatio=1, \
                                     cameraScale=1, \
                                     horizontalFilmAperture=1.4173, \
                                     horizontalFilmOffset=0, \
                                     verticalFilmAperture=0.9449, \
                                     verticalFilmOffset=0, \
                                     filmFit="Fill", \
                                     overscan=1, \
                                     motionBlur=0, \
                                     shutterAngle=144, \
                                     nearClipPlane=0.001, \
                                     farClipPlane=10000, \
                                     orthographic=0, \
                                     orthographicWidth=30, \
                                     panZoomEnabled=1, \
                                     horizontalPan=0, \
                                     verticalPan=0, \
                                     zoom=1)

            # rename
            self.gameCameraTransform = cmds.ls(cameraTemp, l=1)[0]
            cmds.rename(self.gameCameraTransform, "cameraRoof")

            self.gameCameraTransform = cmds.ls("cameraRoof", l=1)[0]
            self.gameCameraShape = cmds.listRelatives(self.gameCameraTransform, c=1, f=1)[0]

            transformY = self.getTankTwoThirdHeight() + 3.5 + 0.929

            cmds.setAttr(self.gameCameraTransform + ".scaleX", 50)
            cmds.setAttr(self.gameCameraTransform + ".scaleY", 50)
            cmds.setAttr(self.gameCameraTransform + ".scaleZ", 50)
            cmds.setAttr(self.gameCameraTransform + ".translateX", 0)
            cmds.setAttr(self.gameCameraTransform + ".translateY", transformY)
            cmds.setAttr(self.gameCameraTransform + ".translateZ", 0)
            # cmds.setAttr(self.gameCameraTransform + ".translateX", lock = 1)
            cmds.setAttr(self.gameCameraTransform + ".translateY", lock=1)
            # cmds.setAttr(self.gameCameraTransform + ".translateZ", lock = 1)
            cmds.transformLimits(self.gameCameraTransform, rx=(-79, 90), erx=(1, 0))

            # cmds.setAttr(self.gameCameraShape + ".focalLength", 21)

            # look through
            allVisPanels = cmds.getPanel(vis=1)
            modelPanelsList = []
            for i in allVisPanels:
                if i.find("model") != -1:
                    cmds.lookThru(self.gameCameraShape, i)
                    break

        else:
            self.gameCameraTransform, self.gameCameraShape = self.findCamera("cameraRoof")

            allVisPanels = cmds.getPanel(vis=1)
            modelPanelsList = []
            for i in allVisPanels:
                if i.find("model") != -1:
                    cmds.lookThru(self.gameCameraShape, i)
                    break

    def doCam(self, cameraType=None):
        cameraTemp = None

        if not cmds.ls("camera" + cameraType):
            print("create a new " + cameraType + " camera")
            # create camera
            cameraTemp = cmds.camera(centerOfInterest=5, \
                                     focalLength=26.686, \
                                     lensSqueezeRatio=1, \
                                     cameraScale=1, \
                                     horizontalFilmAperture=1.4173, \
                                     horizontalFilmOffset=0, \
                                     verticalFilmAperture=0.9449, \
                                     verticalFilmOffset=0, \
                                     filmFit="Fill", \
                                     overscan=1, \
                                     motionBlur=0, \
                                     shutterAngle=144, \
                                     nearClipPlane=0.001, \
                                     farClipPlane=10000, \
                                     orthographic=0, \
                                     orthographicWidth=30, \
                                     panZoomEnabled=1, \
                                     horizontalPan=0, \
                                     verticalPan=0, \
                                     zoom=1)

            mel.eval('objectMoveCommand; cameraMakeNode 2 ""')

            # rename
            self.gameCameraTransform = cmds.ls(cameraTemp, l=1)[0]
            cmds.rename(self.gameCameraTransform, "camera" + cameraType)
            cmds.rename(cmds.listRelatives(cmds.ls("camera" + cameraType, l=1)[0], p=1, f=1),
                        "camera" + cameraType + "Grp")

            # get paths
            self.gameCameraTransform = cmds.ls("camera" + cameraType + "Grp|camera" + cameraType, l=1)[0]
            self.gameCameraShape = cmds.listRelatives(self.gameCameraTransform, c=1, f=1)[0]
            self.gameCameraGrp = cmds.listRelatives(self.gameCameraTransform, p=1, f=1)[0]

            aimObjs = cmds.ls("*aim*", l=1)
            for i in aimObjs:
                if self.gameCameraGrp in i:
                    self.gameCameraAim = i
                    break

            # cmds.setAttr(self.gameCameraGrp + ".visibility", 0)

            # setup camera
            cmds.setAttr(self.gameCameraTransform + ".scaleX", 50)
            cmds.setAttr(self.gameCameraTransform + ".scaleY", 50)
            cmds.setAttr(self.gameCameraTransform + ".scaleZ", 50)

            # # To COMMENT
            # cmds.setAttr(self.gameCameraTransform + ".translateX", 0)
            # cmds.setAttr(self.gameCameraTransform + ".translateY", 4)
            # cmds.setAttr(self.gameCameraTransform + ".translateZ", 5)
            # instead this will call self.refreshCameraPos() with event filter creation

            cameraAimY = self.getTankTwoThirdHeight(cameraType)

            cmds.setAttr(self.gameCameraAim + ".translateX", 0)
            cmds.setAttr(self.gameCameraAim + ".translateY", cameraAimY)
            cmds.setAttr(self.gameCameraAim + ".translateZ", 0)
            cmds.setAttr(self.gameCameraAim + ".translateX", lock=1)
            cmds.setAttr(self.gameCameraAim + ".translateY", lock=1)
            cmds.setAttr(self.gameCameraAim + ".translateZ", lock=1)

            # setup unitConversion TO COMMENT
            unitConversionNode = cmds.listConnections(self.gameCameraGrp + ".distanceBetween")[0]
            cmds.setAttr(unitConversionNode + ".cf", 1)

            # look through
            allVisPanels = cmds.getPanel(vis=1)
            modelPanelsList = []
            for i in allVisPanels:
                if i.find("model") != -1:
                    cmds.lookThru(self.gameCameraShape, i)
                    break

        else:
            self.gameCameraTransform, self.gameCameraShape = self.findCamera("camera" + cameraType)

            allVisPanels = cmds.getPanel(vis=1)
            modelPanelsList = []
            for i in allVisPanels:
                if i.find("model") != -1:
                    cmds.lookThru(self.gameCameraShape, i)
                    break

    def createHangarCam(self):
        if not cmds.ls("cameraHangar"):
            self.doCam("Hangar")
            start_context()
        else:
            self.doCam("Hangar")

    def createGameCam(self):
        if not cmds.ls("cameraGame"):
            self.doCam("Game")
            start_game_context()
        else:
            self.doCam("Game")

    def createGameCamFirst(self):
        # self.doFirstPersonCam()
        if not cmds.ls("cameraRoof"):
            self.doFirstPersonCam()
            start_firstGame_context()
        else:
            self.doFirstPersonCam()
