import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

from shiboken2 import wrapInstance

import os
import json


class CtxMgr:
    """Safe way to manage group undo chunks using the 'with' command.
    It will close the chunk automatically on exit from the block

    Example:
        with CtxMgr('Create Poly Cubes'):
            cmds.polyCube()
            cmds.polyCube()
        cmds.undo() # Will undo both polyCube() creation calls."""
    openChunk = True

    def __init__(self, name='unnamedOperation'):
        self.name = name
        self.closeChunk = False

    def __enter__(self):
        if CtxMgr.openChunk:
            self.closeChunk = True
            CtxMgr.openChunk = False
            cmds.undoInfo(openChunk=True, chunkName=self.name)
        return None

    def __exit__(self, type, value, traceback):
        if self.closeChunk:
            cmds.undoInfo(closeChunk=True)
            CtxMgr.openChunk = True


def chunk(chunkName):
    """Undo decorator to name and group in a single chunk all commands
    inside the decorated callable."""

    # Decorator functions always take a single argument (usually the
    # decorated function), so we need to use a layered approach so we can
    # also pass in the undo chunk name.
    #
    # The top-level decorator function ("chunk") is only there to pass in
    # the undo chunk name as its single argument.  It returns the actual
    # decorator function ("decorator").  decorator is the function doing
    # the decorating: its single argument is the decorated function, and it
    # returns the wrapper ("wrapper") function, which is used instead of
    # the decorated function.  Where the decorated function would have been
    # called, wrapper is now called instead, and it uses the CtxMgr context
    # to group all undoable commands into a single, named undo chunk.

    def decorator(f):
        def wrapper(*args, **kwargs):
            with CtxMgr(chunkName):
                return f(*args, **kwargs)

        return wrapper

    return decorator


def message(msg=None):
    if not msg:
        return
    cmds.inViewMessage(amg='<hl>' + msg + '</hl>', pos='midCenter', fade=True, fot=1000)


def log(text, *args):
    message = "[MODELING TOOLSET] " + str(text) + " "
    for i in args:
        message += str(i) + " "

    print(message)


def error(text, *args):
    message = "[MODELING TOOLSET ERROR] " + str(text) + " "
    for i in args:
        message += str(i) + " "

    print(message)


def warning(text, *args):
    message = "[MODELING TOOLSET WARNING] " + str(text) + " "
    for i in args:
        message += str(i) + " "

    print(message)


def getCurrentDir():
    # Get the place where this .py file is located
    path = str(os.path.dirname(__file__))
    return path


def getRootDir():
    # get root dir of the project
    currentDir = getCurrentDir()
    root = currentDir[: len(currentDir) - len(currentDir.split("\\")[-1]) - 1]
    return root


def getWindowPointer():
    # Get and return Maya Main window pointer
    main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    qt_Maya_Window = wrapInstance(long(main_window_ptr), QMainWindow)
    return qt_Maya_Window


def read_UI_JSON():
    # read JSON data and return it
    currentFolder = getRootDir().replace("\\", "\\\\")
    jsonPath = currentFolder + '\\\\db.json'

    log("Reading ui.json at ", jsonPath)

    fileRead = open(jsonPath, 'r')
    data = json.load(fileRead)
    fileRead.close()

    return data


def removeList(fromList, thisList):
    resultList = [n for n in fromList if n not in thisList]
    resultList = list(resultList)
    return resultList


def comprehensionList(A, B):
    return list(set(A) - set(B))


def matchLists(A, B):
    return list(set(A) & set(B))
