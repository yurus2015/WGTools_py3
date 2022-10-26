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


class ToolOptions(QWidget):

    def __init__(self, parent = None):

        super(ToolOptions, self).__init__(parent)


        self.setLayout(self.createUI())

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
                                    """)

        self.mainLayout.addWidget(self.label)

        return self.mainLayout


    # @classmethod
    def main(self):


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
                cmds.setAttr(i + ".displayRotatePivot",0)
                cmds.setAttr(i + ".displayScalePivot",0)


