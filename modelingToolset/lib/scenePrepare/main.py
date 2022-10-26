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

description = "Setups a mesh with correct attributes"
buttonType = "opt"
beautyName = "Mesh Properties"
iconName = "Scene Prepare"

class ToolOptions(QWidget):

    def __init__(self, parent = None):

        super(ToolOptions, self).__init__(parent)


        self.setLayout(self.createUI())
        self.value = 0

    def createUI(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5,5,5,5)
        self.mainLayout.setSpacing(5) #layout
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.label  = QLabel("""
                                    <b>Description:</b>
                                    <p>Prepares scene options</p>
                                    <p>
                                        <b>What it changes:</b>
                                    </p>
                                    <p style='text-decoration: underline;'>
                                        <b>Mesh properties:</b>
                                    </p>
                                    <p style='mragin: 0px; line-height: 5px;'>displayHandle = Off</p>
                                    <p style='mragin: 0px; line-height: 5px;'>doubleSided = On</p>
                                    <p style='mragin: 0px; line-height: 5px;'>backfaceCullin = Off</p>
                                    <p style='mragin: 0px; line-height: 5px;'>displayBorders = On</p>
                                    <p style='mragin: 0px; line-height: 5px;'>vertexNormalMethod = Angle and Area Weighted</p>
                                    <p style='mragin: 0px; line-height: 5px;'>displayRotatePivot = Off</p>
                                    <p style='mragin: 0px; line-height: 5px;'>displayScalePivot = Off</p>
                                    <p style='mragin: 0px; line-height: 5px;'>displayCenter = Off</p>
                                    <p style='mragin: 0px; line-height: 5px;'>displayNormal = Off</p>

                                    <p style='text-decoration: underline;'>
                                        <b>Camera properties</b>
                                    </p>
                                    <p style='mragin: 0px; line-height: 5px;'>Production ready camera options</p>
                                    <p style='text-decoration: underline;'>
                                        <b>Light properties</b>
                                    </p>
                                    <p style='mragin: 0px; line-height: 5px;'>Two Sides Light = Off</p>
                                    <p style='text-decoration: underline;'>
                                        <b>Options</b>
                                    </p>
                                    """)

        self.checkbox = QCheckBox("Unlock normals on all meshes")
        self.checkbox.stateChanged.connect(self.saveState)

        if cmds.optionVar(exists = 'wg_mdltls_utls_unlcknrmls'):
            if cmds.optionVar(q = 'wg_mdltls_utls_unlcknrmls') == 1:
                self.checkbox.setChecked(1)

        self.mainLayout.addWidget(self.label)

        self.mainLayout.addWidget(self.checkbox)

        return self.mainLayout

    def saveState(self):
        if self.checkbox.isChecked():
            # print "check box checked"
            cmds.optionVar(iv=("wg_mdltls_utls_unlcknrmls", 1))
        else:
            # print "check box unchecked"
            cmds.optionVar(iv=("wg_mdltls_utls_unlcknrmls", 0))


    # @classmethod
    def main(self):

        selection = cmds.ls(sl=1, l=1)


        '''fix meshes'''
        meshList = cmds.ls(type="mesh",l=1)
        transformList = cmds.ls(type="transform", l=1)


        if meshList:
            for i in meshList:
                # shapeNode = cmds.listRelatives(i, f=1, c=1, type = "mesh")

                # if not shapeNode:
                #     continue
                # cmds.setAttr(i + ".displayHandle",0)
                cmds.setAttr(i + ".doubleSided",1)
                cmds.setAttr(i + ".backfaceCulling",0)
                cmds.setAttr(i + ".displayBorders",1)
                cmds.setAttr(i + ".vertexNormalMethod",3)
                cmds.setAttr(i + ".displayCenter",0)
                cmds.setAttr(i + ".displayNormal",0)

        if transformList:
            for i in transformList:
                cmds.setAttr(i + ".displayHandle",0)
                cmds.setAttr(i + ".displayScalePivot",0)
                cmds.setAttr(i + ".displayRotatePivot",0)


        #unlock all normals
        if self.checkbox.isChecked():
            print("normals unlocked")
            cmds.select(meshList)
            cmds.polyNormalPerVertex(ufn=1)




        ''' fix camera'''
        cmds.currentUnit(l = "m")
        cmds.setAttr( "persp.translateX", 24)
        cmds.setAttr( "persp.translateY", 18)
        cmds.setAttr( "persp.translateZ", 24)
        cmds.setAttr( "persp.rotateX", -27.938)
        cmds.setAttr( "persp.rotateY", 45)
        cmds.setAttr( "persp.rotateZ", 0)
        cmds.setAttr( "perspShape.tumblePivotX", 0)
        cmds.setAttr( "perspShape.tumblePivotY", 0)
        cmds.setAttr( "perspShape.tumblePivotZ", 0)
        cmds.grid(sp=10, d=10, s=10, da=1, dgl=1, ddl=1, dpl=0, dol=0, dab=1)
        cmds.setAttr( "perspShape.nearClipPlane", 0.05)
        cmds.setAttr( "perspShape.farClipPlane", 10000)
        cmds.setAttr( "topShape.nearClipPlane", 0.05)
        cmds.setAttr( "topShape.farClipPlane", 10000)
        cmds.setAttr( "frontShape.nearClipPlane", 0.05)
        cmds.setAttr( "frontShape.farClipPlane", 10000)
        cmds.setAttr( "sideShape.nearClipPlane", 0.05)
        cmds.setAttr( "sideShape.farClipPlane", 10000)
        cmds.select(cl=1)
        mel.eval('fitPanel -selected;')
        cmds.FrameAll()




        '''fix lighting'''
        panels = cmds.getPanel( typ = 'modelPanel')
        for i in panels:
            cmds.modelEditor(i, e=1, twoSidedLighting = 0)
            cmds.modelEditor(i, e=1, backfaceCulling = 0)

        cmds.inViewMessage(amg= '<hl style="color: #00FF00">Scene has been prepared successfully</hl>' , pos = 'topLeft', fade = True, fot = 1000)


        if not selection:
            cmds.select(d=1)
        else:
            cmds.select(selection)




