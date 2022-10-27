import maya.cmds as cmds
import maya.mel
from maya.mel import eval as meval
import getpass
import re
import os
import time
import subprocess
import datetime
import sys

# import createCirclePNG
# import sys
# maya2018 pyside2
try:
    from PySide import QtGui, QtCore
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    from PySide2 import QtGui, QtCore, QtWidgets
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *


def username():
    name = getpass.getuser()
    # if (name == "i_kiknavelidze"):
    if not name == "Yurus":
        cmds.confirmDialog(title='User', message='User is not valid', button=['OK'], defaultButton='Yes')
        raise ValueError()


def checkValidData():
    reg_data = datetime.date(2017, 12, 0o1)
    now_date = datetime.date.today()
    delta = reg_data - now_date  # return in format: -1 day, 0:00:00
    delta_str = str(delta)
    days = delta_str.split(' ', 1)

    if int(days[0]) <= 0:
        cmds.confirmDialog(title='Date', message='Date expiried', button=['OK'], defaultButton='Yes')
        raise ValueError()


def hardEdgesInUV(shapes):
    print('HARD')
    value = 0
    for shape in shapes:
        edges = cmds.ls(shape + '.e[*]', fl=True)
        for e in edges:
            hardStr = cmds.polyInfo(e, ev=True)
            if 'Hard' in hardStr:
                value = 1
                break

    return value


def photoshopPathReturn():
    # checkValidData()
    photoshopPath = ''
    cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if 'Photoshop' in line:
            photoshopPath = line.split('"')
            print(photoshopPath)
            if 'Photoshop' in photoshopPath[0]:
                break

            else:
                photoshopPath = ''
    # time.sleep(2)
    # proc.kill()
    os.popen('TASKKILL /PID ' + str(proc.pid) + ' /F')
    if photoshopPath:
        return photoshopPath[1]
    else:
        cmds.confirmDialog(title='Photoshop ERROR', message='Photoshop Not Running', button=['I undestand'],
                           defaultButton='Yes')


def subprocessExecute(javaFile):
    ps_path = photoshopPathReturn()
    subprocess.call([ps_path, javaFile])
    time.sleep(2)


def javascriptNormalSurface(pathColor):
    # checkValidData()
    # username()

    nameColor = pathColor.split('/', -1)
    print('OPS', nameColor)
    pathColor = pathColor.replace('/', '\\\\')

    fileExt = '.jsx'
    tmpJVXPath = (pathColor + fileExt)
    # tmp_a_JVXPath = (pathColor + '_a' + fileExt)
    f = open(tmpJVXPath, "w")
    lines_jvx = ['var doc = activeDocument;\n',
                 'var file = new File("' + pathColor + '.tga");\n',
                 'var docRef = app.open (file);\n',
                 'backFile= app.activeDocument;\n',
                 'backFile.selection.selectAll();\n',
                 'backFile.selection.copy();\n',
                 'backFile.close(SaveOptions.DONOTSAVECHANGES);\n',

                 'var idslct = charIDToTypeID( "slct" );\n',
                 'var desc16 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'var ref6 = new ActionReference();\n',
                 'var idLyr = charIDToTypeID( "Lyr " );\n',
                 'var idOrdn = charIDToTypeID( "Ordn" );\n',
                 'var idTrgt = charIDToTypeID( "Trgt" );\n',
                 'ref6.putEnumerated( idLyr, idOrdn, idTrgt );\n',
                 'desc16.putReference( idnull, ref6 );\n',
                 'var idMkVs = charIDToTypeID( "MkVs" );\n',
                 'desc16.putBoolean( idMkVs, false );\n',
                 'executeAction( idslct, desc16, DialogModes.NO );\n',
                 'doc.selection.deselect();\n',
                 'doc.paste();\n',
                 'app.activeDocument.activeLayer.name = "SURFACE_NM";\n']
    # 'var al = doc.activeLayer;\n',
    # 'doc.al.name = "' +nameColor[-1] +'";\n']

    f.writelines(lines_jvx)
    f.close()

    correctPath = tmpJVXPath.replace('\\\\', '\\')
    subprocessExecute(correctPath)


# os.remove(correctPath)

def javascriptNormalGeometry(pathColor):
    # username()
    # user = username()
    # if not user:
    # cmds.confirmDialog( title='Error', message='50 Dollars!', button=['I undestand'], defaultButton='Yes' )
    # raise ValueError()
    nameColor = pathColor.split('/', -1)
    print('OPS', nameColor)
    pathColor = pathColor.replace('/', '\\\\')

    fileExt = '.jsx'
    tmpJVXPath = (pathColor + fileExt)
    f = open(tmpJVXPath, "w")
    lines_jvx = ['var doc = activeDocument;\n',
                 'var file = new File("' + pathColor + '.tga");\n',
                 'var docRef = app.open (file);\n',
                 'backFile= app.activeDocument;\n',
                 'backFile.selection.selectAll();\n',
                 'backFile.selection.copy();\n',
                 'backFile.close(SaveOptions.DONOTSAVECHANGES);\n',

                 'var idslct = charIDToTypeID( "slct" );\n',
                 'var desc16 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'var ref6 = new ActionReference();\n',
                 'var idLyr = charIDToTypeID( "Lyr " );\n',
                 'var idOrdn = charIDToTypeID( "Ordn" );\n',
                 'var idTrgt = charIDToTypeID( "Trgt" );\n',
                 'ref6.putEnumerated( idLyr, idOrdn, idTrgt );\n',
                 'desc16.putReference( idnull, ref6 );\n',
                 'var idMkVs = charIDToTypeID( "MkVs" );\n',
                 'desc16.putBoolean( idMkVs, false );\n',
                 'executeAction( idslct, desc16, DialogModes.NO );\n',
                 'doc.selection.deselect();\n',
                 'doc.paste();\n',
                 'app.activeDocument.activeLayer.name = "GEOMETRY_NM";\n']
    # 'var al = doc.activeLayer;\n',
    # 'doc.al.name = "' +nameColor[-1] +'";\n']

    f.writelines(lines_jvx)
    f.close()

    correctPath = tmpJVXPath.replace('\\\\', '\\')
    subprocessExecute(correctPath)


# os.remove(correctPath)

def javascriptAlpha(pathAlpha, expand):
    # username()
    # user = username()
    # if not user:
    # cmds.confirmDialog( title='Error', message='50 Dollars!', button=['I undestand'], defaultButton='Yes' )
    # raise ValueError()
    pathAlpha = pathAlpha.replace('/', '\\\\')
    fileExt = '.jsx'
    tmpJVXPath = (pathAlpha + '_a' + fileExt)
    f = open(tmpJVXPath, "w")
    lines_jvx = ['var docRef = app.activeDocument;\n',
                 'docRef.selection.selectAll();\n',
                 'var idPlc = charIDToTypeID( "Plc " );\n',
                 'var desc328 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'desc328.putPath( idnull, new File( "' + pathAlpha + '.png" ) );\n',
                 'var idFTcs = charIDToTypeID( "FTcs" );\n',
                 'var idQCSt = charIDToTypeID( "QCSt" );\n',
                 'var idQcsa = charIDToTypeID( "Qcsa" );\n',
                 'desc328.putEnumerated( idFTcs, idQCSt, idQcsa );\n',
                 'var idOfst = charIDToTypeID( "Ofst" );\n',
                 'var desc329 = new ActionDescriptor();\n',
                 'var idHrzn = charIDToTypeID( "Hrzn" );\n',
                 'var idPxl = charIDToTypeID( "#Pxl" );\n',
                 'desc329.putUnitDouble( idHrzn, idPxl, 0.000000 );\n',
                 'var idVrtc = charIDToTypeID( "Vrtc" );\n',
                 'var idPxl = charIDToTypeID( "#Pxl" );\n',
                 'desc329.putUnitDouble( idVrtc, idPxl, 0.000000 );\n',
                 'var idOfst = charIDToTypeID( "Ofst" );\n',
                 'desc328.putObject( idOfst, idOfst, desc329 );\n',
                 'executeAction( idPlc, desc328, DialogModes.NO );\n',
                 'var idsetd = charIDToTypeID( "setd" );\n',
                 'var desc330 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'var ref258 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idfsel = charIDToTypeID( "fsel" );\n',
                 'ref258.putProperty( idChnl, idfsel );\n',
                 'desc330.putReference( idnull, ref258 );\n',
                 'var idT = charIDToTypeID( "T   " );\n',
                 'var ref259 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idTrsp = charIDToTypeID( "Trsp" );\n',
                 'ref259.putEnumerated( idChnl, idChnl, idTrsp );\n',
                 'desc330.putReference( idT, ref259 );\n',
                 'executeAction( idsetd, desc330, DialogModes.NO );\n',
                 'var idDlt = charIDToTypeID( "Dlt " );\n',
                 'var desc331 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'var ref260 = new ActionReference();\n',
                 'var idLyr = charIDToTypeID( "Lyr " );\n',
                 'var idOrdn = charIDToTypeID( "Ordn" );\n',
                 'var idTrgt = charIDToTypeID( "Trgt" );\n',
                 'ref260.putEnumerated( idLyr, idOrdn, idTrgt );\n',
                 'desc331.putReference( idnull, ref260 );\n',
                 'executeAction( idDlt, desc331, DialogModes.NO );\n',

                 'docRef.selection.expand( ' + expand + ' );\n',

                 'var idMk = charIDToTypeID( "Mk  " );\n',
                 'var desc24 = new ActionDescriptor();\n',
                 'var idNw = charIDToTypeID( "Nw  " );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'desc24.putClass( idNw, idChnl );\n',
                 'var idAt = charIDToTypeID( "At  " );\n',
                 'var ref14 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idMsk = charIDToTypeID( "Msk " );\n',
                 'ref14.putEnumerated( idChnl, idChnl, idMsk );\n',
                 'desc24.putReference( idAt, ref14 );\n',
                 'var idUsng = charIDToTypeID( "Usng" );\n',
                 'var idUsrM = charIDToTypeID( "UsrM" );\n',
                 'var idRvlS = charIDToTypeID( "RvlS" );\n',
                 'desc24.putEnumerated( idUsng, idUsrM, idRvlS );\n',
                 'executeAction( idMk, desc24, DialogModes.NO );\n']

    f.writelines(lines_jvx)
    f.close()
    correctPath = tmpJVXPath.replace('\\\\', '\\')
    print('I DO ALPHA! ', correctPath)
    subprocessExecute(correctPath)


# os.remove(correctPath)


def javascriptHardAlpha(pathAlpha):
    # username()

    pathAlpha = pathAlpha.replace('/', '\\\\')
    fileExt = '.jsx'
    tmpJVXPath = (pathAlpha + fileExt)
    f = open(tmpJVXPath, "w")
    lines_jvx = ['var docRef = app.activeDocument;\n',
                 'docRef.selection.selectAll();\n',
                 'var idPlc = charIDToTypeID( "Plc " );\n',
                 'var desc328 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'desc328.putPath( idnull, new File( "' + pathAlpha + '.png" ) );\n',
                 'var idFTcs = charIDToTypeID( "FTcs" );\n',
                 'var idQCSt = charIDToTypeID( "QCSt" );\n',
                 'var idQcsa = charIDToTypeID( "Qcsa" );\n',
                 'desc328.putEnumerated( idFTcs, idQCSt, idQcsa );\n',
                 'var idOfst = charIDToTypeID( "Ofst" );\n',
                 'var desc329 = new ActionDescriptor();\n',
                 'var idHrzn = charIDToTypeID( "Hrzn" );\n',
                 'var idPxl = charIDToTypeID( "#Pxl" );\n',
                 'desc329.putUnitDouble( idHrzn, idPxl, 0.000000 );\n',
                 'var idVrtc = charIDToTypeID( "Vrtc" );\n',
                 'var idPxl = charIDToTypeID( "#Pxl" );\n',
                 'desc329.putUnitDouble( idVrtc, idPxl, 0.000000 );\n',
                 'var idOfst = charIDToTypeID( "Ofst" );\n',
                 'desc328.putObject( idOfst, idOfst, desc329 );\n',
                 'executeAction( idPlc, desc328, DialogModes.NO );\n',
                 'var idsetd = charIDToTypeID( "setd" );\n',
                 'var desc330 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'var ref258 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idfsel = charIDToTypeID( "fsel" );\n',
                 'ref258.putProperty( idChnl, idfsel );\n',
                 'desc330.putReference( idnull, ref258 );\n',
                 'var idT = charIDToTypeID( "T   " );\n',
                 'var ref259 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idTrsp = charIDToTypeID( "Trsp" );\n',
                 'ref259.putEnumerated( idChnl, idChnl, idTrsp );\n',
                 'desc330.putReference( idT, ref259 );\n',
                 'executeAction( idsetd, desc330, DialogModes.NO );\n',
                 'var idDlt = charIDToTypeID( "Dlt " );\n',
                 'var desc331 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'var ref260 = new ActionReference();\n',
                 'var idLyr = charIDToTypeID( "Lyr " );\n',
                 'var idOrdn = charIDToTypeID( "Ordn" );\n',
                 'var idTrgt = charIDToTypeID( "Trgt" );\n',
                 'ref260.putEnumerated( idLyr, idOrdn, idTrgt );\n',
                 'desc331.putReference( idnull, ref260 );\n',
                 'executeAction( idDlt, desc331, DialogModes.NO );\n',

                 # 'docRef.selection.expand( 1 );\n',

                 'var idMk = charIDToTypeID( "Mk  " );\n',
                 'var desc24 = new ActionDescriptor();\n',
                 'var idNw = charIDToTypeID( "Nw  " );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'desc24.putClass( idNw, idChnl );\n',
                 'var idAt = charIDToTypeID( "At  " );\n',
                 'var ref14 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idMsk = charIDToTypeID( "Msk " );\n',
                 'ref14.putEnumerated( idChnl, idChnl, idMsk );\n',
                 'desc24.putReference( idAt, ref14 );\n',
                 'var idUsng = charIDToTypeID( "Usng" );\n',
                 'var idUsrM = charIDToTypeID( "UsrM" );\n',
                 'var idRvlS = charIDToTypeID( "RvlS" );\n',
                 'desc24.putEnumerated( idUsng, idUsrM, idRvlS );\n',
                 'executeAction( idMk, desc24, DialogModes.NO );\n'

                 # add FX

                 'var idrefineSelectionEdge = stringIDToTypeID( "refineSelectionEdge" );\n',
                 'var desc101 = new ActionDescriptor();\n',
                 'var idrefineEdgeBorderRadius = stringIDToTypeID( "refineEdgeBorderRadius" );\n',
                 'var idPxl = charIDToTypeID( "#Pxl" );\n',
                 'desc101.putUnitDouble( idrefineEdgeBorderRadius, idPxl, 0.000000 );\n',
                 'var idrefineEdgeBorderContrast = stringIDToTypeID( "refineEdgeBorderContrast" );\n',
                 'var idPrc = charIDToTypeID( "#Prc" );\n',
                 'desc101.putUnitDouble( idrefineEdgeBorderContrast, idPrc, 0.000000 );\n',
                 'var idrefineEdgeSmooth = stringIDToTypeID( "refineEdgeSmooth" );\n',
                 'desc101.putInteger( idrefineEdgeSmooth, 0 );\n',
                 'var idrefineEdgeFeatherRadius = stringIDToTypeID( "refineEdgeFeatherRadius" );\n',
                 'var idPxl = charIDToTypeID( "#Pxl" );\n',
                 'desc101.putUnitDouble( idrefineEdgeFeatherRadius, idPxl, 2.000000 );\n',
                 'var idrefineEdgeChoke = stringIDToTypeID( "refineEdgeChoke" );\n',
                 'var idPrc = charIDToTypeID( "#Prc" );\n',
                 'desc101.putUnitDouble( idrefineEdgeChoke, idPrc, 45.000000 );\n',
                 'var idrefineEdgeAutoRadius = stringIDToTypeID( "refineEdgeAutoRadius" );\n',
                 'desc101.putBoolean( idrefineEdgeAutoRadius, false );\n',
                 'var idrefineEdgeDecontaminate = stringIDToTypeID( "refineEdgeDecontaminate" );\n',
                 'desc101.putBoolean( idrefineEdgeDecontaminate, false );\n',
                 'var idrefineEdgeOutput = stringIDToTypeID( "refineEdgeOutput" );\n',
                 'var idrefineEdgeOutput = stringIDToTypeID( "refineEdgeOutput" );\n',
                 'var idrefineEdgeOutputUserMask = stringIDToTypeID( "refineEdgeOutputUserMask" );\n',
                 'desc101.putEnumerated( idrefineEdgeOutput, idrefineEdgeOutput, idrefineEdgeOutputUserMask );\n',
                 'executeAction( idrefineSelectionEdge, desc101, DialogModes.NO );\n',

                 'var idShw = charIDToTypeID( "Shw " );\n',
                 'var desc102 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'var list40 = new ActionList();\n',
                 'var ref94 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idOrdn = charIDToTypeID( "Ordn" );\n',
                 'var idTrgt = charIDToTypeID( "Trgt" );\n',
                 'ref94.putEnumerated( idChnl, idOrdn, idTrgt );\n',
                 'list40.putReference( ref94 );\n',
                 'desc102.putList( idnull, list40 );\n',
                 'executeAction( idShw, desc102, DialogModes.NO );\n',

                 'var idHd = charIDToTypeID( "Hd  " );\n',
                 'var desc103 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'var list41 = new ActionList();\n',
                 'var ref95 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idRd = charIDToTypeID( "Rd  " );\n',
                 'ref95.putEnumerated( idChnl, idChnl, idRd );\n',
                 'list41.putReference( ref95 );\n',
                 'var ref96 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idGrn = charIDToTypeID( "Grn " );\n',
                 'ref96.putEnumerated( idChnl, idChnl, idGrn );\n',
                 'list41.putReference( ref96 );\n',
                 'var ref97 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idBl = charIDToTypeID( "Bl  " );\n',
                 'ref97.putEnumerated( idChnl, idChnl, idBl );\n',
                 'list41.putReference( ref97 );\n',
                 'desc103.putList( idnull, list41 );\n',
                 'executeAction( idHd, desc103, DialogModes.NO );\n',

                 'var idLvls = charIDToTypeID( "Lvls" );\n',
                 'var desc104 = new ActionDescriptor();\n',
                 'var idpresetKind = stringIDToTypeID( "presetKind" );\n',
                 'var idpresetKindType = stringIDToTypeID( "presetKindType" );\n',
                 'var idpresetKindCustom = stringIDToTypeID( "presetKindCustom" );\n',
                 'desc104.putEnumerated( idpresetKind, idpresetKindType, idpresetKindCustom );\n',
                 'var idAdjs = charIDToTypeID( "Adjs" );\n',
                 'var list42 = new ActionList();\n',
                 'var desc105 = new ActionDescriptor();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var ref98 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idOrdn = charIDToTypeID( "Ordn" );\n',
                 'var idTrgt = charIDToTypeID( "Trgt" );\n',
                 'ref98.putEnumerated( idChnl, idOrdn, idTrgt );\n',
                 'desc105.putReference( idChnl, ref98 );\n',
                 'var idInpt = charIDToTypeID( "Inpt" );\n',
                 'var list43 = new ActionList();\n',
                 'list43.putInteger( 0 );\n',
                 'list43.putInteger( 141 );\n',
                 'desc105.putList( idInpt, list43 );\n',
                 'var idGmm = charIDToTypeID( "Gmm " );\n',
                 'desc105.putDouble( idGmm, 1.370000 );\n',
                 'var idLvlA = charIDToTypeID( "LvlA" );\n',
                 'list42.putObject( idLvlA, desc105 );\n',
                 'desc104.putList( idAdjs, list42 );\n',
                 'executeAction( idLvls, desc104, DialogModes.NO );\n',

                 'var idShw = charIDToTypeID( "Shw " );\n',
                 'var desc106 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'var list44 = new ActionList();\n',
                 'var ref99 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idRd = charIDToTypeID( "Rd  " );\n',
                 'ref99.putEnumerated( idChnl, idChnl, idRd );\n',
                 'list44.putReference( ref99 );\n',
                 'var ref100 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idGrn = charIDToTypeID( "Grn " );\n',
                 'ref100.putEnumerated( idChnl, idChnl, idGrn );\n',
                 'list44.putReference( ref100 );\n',
                 'var ref101 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idBl = charIDToTypeID( "Bl  " );\n',
                 'ref101.putEnumerated( idChnl, idChnl, idBl );\n',
                 'list44.putReference( ref101 );\n',
                 'desc106.putList( idnull, list44 );\n',
                 'executeAction( idShw, desc106, DialogModes.NO );\n',

                 'var idHd = charIDToTypeID( "Hd  " );\n',
                 'var desc107 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'var list45 = new ActionList();\n',
                 'var ref102 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idOrdn = charIDToTypeID( "Ordn" );\n',
                 'var idTrgt = charIDToTypeID( "Trgt" );\n',
                 'ref102.putEnumerated( idChnl, idOrdn, idTrgt );\n',
                 'list45.putReference( ref102 );\n',
                 'desc107.putList( idnull, list45 );\n',
                 'executeAction( idHd, desc107, DialogModes.NO );\n']
    f.writelines(lines_jvx)
    f.close()
    correctPath = tmpJVXPath.replace('\\\\', '\\')
    subprocessExecute(correctPath)


def javascriptColorMask(pathAlpha):
    # username()
    pathAlpha = pathAlpha.replace('/', '\\\\')
    fileExt = '.jsx'
    tmpJVXPath = (pathAlpha + '_c' + fileExt)
    f = open(tmpJVXPath, "w")
    lines_jvx = ['var docRef = app.activeDocument;\n',
                 'docRef.selection.selectAll();\n',
                 'var idPlc = charIDToTypeID( "Plc " );\n',
                 'var desc3 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'desc3.putPath( idnull, new File( "' + pathAlpha + '.tga" ) );\n',
                 'var idFTcs = charIDToTypeID( "FTcs" );\n',
                 'var idQCSt = charIDToTypeID( "QCSt" );\n',
                 'var idQcsa = charIDToTypeID( "Qcsa" );\n',
                 'desc3.putEnumerated( idFTcs, idQCSt, idQcsa );\n',
                 'var idOfst = charIDToTypeID( "Ofst" );\n',
                 'var desc4 = new ActionDescriptor();\n',
                 'var idHrzn = charIDToTypeID( "Hrzn" );\n',
                 'var idPxl = charIDToTypeID( "#Pxl" );\n',
                 'desc4.putUnitDouble( idHrzn, idPxl, 0.000000 );\n',
                 'var idVrtc = charIDToTypeID( "Vrtc" );\n',
                 'var idPxl = charIDToTypeID( "#Pxl" );\n',
                 'desc4.putUnitDouble( idVrtc, idPxl, 0.000000 );\n',
                 'var idOfst = charIDToTypeID( "Ofst" );\n',
                 'desc3.putObject( idOfst, idOfst, desc4 );\n',
                 'executeAction( idPlc, desc3, DialogModes.NO );\n',

                 'var idShw = charIDToTypeID( "Shw " );\n',
                 'var desc202 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'var list49 = new ActionList();\n',
                 'var ref179 = new ActionReference();\n',
                 'var idLyr = charIDToTypeID( "Lyr " );\n',
                 'var idOrdn = charIDToTypeID( "Ordn" );\n',
                 'var idTrgt = charIDToTypeID( "Trgt" );\n',
                 'ref179.putEnumerated( idLyr, idOrdn, idTrgt );\n',
                 'list49.putReference( ref179 );\n',
                 'desc202.putList( idnull, list49 );\n',
                 'var idTglO = charIDToTypeID( "TglO" );\n',
                 'desc202.putBoolean( idTglO, true );\n',
                 'executeAction( idShw, desc202, DialogModes.NO );\n',

                 'var idsetd = charIDToTypeID( "setd" );\n',
                 'var desc5 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'var ref2 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idfsel = charIDToTypeID( "fsel" );\n',
                 'ref2.putProperty( idChnl, idfsel );\n',
                 'desc5.putReference( idnull, ref2 );\n',
                 'var idT = charIDToTypeID( "T   " );\n',
                 'var ref3 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idRd = charIDToTypeID( "Rd  " );\n',
                 'ref3.putEnumerated( idChnl, idChnl, idRd );\n',
                 'desc5.putReference( idT, ref3 );\n',
                 'executeAction( idsetd, desc5, DialogModes.NO );\n',

                 'var idShw = charIDToTypeID( "Shw " );\n',
                 'var desc204 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'var list50 = new ActionList();\n',
                 'var ref182 = new ActionReference();\n',
                 'var idLyr = charIDToTypeID( "Lyr " );\n',
                 'var idOrdn = charIDToTypeID( "Ordn" );\n',
                 'var idTrgt = charIDToTypeID( "Trgt" );\n',
                 'ref182.putEnumerated( idLyr, idOrdn, idTrgt );\n',
                 'list50.putReference( ref182 );\n',
                 'desc204.putList( idnull, list50 );\n',
                 'var idTglO = charIDToTypeID( "TglO" );\n',
                 'desc204.putBoolean( idTglO, true );\n',
                 'executeAction( idShw, desc204, DialogModes.NO );\n',

                 'var idDlt = charIDToTypeID( "Dlt " );\n',
                 'var desc6 = new ActionDescriptor();\n',
                 'var idnull = charIDToTypeID( "null" );\n',
                 'var ref4 = new ActionReference();\n',
                 'var idLyr = charIDToTypeID( "Lyr " );\n',
                 'var idOrdn = charIDToTypeID( "Ordn" );\n',
                 'var idTrgt = charIDToTypeID( "Trgt" );\n',
                 'ref4.putEnumerated( idLyr, idOrdn, idTrgt );\n',
                 'desc6.putReference( idnull, ref4 );\n',
                 'executeAction( idDlt, desc6, DialogModes.NO );\n',

                 # 'docRef.selection.expand( '+ expand +' );\n',

                 'var idMk = charIDToTypeID( "Mk  " );\n',
                 'var desc7 = new ActionDescriptor();\n',
                 'var idNw = charIDToTypeID( "Nw  " );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'desc7.putClass( idNw, idChnl );\n',
                 'var idAt = charIDToTypeID( "At  " );\n',
                 'var ref5 = new ActionReference();\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idChnl = charIDToTypeID( "Chnl" );\n',
                 'var idMsk = charIDToTypeID( "Msk " );\n',
                 'ref5.putEnumerated( idChnl, idChnl, idMsk );\n',
                 'desc7.putReference( idAt, ref5 );\n',
                 'var idUsng = charIDToTypeID( "Usng" );\n',
                 'var idUsrM = charIDToTypeID( "UsrM" );\n',
                 'var idRvlS = charIDToTypeID( "RvlS" );\n',
                 'desc7.putEnumerated( idUsng, idUsrM, idRvlS );\n',
                 'executeAction( idMk, desc7, DialogModes.NO );\n']

    f.writelines(lines_jvx)
    f.close()
    correctPath = tmpJVXPath.replace('\\\\', '\\')
    subprocessExecute(correctPath)


def writeMultiBakeFile(executeCmd):
    tmpDir = cmds.internalVar(userTmpDir=True)
    fileExt = 'bakerlist.bcm'
    fileExt = tmpDir + fileExt
    print('FILE PATH', fileExt)


def javascriptLinkingNormal(linkFile):
    fileExt = '.jsx'
    linkFile = linkFile.replace('/', '\\\\')
    tmpJVXPath = (linkFile + fileExt)
    f = open(tmpJVXPath, "w")
    # lines_jvx = ['var doc = app.activeDocument;\n',
    # 'var layerId = Stdlib.getLayerID(doc, doc.activeLayer);\n',
    # 'activeDocument.layers[layerId].link(activeDocument.layers[layerId+1]);']
    lines_jvx = ['activeDocument.layers[0].link(activeDocument.layers[1]);']
    f.writelines(lines_jvx)
    f.close()

    correctPath = tmpJVXPath.replace('\\\\', '\\')
    print('I DO IT! ', correctPath)
    subprocessExecute(correctPath)


def load_plugins():
    currentVersion = cmds.about(v=1)
    if '2014' in currentVersion:

        if not cmds.pluginInfo('techartAPI2014', query=True, l=True):
            try:
                cmds.loadPlugin('techartAPI2014')
            except:
                raise MissingPluginError('Unable to load techartAPI2014.mll!')

    if '2015' in currentVersion:

        if not cmds.pluginInfo('techartAPI2015', query=True, l=True):
            try:
                cmds.loadPlugin('techartAPI2015')
            except:
                raise MissingPluginError('Unable to load techartAPI2015.mll!')

    if "2016 Extension 2" in currentVersion:
        try:
            cmds.loadPlugin('techartAPI2016ext2')
        except:
            print('Don`t load plugin')


def mapToHard():
    load_plugins()
    objList = cmds.ls(sl=1, o=1)
    for o in objList:
        cmds.select(o)
        cmds.polyNormalPerVertex(ufn=1)
        cmds.polySoftEdge(o, a=180, ch=0)
        cmds.select(o)
        try:
            mapBorders = meval('selectUVBorderEdge -he')
        except:
            mapBorders = meval('selectUVBorderEdge')
        cmds.polySoftEdge(mapBorders, a=0, ch=1)
    cmds.select(objList)


def hardEdgeSelect():
    load_plugins()
    mapBorders = []
    if cmds.filterExpand(sm=12):
        try:
            mapBorders = meval('selectUVBorderEdge -he')
        except:
            mapBorders = meval('selectUVBorderEdge')
        cmds.select(mapBorders)
    else:
        cmds.confirmDialog(title='Selection ERROR', message='Select mesh', button=['I undestand'], defaultButton='Yes')
        cmds.error('Dont select any mesh')


def borderEdgeToHard():
    cmds.polySelectConstraint(disable=1)
    cmds.polySelectConstraint(m=0)
    cmds.polySelectConstraint(w=0, t=0x0010)
    objList = cmds.ls(sl=1, o=1)
    for ol in objList:
        finalBorder = list()
        cmds.select(ol)
        cmds.polyNormalPerVertex(ufn=1)
        cmds.polySoftEdge(ol, a=180, ch=1)
        cmds.select(ol + '.map[*]', r=1)
        meval('polySelectBorderShell 1')

        uvBorder = cmds.polyListComponentConversion(te=1, internal=1)
        uvBorder = cmds.ls(uvBorder, fl=1)
        for edg in uvBorder:
            print('EDGE ', edg)
            uvEdge = cmds.polyListComponentConversion(edg, tuv=1)
            uvEdge = cmds.ls(uvEdge, fl=1)
            cmds.select(uvEdge[0])
            meval('polySelectBorderShell 1')
            uvShell = cmds.ls(sl=1, fl=1)
            if len(uvEdge) > 2:

                if len(list(set(uvShell) & set(uvEdge))) != len(uvEdge):
                    finalBorder.append(edg)

        if finalBorder:
            cmds.polySoftEdge(finalBorder, a=0, ch=1)

    cmds.select(objList)


###################################
def gatherGUIValue_main():
    tris = meval('checkBoxGrp -q -value1 triangulate_CB')
    preview = meval('checkBoxGrp -q -v1 preview_CB')
    angle = meval('checkBoxGrp -q -value1 angleArea_CB')
    width = meval('optionMenuGrp -q -sl bakerWidthNormalMenu')
    height = meval('optionMenuGrp -q -sl bakerHightNormalMenu')
    surface = meval('checkBoxGrp -q -v1 alphaSurfaceCB')
    surfaceAlpha = meval('optionMenuGrp -q -sl surfaceAlphaMask')
    geometry = meval('checkBoxGrp -q -v1 alphaGeometryCB')
    geometryAlpha = meval('optionMenuGrp -q -sl geometryAlphaMask')


def cleanUP():
    meval('polyCleanupArgList 3 { "0","2","1","0","0","0","0","0","0","1e-005","0","1e-005","0","1e-006","0","1","0" }')
    bagselect = cmds.ls(sl=True)
    if bagselect:
        cmds.confirmDialog(title='Error', message='Non-manifold geometry. Operation canceled', button=['I undestand'],
                           defaultButton='Yes')
        raise ValueError()


def bevelingEdges(ob):
    bevel_nodes = list()
    cmds.select(ob)
    # if typ == 2:
    cmds.polySelectConstraint(m=3, t=0x8000, sm=1, w=2)  # to get hard edges
    edges_hs = cmds.ls(sl=True, fl=True)
    if not edges_hs:
        cmds.polySelectConstraint(sm=0)  # turn off edge smoothness constraint
        cmds.polySelectConstraint(m=0)
        cmds.polySelectConstraint(w=0, t=0x0010)
        cmds.confirmDialog(title='Error', message='Has not edges current type', button=['I undestand'],
                           defaultButton='Yes')
        cmds.select(ob)
    # raise ValueError()
    angle = 0

    while edges_hs:
        # if typ == 2:
        cmds.polySelectConstraint(m=3, t=0x8000, sm=1, w=2)  # to get hard edges
        angle = 180

        edges_hs = cmds.ls(sl=True, fl=True)
        cmds.polySelectConstraint(dis=0)
        edges = edges_hs[0:1000]  # old
        # edges = edges_hs

        if edges:
            bevel_node = cmds.polyBevel(edges, o=0, sg=2, smoothingAngle=angle)
            version = meval('getApplicationVersionAsFloat()')
            if version > 2014.0:
                cmds.setAttr((bevel_node[0] + '.useLegacyBevelAlgorithm'), 1)
            bevel_nodes.append(bevel_node)
    cmds.selectMode(component=True)
    cmds.polySelectConstraint(sm=0)  # turn off edge smoothness constraint
    cmds.polySelectConstraint(m=0)
    cmds.polySelectConstraint(w=0, t=0x0010)

    return bevel_nodes


def mayaQtSnapshot(width, height, path):
    print("NEW SNAPSHOT\n")
    objects = cmds.filterExpand(ex=True, sm=12)
    if objects:
        cmds.select(objects)
        cmds.polySelectConstraint(m=3, t=0x8000, sm=1, w=2)  # to get hard edges
        edges_hs = cmds.ls(sl=True, fl=True)
        cmds.polySelectConstraint(dis=0)
        cmds.selectMode(component=True)
        cmds.polySelectConstraint(dis=0)
        cmds.polySelectConstraint(sm=0)  # turn off edge smoothness constraint
        cmds.polySelectConstraint(m=0)
        cmds.polySelectConstraint(w=0, t=0x0010)
        cmds.select(objects)
    if not edges_hs:
        cmds.confirmDialog(title='Error', message='Has not edges current type', button=['I undestand'],
                           defaultButton='Yes')
    if edges_hs:
        # createCirclePNG.main(path, width, edges_hs)
        snapshot_main(path, width, edges_hs)


def mayaShop_snapshot(width, height, path):
    # username()

    objects = cmds.filterExpand(ex=True, sm=12)
    faces = cmds.filterExpand(ex=True, sm=34)
    edges = cmds.filterExpand(ex=True, sm=32)
    uv = cmds.filterExpand(ex=True, sm=35)
    print('OBJECTS ', objects)

    if objects:
        cleanUP()
        all_bevel = list()
        # bevels_nodes = range(len(objects))
        for index in range(len(objects)):
            object_bevel = bevelingEdges(objects[index])
            all_bevel.extend(object_bevel)

        cmds.select(objects)
        cmds.selectType(pf=True)

        cmds.polySelectConstraint(m=3, t=8, ga=True, gab=(0.0, 0.000))

        cmds.uvSnapshot(o=True, n=(path + '.png'), ff='png', aa=True, xr=width, yr=height)

        cmds.polySelectConstraint(ga=False)
        cmds.polySelectConstraint(m=0)
        cmds.polySelectConstraint(w=0, t=0x0010)

        for bevel in all_bevel:
            cmds.delete(bevel)
        cmds.select(objects)
    if faces:
        cmds.uvSnapshot(o=True, n=(path + 'hard_alpha.png'), ff='png', aa=True, xr=width, yr=height)
        cmds.select(faces)
    if edges:
        cleanUP()

        bevel_node = cmds.polyBevel(edges, o=0, sg=2)
        cmds.selectType(pf=True)
        cmds.polySelectConstraint(m=3, t=8, ga=True, gab=(0, 0))
        cmds.polySelectConstraint(m=0)
        cmds.polySelectConstraint(w=0, t=0x0010)
        cmds.uvSnapshot(o=True, n=(path + 'hard_alpha.png'), ff='png', aa=True, xr=width, yr=height)

        cmds.delete(bevel_node)
        cmds.select(edges)
    if uv:
        # cmds.select(uv)
        cmds.polySelectConstraint(m=2, sh=True)  # to get shell uv
        shell = cmds.ls(sl=True)
        print('Shell ', shell)
        cmds.polySelectConstraint(m=0, sh=False)
        cmds.polySelectConstraint(w=0, t=0x0010)  #

        fc = cmds.polyListComponentConversion(tf=True)
        cmds.select(fc)
        # cmds.uvSnapshot( o=True, n=(path +'snap_advanced.tga'), ff = 'tga', aa = True, xr = width, yr = height )
        cmds.uvSnapshot(o=True, n=(path + 'hard_alpha.png'), ff='png', aa=True, xr=width, yr=height)

        cmds.select(uv)

        cmds.polySelectConstraint(sm=0)  # turn off edge smoothness constraint
        cmds.polySelectConstraint(m=0)
        cmds.polySelectConstraint(w=0, t=0x0010)


def moveShellToSquare(objectsString):
    objects = objectsString.split(' ')
    for objt in objects:
        if objt:
            print('CURRENT OBJECT', objt)
            bbx2d = cmds.polyEvaluate(objt, b2=True)
            print('BOUNDING BOX UV', bbx2d)
            cmds.optionVar(iv=('inViewMessageEnable', 1))
            cmds.optionVar(iv=('inViewMessageAssistEnable', 1))
            if bbx2d[0][0] < 0 and bbx2d[0][1] < 0 or bbx2d[0][0] > 1 and bbx2d[0][1] > 1 or bbx2d[1][0] < 0 and \
                    bbx2d[1][1] < 0 or bbx2d[1][0] > 1 and bbx2d[1][1] > 1:
                cmds.inViewMessage(amg='Any Uvs outside square', pos='midCenter', fade=True)
                time.sleep(2)


def selectedEdges(size):
    selected = cmds.filterExpand(sm=32)
    print(len(selected))
    listOfLines = generateLineFromEdges(selected, size)
    # imageGenerator(listOfLines, "D:/sps.png", 1024, 1024)
    return listOfLines


def generateLineFromEdges(edges, val):
    linesEdge = []
    val = val * 1.333
    for edg in edges:
        uvs = cmds.polyListComponentConversion(edg, tuv=1)
        uvs = cmds.ls(uvs, fl=1)
        if len(uvs) > 2:  # edge on texture border
            # print "BIG"
            vrtFace = cmds.polyListComponentConversion(edg, tvf=1)
            vrtFace = cmds.ls(vrtFace, fl=1)
            # cmds.select(vrtFace)
            # vrtFace.sort()
            # print vrtFace

            uv_0_0 = cmds.polyListComponentConversion(vrtFace[0], tuv=1)
            # print "UV", uv_0_0
            uv_0_0_coord = cmds.polyEditUV(uv_0_0, query=True)
            uv_0_0_coord[1] = 1.0 - uv_0_0_coord[1]
            # print "1", uv_0_0_coord

            uv_0_1 = cmds.polyListComponentConversion(vrtFace[1], tuv=1)
            # print "UV", uv_0_1
            uv_0_1_coord = cmds.polyEditUV(uv_0_1, query=True)
            uv_0_1_coord[1] = 1.0 - uv_0_1_coord[1]
            # print "2", uv_0_1_coord

            uv_1_0 = cmds.polyListComponentConversion(vrtFace[2], tuv=1)
            uv_1_0_coord = cmds.polyEditUV(uv_1_0, query=True)
            uv_1_0_coord[1] = 1.0 - uv_1_0_coord[1]

            uv_1_1 = cmds.polyListComponentConversion(vrtFace[3], tuv=1)
            uv_1_1_coord = cmds.polyEditUV(uv_1_1, query=True)
            uv_1_1_coord[1] = 1.0 - uv_1_1_coord[1]

            line_first = (uv_0_0_coord[0] * val, uv_0_0_coord[1] * val, uv_0_1_coord[0] * val, uv_0_1_coord[1] * val)
            line_second = (uv_1_0_coord[0] * val, uv_1_0_coord[1] * val, uv_1_1_coord[0] * val, uv_1_1_coord[1] * val)

            linesEdge.append(line_first)
            linesEdge.append(line_second)

        else:
            # print "SMALL"
            uv_0_0_coord = cmds.polyEditUV(uvs[0], query=True)
            uv_0_0_coord[1] = 1.0 - uv_0_0_coord[1]

            uv_0_1_coord = cmds.polyEditUV(uvs[1], query=True)
            uv_0_1_coord[1] = 1.0 - uv_0_1_coord[1]

            line_one = (uv_0_0_coord[0] * val, uv_0_0_coord[1] * val, uv_0_1_coord[0] * val, uv_0_1_coord[1] * val)
            linesEdge.append(line_one)

    # print linesEdge
    return linesEdge


def createCircle(points, path, size):
    lines = []
    size = QSize(size * 1.333, size * 1.333)
    picture = QImage(size, QImage.Format_ARGB32_Premultiplied)
    picture.fill(0)
    picture.setAlphaChannel(picture)

    painter = QPainter()
    painter.begin(picture)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBackgroundMode(Qt.TransparentMode)
    pen = QPen()
    color = QColor(255, 255, 255)
    pen.setColor(color)
    pen.setWidth(5)
    pen.setCapStyle(Qt.RoundCap)
    painter.setPen(pen)
    for p in points:
        # line1 = QLineF(p)
        line2 = QLineF(p[0], p[1], p[2], p[3])
        # lines.append(line1)
        painter.drawLine(line2)
    painter.end()

    # imagefile = QImageWriter()
    # imagefile.setFileName("D:/circle1.png")
    # imagefile.setFormat("png")
    # imagefile.setQuality(100)
    picture.save(path, "PNG", -1)


def snapshot_main(path, sz, edges):
    # n = selectedEdges(sz)
    listOfLines = generateLineFromEdges(edges, sz)
    execute = createCircle(listOfLines, path, sz)
