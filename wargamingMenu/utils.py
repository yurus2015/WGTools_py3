import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaRender as OpenMayaRender


from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

from shiboken2 import wrapInstance

import os
import json
#import main as Main


class Utils(object):

    @classmethod
    def getCurrentDir(cls):
        # Get the place where this .py file is located
        path = str(os.path.dirname(__file__))
        return path

    @classmethod
    def getWindowPointer(cls):
        # Get and return Maya Main window pointer
        main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        qt_Maya_Window = wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

        return qt_Maya_Window

    @classmethod
    def moveMenuPosition(cls, menu):
        main_window = cls.getWindowPointer().objectName()
        array_menu = cmds.window(main_window, q=1, menuArray=1)
        cmds.window(main_window, e=1, menuIndex=[menu.objectName(), len(array_menu)-2])

    @classmethod
    def uiRec(cls, p_parent, menuPtr):
        # Recursively look for the Maya's main QMenuBar
        for child in p_parent.children():
            if child.objectName() == "mainFileMenu":

                menuPtr = child.parent()
                return menuPtr

            menuPtr = cls.uiRec(child, menuPtr)

        return menuPtr

    @classmethod
    def getMenuPanel(cls):
        # Get maya main menu and return the pointer
        mainWindow = cls.getWindowPointer()
        mayaMainMenu_pointer = cls.uiRec(mainWindow, None)

        return mayaMainMenu_pointer

    @classmethod
    def cleanUpMenu(cls, namesList=[]):
        # delete menus from Maya main menu bar by the names from the namesList[]
        menu = cls.getMenuPanel()
        actions = menu.actions()
        for i in actions:
            for j in namesList:
                if i.text() == j:
                    menu.removeAction(i)

    @classmethod
    def readJSON(cls):
        # read JSON data and return it
        currentFolder = cls.getCurrentDir().replace("\\", "\\\\")
        fileRead = open(currentFolder + '\\menu.json', 'r')
        data = json.load(fileRead)

        return data

    @classmethod
    def getMenuPtr(cls, name="Wargaming_3.0"):
        # get wargaming menu pointer
        menu = cls.getMenuPanel()

        actions = menu.actions()
        for i in actions:
            if i.text() == name:
                return i

    @classmethod
    def insertJSONAction(cls, action=None):
        if not action:
            return

        # insert new Action to JSON
        currentFolder = cls.getCurrentDir().replace("\\", "\\\\")
        data = None

        # read current JSON into DICTIONARY
        with open(currentFolder + '\\menu.json', 'r') as f:
            data = json.loads(f.read())

        # DATA for dictionary
        data.append(action)

        # WRITE DATA back to JSON
        with open(currentFolder + '\\menu.json', 'w') as f:
            f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))

    @classmethod
    def getActionFiles(cls):
        # get all actions in directory
        directory = cls.getCurrentDir() + "\\actions"
        file_paths = []
        for root, directories, files in os.walk(directory):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                if "__init__" not in filename and ".pyc" not in filename:
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)  # Add it to the list.

        return file_paths

    @classmethod
    def cleanUpJSON(cls):
        # clear json file
        currentFolder = cls.getCurrentDir().replace("\\", "\\\\")
        jsonFile = open(currentFolder + '\\menu.json', 'w')   # Trying to create a new file
        jsonFile.write("[\n]")
        jsonFile.close()

    @classmethod
    def checkNewItem(cls, actionName=None):
        if not actionName:
            return 0

        actionNameVar = "newAction_" + actionName

        if cmds.optionVar(exists=actionNameVar):
            result = cmds.optionVar(q=actionNameVar)
            if result == 1:
                return 1  # new item
            else:
                return 0  # old item
        else:
            return 1  # option var doesnt exists - its new item

    @classmethod
    def initializeOldActions(cls, option=0):
        cmds.optionVar(iv=('newAction_checkList', option))
        cmds.optionVar(iv=('newAction_textureEditor', option))
        cmds.optionVar(iv=('newAction_uvInfo', option))
        cmds.optionVar(iv=('newAction_validator', option))
        cmds.optionVar(iv=('newAction_bakeMenu', option))
        cmds.optionVar(iv=('newAction_fakeShadow', option))
        cmds.optionVar(iv=('newAction_simplygon', option))
        cmds.optionVar(iv=('newAction_splineTrack', option))
        cmds.optionVar(iv=('newAction_trackSplitTool', option))
        cmds.optionVar(iv=('newAction_caraculGenerator', option))
        cmds.optionVar(iv=('newAction_colliderCreationToolset', option))
        cmds.optionVar(iv=('newAction_colliderMaterial', option))
        cmds.optionVar(iv=('newAction_engineImport', option))
        cmds.optionVar(iv=('newAction_environmentSimplygon', option))
        cmds.optionVar(iv=('newAction_ephu', option))
        cmds.optionVar(iv=('newAction_fullMetalToolset', option))
        cmds.optionVar(iv=('newAction_objectExporter', option))
        cmds.optionVar(iv=('newAction_tankExporter', option))
        cmds.optionVar(iv=('newAction_wgExpolorer', option))
        cmds.optionVar(iv=('newAction_blueprint', option))
        cmds.optionVar(iv=('newAction_blueprintShare', option))
        cmds.optionVar(iv=('newAction_angleTool', option))
        cmds.optionVar(iv=('newAction_ruller', option))
        cmds.optionVar(iv=('newAction_userTest', 1))
