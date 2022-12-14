import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaRender as OpenMayaRender

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

import sys
import os
import importlib
from .utils import Utils

dir = str(os.path.dirname(__file__))


class WGAction(QAction):

    def __init__(self, parent, titleName, titleText, icon):
        QAction.__init__(self, parent)

        self.setObjectName(titleName)
        self.setText(titleText)
        self.triggered.connect(self.runAction)

        self.icon = icon

        if self.icon:
            iconPath = Utils.getCurrentDir() + "\\res\\small_icons\\" + self.icon
            self.setIcon(QIcon(iconPath))

        self.actionName = titleName

    def runAction(self):
        path = Utils.getCurrentDir() + "\\actions\\" + self.actionName + ".py"
        scriptFile = open(path, 'r')
        scriptIn = scriptFile.read()
        exec(scriptIn)


class WGWidgetAction_NULL(QWidgetAction):
    def __init__(self, parent):
        QWidgetAction.__init__(self, parent)

        self.label = QWidget()
        self.label.setMinimumHeight(1)
        self.label.setMaximumHeight(1)
        self.label.resize(1, 1)
        self.label.setStyleSheet("Height: 1px; Width: 1px;")

        self.setDefaultWidget(self.label)
        self.setObjectName("topSeparatorWidget_wgMenu")


class WGWidgetAction_StdUI(QWidget):
    def __init__(self, parent, title, name, icon, newItemCheckResilt, options):
        QWidget.__init__(self)

        self.titleText = title
        self.icon = icon
        self.newItemCheck = newItemCheckResilt
        self.options = options

        self.setObjectName(name)
        self.setMinimumSize(200, 22)
        self.setMaximumSize(200, 22)

        self.setLayout(self.createUI())

    def createUI(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignLeft)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        '''icon'''
        self.iconContainer = QWidget()
        self.iconContainer.setStyleSheet("background-color: rgb(64,64,64);")

        self.iconLayout = QVBoxLayout()
        self.iconLayout.setAlignment(Qt.AlignTop)
        self.iconLayout.setContentsMargins(0, 0, 0, 0)
        self.iconLayout.setSpacing(0)

        self.iconContainer.setLayout(self.iconLayout)

        self.iconLabel = QLabel("")
        self.iconLabel.setMinimumSize(19, 22)
        self.iconLabel.setMaximumSize(19, 22)
        self.iconLabel.setGeometry(0, 0, 19, 22)
        self.iconLabel.setPixmap(QPixmap(Utils.getCurrentDir() + "\\res\\small_icons\\" + str(self.icon)).scaled(16, 16,
                                                                                                                 Qt.KeepAspectRatio,
                                                                                                                 Qt.SmoothTransformation))
        self.iconLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.iconLayout.addWidget(self.iconLabel)

        '''text'''
        self.textWrapper = QWidget()

        self.textLayout = QHBoxLayout()
        self.textLayout.setAlignment(Qt.AlignTop)
        self.textLayout.setContentsMargins(0, 0, 0, 0)
        self.textLayout.setSpacing(0)

        self.textWrapper.setLayout(self.textLayout)

        self.textLabel = QLabel(self.titleText)
        self.textLabel.setMinimumSize(180, 22)
        self.textLabel.setMaximumSize(180, 22)
        self.textLabel.setStyleSheet("color: rgb(230,230,230); padding-left: 14px;")

        if self.newItemCheck == 0:
            # its old item
            self.textWrapper.setStyleSheet("background-color: rgb(82,82,82);")
            self.textLabel.setStyleSheet("color: rgb(230,230,230); padding-left: 14px;")

        if self.newItemCheck == 1:
            # its new item
            self.textWrapper.setStyleSheet(
                "background-color: rgb(82,82,82); background-image: url(" + Utils.getCurrentDir().replace("\\",
                                                                                                          "/") + "/res/small_icons/newItemBG.png)")
            self.textLabel.setStyleSheet("color: #66ff33; padding-left: 14px;")

        self.textLayout.addWidget(self.textLabel)

        self.optionsLayout = QVBoxLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)
        self.optionsLayout.setContentsMargins(0, 0, 0, 0)
        self.optionsLayout.setSpacing(0)

        if self.options:
            self.button_options = OptionButton(self.options)
            self.optionsLayout.addWidget(self.button_options)

        '''main layout'''
        self.mainLayout.addWidget(self.iconContainer)
        self.mainLayout.addWidget(self.textWrapper)
        self.mainLayout.addLayout(self.optionsLayout)
        return self.mainLayout

    def makeBGOld(self):
        self.newItemCheck = 0
        self.textWrapper.setStyleSheet("")
        self.textWrapper.setStyleSheet("background-color: rgb(82,82,82);")

    def enterEvent(self, event):
        if self.newItemCheck == 0:
            # its old item
            self.textWrapper.setStyleSheet("background-color: #5285a6;")
            self.textLabel.setStyleSheet("color: rgb(230,230,230); padding-left: 14px;")

        if self.newItemCheck == 1:
            # its new item
            self.textWrapper.setStyleSheet(
                "background-color: #5285a6; background-image: url(" + Utils.getCurrentDir().replace("\\",
                                                                                                    "/") + "/res/small_icons/newItemBG.png);")
            self.textLabel.setStyleSheet("color: #66ff33; padding-left: 14px;")

    def leaveEvent(self, event):
        if self.newItemCheck == 0:
            self.textWrapper.setStyleSheet("background-color: rgb(82,82,82);")
            self.textLabel.setStyleSheet("color: rgb(230,230,230); padding-left: 14px;")
            if self.options:
                self.button_options.setStyleSheet("background-color: rgb(82,82,82); border: none;")

        if self.newItemCheck == 1:
            # its new item
            self.textWrapper.setStyleSheet(
                "background-color: rgb(82,82,82); background-image: url(" + Utils.getCurrentDir().replace("\\",
                                                                                                          "/") + "/res/small_icons/newItemBG.png);")
            self.textLabel.setStyleSheet("color: #66ff33; padding-left: 14px;")


class OptionButton(QPushButton):

    def __init__(self, action=None):
        QPushButton.__init__(self)
        self.action = action
        print('Options_Action', self.action)
        icon = QPixmap(Utils.getCurrentDir() + "\\res\\option.svg").scaled(11, 11, Qt.KeepAspectRatio,
                                                                           Qt.SmoothTransformation)
        self.setIcon(icon)
        self.setMinimumSize(19, 22)
        self.setMaximumSize(19, 22)
        self.setGeometry(0, 0, 19, 22)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setStyleSheet("background-color: rgb(82,82,82); border: none;")

        self.clicked.connect(self.buttonClick)

    def enterEvent(self, event):
        self.setStyleSheet("background-color: #5285a6;")

    def leaveEvent(self, event):
        self.setStyleSheet("background-color: rgb(82,82,82); border: none;")

    def buttonClick(self):
        OPTION_PATH = 'wargamingMenu.options.'
        exec('import ' + OPTION_PATH + self.action + '.main')
        print('Action', OPTION_PATH + self.action + '.main.main()')

        self.returnUI = eval(OPTION_PATH + self.action + '.main.main()')


class WGWidgetAction(QWidgetAction):
    def __init__(self, parent, titleName, titleText, icon, actionType="standart", newItemCheck=False, options=None):
        QWidgetAction.__init__(self, parent)

        self.titleText = titleText
        self.actionName = titleName
        self.icon = icon
        self.setObjectName(titleName)
        self.parentMenu = parent
        self.options = options

        self.setText(self.titleText)
        if self.icon:
            _iconPath = Utils.getCurrentDir() + "\\res\\small_icons\\" + self.icon
            self.setIcon(QIcon(_iconPath))

        if actionType == "standart":
            if not newItemCheck:
                # for extra menu items that doesn't have to be checked
                self.mainWidget = WGWidgetAction_StdUI(self, title=titleText, name=titleName + "wgtUI", icon=self.icon,
                                                       newItemCheckResilt=0, options=self.options)
                self.setDefaultWidget(self.mainWidget)
                self.triggered.connect(self.runAction)
            else:
                # check for standart items in menu
                result = Utils.checkNewItem(
                    self.actionName)  # 1 - if its new item - green it, 0 = it was clicked and not new - do not green it

                self.mainWidget = WGWidgetAction_StdUI(self, title=titleText, name=titleName + "wgtUI", icon=self.icon,
                                                       newItemCheckResilt=result, options=self.options)
                self.setDefaultWidget(self.mainWidget)
                self.triggered.connect(self.runAction)

    def runAction(self):
        # update New Item - to Old Item
        cmds.optionVar(iv=('newAction_' + self.actionName, 0))
        # change CSS
        self.mainWidget.makeBGOld()

        path = Utils.getCurrentDir() + "\\actions\\" + self.actionName + ".py"
        # path_2 = importlib.import_module(CHECKS_PATH + self.action + '.fix')
        print('action! ', path)

        scriptFile = open(path, 'r')
        scriptIn = scriptFile.read()
        scriptFile.close()

        modifiers = QApplication.keyboardModifiers()
        if modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            actionCommand = self.getAction()
            actionCommand = actionCommand.replace("\'", "\"")
            actionName = self.getActionName()
            actionIcon = self.getIcon()

            if actionIcon:
                actionIcon = Utils.getCurrentDir() + "\\res\\small_icons\\" + str(actionIcon)
            else:
                actionIcon = 'commandButton.xpm'

            currentShelf = mel.eval("string $currentShelf = `tabLayout -q -st $gShelfTopLevel`;")
            currentShelfContent = cmds.shelfLayout(currentShelf, q=1, childArray=1)

            cmds.shelfButton(parent=currentShelf,
                             scaleIcon=1,
                             annotation=actionName,
                             i=actionIcon,
                             c=actionCommand,
                             style="iconAndTextHorizontal",
                             sourceType="python",
                             width=20,
                             height=20)

            self.parentMenu.setVisible(1)
            return False

        else:
            exec(scriptIn)

    def getAction(self):
        path = Utils.getCurrentDir() + "\\actions\\" + self.actionName + ".py"

        scriptFile = open(path, 'r')
        scriptIn = scriptFile.read()
        scriptFile.close()

        return scriptIn

    def getActionName(self):
        return self.actionName

    def getIcon(self):
        return self.icon


class SubMenu(QMenu):

    def __init__(self, label="Default SubMenu"):
        QMenu.__init__(self)
        self.setObjectName(label.replace(" ", "") + "_objName")
        self.setTitle("   " + label)


class WargamingMenu(QMenu):

    def __init__(self, parent):
        QMenu.__init__(self, parent)
        '''Menu structure'''
        # get all action files in "action" folder
        self.fileList = Utils.getActionFiles()

        # read menu.json data - returns dictionary
        self.jsonData = Utils.readJSON()

        # update menu.json
        self.updateMenuJSON()

        # read menu.json data AGAIN with updated data
        self.jsonData = Utils.readJSON()

        # crate menu based on menu.json data
        self.createMenuActions()

    def updateMenuJSON(self):
        # if there are new actions - update JSON that is used for the menu
        if not self.fileList:
            return

        for i in self.fileList:
            # get file content
            actionLabel = None
            actionCategory = None
            actionIcon = None
            actionName = i.split("\\")[-1].split(".")[0]  # ephu

            with open(i) as runActionFile:
                for line in runActionFile:
                    if "action_label" in line:
                        actionLabel = line.split("=")[-1].strip().replace("\"", "")
                    elif "action_category" in line:
                        actionCategory = line.split("=")[-1].strip().replace("\"", "")
                    elif "action_icon" in line:
                        actionIcon = line.split("=")[-1].strip().replace("\"", "")

            if not actionLabel: continue

            # update json
            isUnique = True
            for menuItem in self.jsonData:
                if menuItem["action_label"] == actionLabel:
                    isUnique = False

            # if an action has a new name - it means its a brand new action - insert it into the JSON file
            if isUnique:
                newMenuAction = ({"action_label": actionLabel,
                                  "action_category": actionCategory,
                                  "action_name": actionName,
                                  "action_icon": actionIcon})

                Utils.insertJSONAction(action=newMenuAction)

    def createMenuActions(self):
        print('Iam')
        # core predefined priority
        categoryPriority = ["Main Tools", "Tank Tools", "Objects", "Animation", "TechArt Tools", "Historical Tools",
                            "Options"]

        # now we can see top separator
        topWidgetFix = WGWidgetAction_NULL(self)
        self.addAction(topWidgetFix)

        # Main Categories
        for i in categoryPriority:
            if i != "Options":
                separator = self.addSeparator()
                separator.setText(i)

            subMenus = []
            for action in self.jsonData:
                actionLabel = action["action_label"]
                actionName = action["action_name"]
                actionCategory = action["action_category"]
                actionIcon = action["action_icon"]
                actionOptions = action["action_options"]

                print('Options', actionOptions)

                if actionCategory == i and actionCategory != "Options":
                    # newAction = WGWidgetAction(parent = self, titleName= actionName, titleText= actionLabel, icon = actionIcon, newItemCheck = True)
                    # self.addAction(newAction)
                    '''Adding SubMenu'''

                    if "/" in actionLabel:
                        subM = actionLabel.split("/")[0]
                        subM_actionLabel = actionLabel[len(subM) + 1:]

                        # find this menu
                        foundSubMenu = None
                        for m in subMenus:
                            if m.title() == "   " + subM:
                                foundSubMenu = m

                        if foundSubMenu:
                            newAction = WGWidgetAction(parent=self, titleName=actionName, titleText=subM_actionLabel,
                                                       icon=actionIcon, newItemCheck=True, options=actionOptions)
                            foundSubMenu.addAction(newAction)
                        else:
                            # create new Menu
                            newMenu = SubMenu(subM)
                            self.addMenu(newMenu)
                            subMenus.append(newMenu)

                            newAction = WGWidgetAction(parent=self, titleName=actionName, titleText=subM_actionLabel,
                                                       icon=actionIcon, newItemCheck=True, options=actionOptions)
                            newMenu.addAction(newAction)

                    else:
                        newAction = WGWidgetAction(parent=self, titleName=actionName, titleText=actionLabel,
                                                   icon=actionIcon, newItemCheck=True, options=actionOptions)
                        self.addAction(newAction)

        # Other Categories
        separatorCustom = self.addSeparator()
        separatorCustom.setText("User Custom Tools")

        subMenus = []

        for action in self.jsonData:
            actionLabel = action["action_label"]
            actionName = action["action_name"]
            actionCategory = action["action_category"]
            actionIcon = action["action_icon"]
            actionOptions = action["action_options"]

            if actionCategory == None or actionCategory not in categoryPriority:
                # newAction = WGWidgetAction(parent = self, titleName= actionName, titleText= actionLabel, icon = actionIcon, newItemCheck = True)
                # self.addAction(newAction)
                '''Adding SubMenu'''

                if "/" in actionLabel:
                    subM = actionLabel.split("/")[0]
                    subM_actionLabel = actionLabel[len(subM) + 1:]

                    # find this menu
                    foundSubMenu = None
                    for m in subMenus:
                        if m.title() == "   " + subM:
                            foundSubMenu = m

                    if foundSubMenu:
                        newAction = WGWidgetAction(parent=self, titleName=actionName, titleText=subM_actionLabel,
                                                   icon=actionIcon, newItemCheck=True, options=actionOptions)
                        foundSubMenu.addAction(newAction)
                    else:
                        # create new Menu
                        newMenu = SubMenu(subM)
                        self.addMenu(newMenu)
                        subMenus.append(newMenu)

                        newAction = WGWidgetAction(parent=self, titleName=actionName, titleText=subM_actionLabel,
                                                   icon=actionIcon, newItemCheck=True, options=actionOptions)
                        newMenu.addAction(newAction)
                else:
                    newAction = WGWidgetAction(parent=self, titleName=actionName, titleText=actionLabel,
                                               icon=actionIcon, newItemCheck=True, options=actionOptions)
                    self.addAction(newAction)

                ''''''
        separatorCustom = self.addSeparator()
        separatorCustom.setText(" ")

        # Options
        for action in self.jsonData:
            actionLabel = action["action_label"]
            actionName = action["action_name"]
            actionCategory = action["action_category"]
            actionOptions = action["action_options"]
            # actionIcon = action["action_icon"]
            if actionCategory == "Options":
                newAction = WGWidgetAction(parent=self, titleName=actionName, titleText=actionLabel, icon=None,
                                           newItemCheck=False, options=actionOptions)
                self.addAction(newAction)

    def mouseReleaseEvent(self, event):
        # get pressde action
        action = self.activeAction()

        # Add to shelf
        modifiers = QApplication.keyboardModifiers()

        if modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            actionCommand = action.getAction()
            actionCommand = actionCommand.replace("\'", "\"")
            actionName = action.getActionName()
            actionIcon = action.getIcon()

            if actionIcon:
                actionIcon = Utils.getCurrentDir() + "\\res\\small_icons\\" + str(actionIcon)
            else:
                actionIcon = 'commandButton.xpm'

            currentShelf = mel.eval("string $currentShelf = `tabLayout -q -st $gShelfTopLevel`;")
            currentShelfContent = cmds.shelfLayout(currentShelf, q=1, childArray=1)

            cmds.shelfButton(parent=currentShelf,
                             scaleIcon=1,
                             annotation=actionName,
                             i=actionIcon,
                             c=actionCommand,
                             style="iconAndTextHorizontal",
                             sourceType="python",
                             width=20,
                             height=20)

            return False

        # Run the action
        if action and action.isEnabled():
            action.trigger()
            self.setVisible(0)

        # Default
        return False


def updateCMenuJSON(fileList, jsonData):
    # if there are new actions - update JSON that is used for the menu
    if not fileList:
        return

    for i in fileList:
        # get file content
        actionLabel = None
        actionCategory = None
        actionIcon = None
        actionName = i.split("\\")[-1].split(".")[0]  # ephu
        actionOptions = None

        with open(i) as runActionFile:
            for line in runActionFile:
                if "action_label" in line:
                    actionLabel = line.split("=")[-1].strip().replace("\"", "")
                elif "action_category" in line:
                    actionCategory = line.split("=")[-1].strip().replace("\"", "")
                elif "action_icon" in line:
                    actionIcon = line.split("=")[-1].strip().replace("\"", "")

        if not actionLabel:
            continue

        # update json
        isUnique = True
        for menuItem in jsonData:
            if menuItem["action_label"] == actionLabel:
                isUnique = False

        # if an action has a new name - it means its a brand new action - insert it into the JSON file
        if isUnique:
            newMenuAction = ({"action_label": actionLabel,
                              "action_category": actionCategory,
                              "action_name": actionName,
                              "action_icon": actionIcon})

            Utils.insertJSONAction(action=newMenuAction)


def createCMenu(menuBar, menuName):
    menu = QMenu(menuBar)
    menu.setTearOffEnabled(True)
    menu.setWindowTitle(menuName)
    menu.setTitle(menuName)
    menu.setObjectName("wargamingMenu")
    menu.setGeometry(50, 50, 280, 150)
    menuBar.addAction(menu.menuAction())

    fileList = Utils.getActionFiles()
    jsonData = Utils.readJSON()

    updateCMenuJSON(fileList, jsonData)
    jsonData = Utils.readJSON()

    print('####-------------####', jsonData)

    '''_______________________________________'''

    # core predefined priority
    categoryPriority = ["Main Tools", "Tank Tools", "Objects", "Animation", "TechArt Tools", "Historical Tools",
                        "Options"]

    # now we can see top separator
    topWidgetFix = WGWidgetAction_NULL(menu)
    menu.addAction(topWidgetFix)

    # Main Categories
    for i in categoryPriority:
        if i != "Options":
            separator = menu.addSeparator()
            separator.setText(i)

        subMenus = []

        for action in jsonData:
            actionLabel = action["action_label"]
            actionName = action["action_name"]
            actionCategory = action["action_category"]
            actionIcon = action["action_icon"]
            actionOptions = None
            try:
                actionOptions = action["action_options"]
                print('Options', actionOptions)
            except:
                pass

            if actionCategory == i and actionCategory != "Options":
                # newAction = WGWidgetAction(parent = self, titleName= actionName, titleText= actionLabel, icon = actionIcon, newItemCheck = True)
                # self.addAction(newAction)
                '''Adding SubMenu'''

                if "/" in actionLabel:
                    subM = actionLabel.split("/")[0]
                    subM_actionLabel = actionLabel[len(subM) + 1:]

                    # find this menu
                    foundSubMenu = None
                    for m in subMenus:
                        if m.title() == "   " + subM:
                            foundSubMenu = m

                    if foundSubMenu:
                        newAction = WGWidgetAction(parent=menu, titleName=actionName, titleText=subM_actionLabel,
                                                   icon=actionIcon, newItemCheck=True, options=actionOptions)
                        foundSubMenu.addAction(newAction)
                    else:
                        # create new Menu
                        newMenu = SubMenu(subM)
                        menu.addMenu(newMenu)
                        subMenus.append(newMenu)

                        newAction = WGWidgetAction(parent=menu, titleName=actionName, titleText=subM_actionLabel,
                                                   icon=actionIcon, newItemCheck=True, options=actionOptions)
                        newMenu.addAction(newAction)
                else:
                    newAction = WGWidgetAction(parent=menu, titleName=actionName, titleText=actionLabel,
                                               icon=actionIcon, newItemCheck=True, options=actionOptions)
                    menu.addAction(newAction)

    return menu
