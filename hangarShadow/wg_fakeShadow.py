#basic libraries
import maya.cmds as cmds
import maya.mel as mel
#maya2018 pyside2

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *


from shiboken2 import wrapInstance
import maya.OpenMayaUI as omu
import maya.OpenMaya as OpenMaya
import os, time

#Pointer to the main window
def mainWindowPointer():
	ptr = omu.MQtUtil.mainWindow() #pointer for the main window
	return wrapInstance(long(ptr), QWidget)



#QT GUI Class
class myNewWindow(QDialog):
	#initialization
	def __init__(self, parent = mainWindowPointer()):
		QDialog.__init__(self,parent)
		self.setWindowTitle("fakeShadowExporter")
		self.setFixedSize(400, 150);
		self.setObjectName("id_fakeShadowExporter")

		self.renderPath = "C:/temp/fakeShadows/"
		self.projectName = cmds.file(q=1,sn=1, shn=1).split(".")[0]
		self.fileName  = cmds.file(q=1,sn=1, shn=1).split(".")[0]
		self.projectPath = None

		self.setLayout(self.create_layout())
		self.connections()

	#here we create GUI elements
	def create_layout(self):

		self.btnOK =   QPushButton("Generate");

		self.dirGrp     = QGroupBox("Save Folder")
		self.folder_HLayout     =   QHBoxLayout()
		self.pathTxt    = QLineEdit()
		self.pathTxt.setEnabled(0)
		self.buttonDir  = QPushButton("Dir")
		self.folder_HLayout.addWidget(self.pathTxt)
		self.folder_HLayout.addWidget(self.buttonDir)
		self.dirGrp.setLayout(self.folder_HLayout)

		#set default folder for savings
		saveFolder = "C:/temp/fakeShadows"
		saveFolder = cmds.optionVar(q = "wg_saveFakeShadowFolder")
		if not saveFolder:
			saveFolder = "C:/temp/fakeShadows"
			cmds.optionVar(sv = ("wg_saveFakeShadowFolder", saveFolder))

		self.pathTxt.setText(str(saveFolder))
		saveFolder = saveFolder.replace("\\", "/")
		self.renderPath = saveFolder
		print("Render Folder: ", self.renderPath)

		#main layout
		self.mainLayout =  QVBoxLayout()

		self.mainLayout.addWidget(self.dirGrp)
		self.mainLayout.addWidget(self.btnOK)

		return self.mainLayout

	#connect widgets with functions
	def connections(self):
		self.connect(self.btnOK, QtCore.SIGNAL("clicked()"), self.generateShadowMap)
		self.connect(self.buttonDir, QtCore.SIGNAL("clicked()"), self.dirFolder)

	def dirFolder(self):
		currentPath = self.pathTxt.text()
		path = None
		try:
			path = cmds.fileDialog2(fm=3, dialogStyle=1, dir = currentPath)[0]
		except:
			pass

		if path:
			cmds.optionVar(sv=("wg_saveFakeShadowFolder", path))
			self.pathTxt.setText(path)
			path = path.replace("\\", "/")
			self.renderPath = path

		print("New folder: ", self.renderPath)

	def renderShadow(self, plane):

		currentTime = time.strftime("%H%M%S")
		currentDate = time.strftime("%d%B%Y")

		project = self.projectName + "_" + currentDate + "_" + currentTime #project filder name = file name + day + time

		if not os.path.exists(self.renderPath + "/" + project):
			os.makedirs(self.renderPath + "/" + project)

		fullRenderPath = self.renderPath + "/" + project
		self.projectPath = fullRenderPath

		oldWS = cmds.workspace(q=1, fn=1)
		cmds.workspace(fr=["images", fullRenderPath])
		cmds.workspace(u=1)
		print(fullRenderPath)
		#mel.eval('ilrTextureBakeCmd \
		#	-sf on \
		#	-target "pasted__bakeShape"\
		#	-camera "persp"   \
		#	-directory "'+ fullRenderPath +'" \
		#	-fileName "turtleTmpRender.png" \
		#	-fileFormat 9 \
		#	-fullShading 1 \
		#	-useRenderView 1 \
		#	-width 1024 \
		#	-height 1024;')
		# -layer defaultRenderLayer1;')
		command = 'ilrTextureBakeCmd  \
		-target '+ plane +' \
		-selectionMode 0 \
		-camera "persp" \
		-normalDirection 0 \
		-bakeLayer TurtleDefaultBakeLayer \
		-width 1024 \
		-height 1024 \
		-saveToRenderView 0 \
		-saveToFile 1 \
		-directory "'+ fullRenderPath +'" \
		-fileName "turtleTmpRender.png" \
		-fileFormat 9 \
		-edgeDilation 3 \
		-bilinearFilter 0 \
		-merge 1 \
		-fullShading 1 \
		-useRenderView 1; '

		mel.eval(command)



		cmds.workspace(fr=[fullRenderPath, oldWS])
		cmds.workspace(u=1)
		cmds.workspace(s=1)
		return 1

	def bakeAO_renderSetting(self):

		try:
			mel.eval('ilrDefaultNodes(0);')
			mel.eval('ilrDefaultNodes(1);')
		except:
			mel.eval('ilrDefaultNodes();')

		render = "TurtleRenderOptions"
		cmds.setAttr(render + ".renderer", 1)
		cmds.setAttr(render + ".aaMinSampleRate", 0)
		#cmds.setAttr(render + ".imageFormat", 9)
		#render layer
		cmds.setAttr("TurtleDefaultBakeLayer.renderType", 1)
		#cmds.setAttr("TurtleDefaultBakeLayer.renderSelection", 1)
		#setAttr "TurtleRenderOptions.imageFormat" 9;




	def meshTurtleAO(self, planeShape):
		#set TURTLE as default renderer and setup it
		cmds.setAttr('defaultRenderGlobals.currentRenderer', 'turtle', type='string')

		selForOcl = cmds.ls(sl=1)
		#bakeLayer = mel.eval('ilrCreateBakeLayer("", 1)')

		oclShader = cmds.shadingNode("ilrOccSampler", asShader = 1)
		cmds.setAttr(oclShader + ".minSamples", 64)
		cmds.setAttr(oclShader + ".enableAdaptiveSampling", 0)

		cmds.select(selForOcl)
		cmds.hyperShade(assign = oclShader)

		self.bakeAO_renderSetting()

		#cmds.setAttr("TurtleRenderOptions.renderer", 1)
		#cmds.setAttr("TurtleRenderOptions.aaMinSampleRate", 0)

		#cmds.setAttr(bakeLayer + ".tbResX", 1024)
		#cmds.setAttr(bakeLayer + ".tbResY", 1024)
#
		#cmds.setAttr(bakeLayer + ".tbMerge", 1)
		#cmds.setAttr(bakeLayer + ".tbSaveToRenderView", 1)
		#cmds.setAttr(bakeLayer + ".tbEdgeDilation", 3)
		#cmds.setAttr(bakeLayer + ".tbBilinearFilter", 0)

		renderOutput = self.renderShadow(planeShape)

		if renderOutput:
			print("Done Didone")

	def cleanProjectDir(self):
		try:
			os.remove(self.projectPath+"/psEdit.jsx")
		except:
			pass

		try:
			cmds.delete('pasted__bake*')
		except:
			pass

	def generateShadowJSX(self):
		lines_save = []

		projectPath = self.projectPath.replace("/","\\\\")

		#open the file
		lines_save.append('var idOpn = charIDToTypeID( "Opn " );\n')
		lines_save.append('var desc41 = new ActionDescriptor();\n')
		lines_save.append('var idnull = charIDToTypeID( "null" );\n')
		lines_save.append('desc41.putPath( idnull, new File( "' + projectPath + '\\\\turtleTmpRender.png" ) );\n')
		lines_save.append('executeAction( idOpn, desc41, DialogModes.NO );\n')

		#make it as a layer0
		lines_save.append('var idsetd = charIDToTypeID( "setd" );\n')
		lines_save.append('var desc49 = new ActionDescriptor();\n')
		lines_save.append('var idnull = charIDToTypeID( "null" );\n')
		lines_save.append('var ref28 = new ActionReference();\n')
		lines_save.append('var idLyr = charIDToTypeID( "Lyr " );\n')
		lines_save.append('var idBckg = charIDToTypeID( "Bckg" );\n')
		lines_save.append('ref28.putProperty( idLyr, idBckg );\n')
		lines_save.append('desc49.putReference( idnull, ref28 );\n')
		lines_save.append('var idT = charIDToTypeID( "T   " );\n')
		lines_save.append('var desc50 = new ActionDescriptor();\n')
		lines_save.append('var idOpct = charIDToTypeID( "Opct" );\n')
		lines_save.append('var idPrc = charIDToTypeID( "#Prc" );\n')
		lines_save.append('desc50.putUnitDouble( idOpct, idPrc, 100.000000 );\n')
		lines_save.append('var idMd = charIDToTypeID( "Md  " );\n')
		lines_save.append('var idBlnM = charIDToTypeID( "BlnM" );\n')
		lines_save.append('var idNrml = charIDToTypeID( "Nrml" );\n')
		lines_save.append('desc50.putEnumerated( idMd, idBlnM, idNrml );\n')
		lines_save.append('var idLyr = charIDToTypeID( "Lyr " );\n')
		lines_save.append('desc49.putObject( idT, idLyr, desc50 );\n')
		lines_save.append('executeAction( idsetd, desc49, DialogModes.NO );\n')



		#set lavels 215
		lines_save.append('var idLvls = charIDToTypeID( "Lvls" );\n')
		lines_save.append('var desc51 = new ActionDescriptor();\n')
		lines_save.append('var idpresetKind = stringIDToTypeID( "presetKind" );\n')
		lines_save.append('var idpresetKindType = stringIDToTypeID( "presetKindType" );\n')
		lines_save.append('var idpresetKindCustom = stringIDToTypeID( "presetKindCustom" );\n')
		lines_save.append('desc51.putEnumerated( idpresetKind, idpresetKindType, idpresetKindCustom );\n')
		lines_save.append('var idAdjs = charIDToTypeID( "Adjs" );\n')
		lines_save.append('var list7 = new ActionList();\n')
		lines_save.append('var desc52 = new ActionDescriptor();\n')
		lines_save.append('var idChnl = charIDToTypeID( "Chnl" );\n')
		lines_save.append('var ref29 = new ActionReference();\n')
		lines_save.append('var idChnl = charIDToTypeID( "Chnl" );\n')
		lines_save.append('var idChnl = charIDToTypeID( "Chnl" );\n')
		lines_save.append('var idCmps = charIDToTypeID( "Cmps" );\n')
		lines_save.append('ref29.putEnumerated( idChnl, idChnl, idCmps );\n')
		lines_save.append('desc52.putReference( idChnl, ref29 );\n')
		lines_save.append('var idInpt = charIDToTypeID( "Inpt" );\n')
		lines_save.append('var list8 = new ActionList();\n')
		lines_save.append('list8.putInteger( 0 );\n')
		lines_save.append('list8.putInteger( 215 );\n')
		lines_save.append('desc52.putList( idInpt, list8 );\n')
		lines_save.append('var idLvlA = charIDToTypeID( "LvlA" );\n')
		lines_save.append('list7.putObject( idLvlA, desc52 );\n')
		lines_save.append('desc51.putList( idAdjs, list7 );\n')
		lines_save.append('executeAction( idLvls, desc51, DialogModes.NO );\n')


		#set blur
		lines_save.append('var idGsnB = charIDToTypeID( "GsnB" );\n')
		lines_save.append('var desc53 = new ActionDescriptor();\n')
		lines_save.append('var idRds = charIDToTypeID( "Rds " );\n')
		lines_save.append('var idPxl = charIDToTypeID( "#Pxl" );\n')
		lines_save.append('desc53.putUnitDouble( idRds, idPxl, 1.000000 );\n')
		lines_save.append('executeAction( idGsnB, desc53, DialogModes.NO );\n')

		#reset Colors
		lines_save.append('var idRset = charIDToTypeID( "Rset" );\n')
		lines_save.append('var desc54 = new ActionDescriptor();\n')
		lines_save.append('var idnull = charIDToTypeID( "null" );\n')
		lines_save.append('var ref30 = new ActionReference();\n')
		lines_save.append('var idClr = charIDToTypeID( "Clr " );\n')
		lines_save.append('var idClrs = charIDToTypeID( "Clrs" );\n')
		lines_save.append('ref30.putProperty( idClr, idClrs );\n')
		lines_save.append('desc54.putReference( idnull, ref30 );\n')
		lines_save.append('executeAction( idRset, desc54, DialogModes.NO );\n')



		#ACTIONS

		#dublicate layer to layer 0 copy

		# lines_save.append('var idslct = charIDToTypeID( "slct" );\n')
		# lines_save.append('var desc17 = new ActionDescriptor();\n')
		# lines_save.append('var idnull = charIDToTypeID( "null" );\n')
		# lines_save.append('var ref12 = new ActionReference();\n')
		# lines_save.append('var idHstS = charIDToTypeID( "HstS" );\n')
		# lines_save.append('var idOrdn = charIDToTypeID( "Ordn" );\n')
		# lines_save.append('var idPrvs = charIDToTypeID( "Prvs" );\n')
		# lines_save.append('ref12.putEnumerated( idHstS, idOrdn, idPrvs );\n')
		# lines_save.append('desc17.putReference( idnull, ref12 );\n')
		# lines_save.append('executeAction( idslct, desc17, DialogModes.NO );\n')

		lines_save.append('var idDplc = charIDToTypeID( "Dplc" );\n')
		lines_save.append('var desc18 = new ActionDescriptor();\n')
		lines_save.append('var idnull = charIDToTypeID( "null" );\n')
		lines_save.append('var ref13 = new ActionReference();\n')
		lines_save.append('var idLyr = charIDToTypeID( "Lyr " );\n')
		lines_save.append('var idOrdn = charIDToTypeID( "Ordn" );\n')
		lines_save.append('var idTrgt = charIDToTypeID( "Trgt" );\n')
		lines_save.append('ref13.putEnumerated( idLyr, idOrdn, idTrgt );\n')
		lines_save.append('desc18.putReference( idnull, ref13 );\n')
		lines_save.append('var idVrsn = charIDToTypeID( "Vrsn" );\n')
		lines_save.append('desc18.putInteger( idVrsn, 5 );\n')
		lines_save.append('executeAction( idDplc, desc18, DialogModes.NO );\n')

		#select layer 0 (which was a background layer)

		lines_save.append('var idslct = charIDToTypeID( "slct" );\n')
		lines_save.append('    var desc23 = new ActionDescriptor();\n')
		lines_save.append('    var idnull = charIDToTypeID( "null" );\n')
		lines_save.append('        var ref18 = new ActionReference();\n')
		lines_save.append('        var idLyr = charIDToTypeID( "Lyr " );\n')
		lines_save.append('        ref18.putName( idLyr, "Layer 0" );\n')
		lines_save.append('    desc23.putReference( idnull, ref18 );\n')
		lines_save.append('    var idMkVs = charIDToTypeID( "MkVs" );\n')
		lines_save.append('    desc23.putBoolean( idMkVs, false );\n')
		lines_save.append('executeAction( idslct, desc23, DialogModes.NO );\n')

		#fill layer with the background color

		lines_save.append('var idFl = charIDToTypeID( "Fl  " );\n')
		lines_save.append('    var desc39 = new ActionDescriptor();\n')
		lines_save.append('    var idUsng = charIDToTypeID( "Usng" );\n')
		lines_save.append('    var idFlCn = charIDToTypeID( "FlCn" );\n')
		lines_save.append('    var idBckC = charIDToTypeID( "BckC" );\n')
		lines_save.append('    desc39.putEnumerated( idUsng, idFlCn, idBckC );\n')
		lines_save.append('    var idOpct = charIDToTypeID( "Opct" );\n')
		lines_save.append('    var idPrc = charIDToTypeID( "#Prc" );\n')
		lines_save.append('    desc39.putUnitDouble( idOpct, idPrc, 100.000000 );\n')
		lines_save.append('    var idMd = charIDToTypeID( "Md  " );\n')
		lines_save.append('    var idBlnM = charIDToTypeID( "BlnM" );\n')
		lines_save.append('    var idNrml = charIDToTypeID( "Nrml" );\n')
		lines_save.append('    desc39.putEnumerated( idMd, idBlnM, idNrml );\n')
		lines_save.append('executeAction( idFl, desc39, DialogModes.NO );\n')


		# selecy copy layer

		lines_save.append('var idslct = charIDToTypeID( "slct" );\n')
		lines_save.append('    var desc41 = new ActionDescriptor();\n')
		lines_save.append('    var idnull = charIDToTypeID( "null" );\n')
		lines_save.append('        var ref24 = new ActionReference();\n')
		lines_save.append('        var idLyr = charIDToTypeID( "Lyr " );\n')
		lines_save.append('        ref24.putName( idLyr, "Layer 0 copy" );\n')
		lines_save.append('    desc41.putReference( idnull, ref24 );\n')
		lines_save.append('    var idMkVs = charIDToTypeID( "MkVs" );\n')
		lines_save.append('    desc41.putBoolean( idMkVs, false );\n')
		lines_save.append('executeAction( idslct, desc41, DialogModes.NO );\n')

		# set the opacity 80%

		lines_save.append('var idsetd = charIDToTypeID( "setd" );\n')
		lines_save.append('    var desc49 = new ActionDescriptor();\n')
		lines_save.append('    var idnull = charIDToTypeID( "null" );\n')
		lines_save.append('        var ref29 = new ActionReference();\n')
		lines_save.append('        var idLyr = charIDToTypeID( "Lyr " );\n')
		lines_save.append('        var idOrdn = charIDToTypeID( "Ordn" );\n')
		lines_save.append('        var idTrgt = charIDToTypeID( "Trgt" );\n')
		lines_save.append('        ref29.putEnumerated( idLyr, idOrdn, idTrgt );\n')
		lines_save.append('    desc49.putReference( idnull, ref29 );\n')
		lines_save.append('    var idT = charIDToTypeID( "T   " );\n')
		lines_save.append('        var desc50 = new ActionDescriptor();\n')
		lines_save.append('        var idOpct = charIDToTypeID( "Opct" );\n')
		lines_save.append('        var idPrc = charIDToTypeID( "#Prc" );\n')
		lines_save.append('        desc50.putUnitDouble( idOpct, idPrc, 80.000000 );\n')
		lines_save.append('    var idLyr = charIDToTypeID( "Lyr " );\n')
		lines_save.append('    desc49.putObject( idT, idLyr, desc50 );\n')
		lines_save.append('executeAction( idsetd, desc49, DialogModes.NO );\n')


		#select another layer and merge all layers


		lines_save.append('var idslct = charIDToTypeID( "slct" );\n')
		lines_save.append('    var desc52 = new ActionDescriptor();\n')
		lines_save.append('    var idnull = charIDToTypeID( "null" );\n')
		lines_save.append('        var ref31 = new ActionReference();\n')
		lines_save.append('        var idLyr = charIDToTypeID( "Lyr " );\n')
		lines_save.append('        ref31.putName( idLyr, "Layer 0" );\n')
		lines_save.append('    desc52.putReference( idnull, ref31 );\n')
		lines_save.append('    var idselectionModifier = stringIDToTypeID( "selectionModifier" );\n')
		lines_save.append('    var idselectionModifierType = stringIDToTypeID( "selectionModifierType" );\n')
		lines_save.append('    var idaddToSelectionContinuous = stringIDToTypeID( "addToSelectionContinuous" );\n')
		lines_save.append('    desc52.putEnumerated( idselectionModifier, idselectionModifierType, idaddToSelectionContinuous );\n')
		lines_save.append('    var idMkVs = charIDToTypeID( "MkVs" );\n')
		lines_save.append('    desc52.putBoolean( idMkVs, false );\n')
		lines_save.append('executeAction( idslct, desc52, DialogModes.NO );\n')


		lines_save.append('var idMrgtwo = charIDToTypeID( "Mrg2" );\n')
		lines_save.append('    var desc53 = new ActionDescriptor();\n')
		lines_save.append('executeAction( idMrgtwo, desc53, DialogModes.NO );\n')


		#crop the canvas to 512-horizontal


		lines_save.append('var idCnvS = charIDToTypeID( "CnvS" );\n')
		lines_save.append('    var desc54 = new ActionDescriptor();\n')
		lines_save.append('    var idWdth = charIDToTypeID( "Wdth" );\n')
		lines_save.append('    var idPxl = charIDToTypeID( "#Pxl" );\n')
		lines_save.append('    desc54.putUnitDouble( idWdth, idPxl, 512.000000 );\n')
		lines_save.append('    var idHrzn = charIDToTypeID( "Hrzn" );\n')
		lines_save.append('    var idHrzL = charIDToTypeID( "HrzL" );\n')
		lines_save.append('    var idCntr = charIDToTypeID( "Cntr" );\n')
		lines_save.append('    desc54.putEnumerated( idHrzn, idHrzL, idCntr );\n')
		lines_save.append('executeAction( idCnvS, desc54, DialogModes.NO );\n')


		# set selection to all

		lines_save.append('var idsetd = charIDToTypeID( "setd" );\n')
		lines_save.append('    var desc55 = new ActionDescriptor();\n')
		lines_save.append('    var idnull = charIDToTypeID( "null" );\n')
		lines_save.append('        var ref32 = new ActionReference();\n')
		lines_save.append('        var idChnl = charIDToTypeID( "Chnl" );\n')
		lines_save.append('        var idfsel = charIDToTypeID( "fsel" );\n')
		lines_save.append('        ref32.putProperty( idChnl, idfsel );\n')
		lines_save.append('    desc55.putReference( idnull, ref32 );\n')
		lines_save.append('    var idT = charIDToTypeID( "T   " );\n')
		lines_save.append('    var idOrdn = charIDToTypeID( "Ordn" );\n')
		lines_save.append('    var idAl = charIDToTypeID( "Al  " );\n')
		lines_save.append('    desc55.putEnumerated( idT, idOrdn, idAl );\n')
		lines_save.append('executeAction( idsetd, desc55, DialogModes.NO );\n')

		#copy current selection ?????????
		lines_save.append('var idcopy = charIDToTypeID( "copy" );\n')
		lines_save.append('executeAction( idcopy, undefined, DialogModes.NO );\n')

		#create an empty alpha channel
		lines_save.append('var idMk = charIDToTypeID( "Mk  " );\n')
		lines_save.append('var desc115 = new ActionDescriptor();\n')
		lines_save.append('var idNw = charIDToTypeID( "Nw  " );\n')
		lines_save.append('var desc116 = new ActionDescriptor();\n')
		lines_save.append('var idClrI = charIDToTypeID( "ClrI" );\n')
		lines_save.append('var idMskI = charIDToTypeID( "MskI" );\n')
		lines_save.append('var idMskA = charIDToTypeID( "MskA" );\n')
		lines_save.append('desc116.putEnumerated( idClrI, idMskI, idMskA );\n')
		lines_save.append('var idClr = charIDToTypeID( "Clr " );\n')
		lines_save.append('var desc117 = new ActionDescriptor();\n')
		lines_save.append('var idRd = charIDToTypeID( "Rd  " );\n')
		lines_save.append('desc117.putDouble( idRd, 255.000000 );\n')
		lines_save.append('var idGrn = charIDToTypeID( "Grn " );\n')
		lines_save.append('desc117.putDouble( idGrn, 0.000000 );\n')
		lines_save.append('var idBl = charIDToTypeID( "Bl  " );\n')
		lines_save.append('desc117.putDouble( idBl, 0.000000 );\n')
		lines_save.append('var idRGBC = charIDToTypeID( "RGBC" );\n')
		lines_save.append('desc116.putObject( idClr, idRGBC, desc117 );\n')
		lines_save.append('var idOpct = charIDToTypeID( "Opct" );\n')
		lines_save.append('desc116.putInteger( idOpct, 50 );\n')
		lines_save.append('var idChnl = charIDToTypeID( "Chnl" );\n')
		lines_save.append('desc115.putObject( idNw, idChnl, desc116 );\n')
		lines_save.append('executeAction( idMk, desc115, DialogModes.NO );\n')

		#paste copied to the alpha-channel
		lines_save.append('var idpast = charIDToTypeID( "past" );\n')
		lines_save.append('var desc140 = new ActionDescriptor();\n')
		lines_save.append('var idAntA = charIDToTypeID( "AntA" );\n')
		lines_save.append('var idAnnt = charIDToTypeID( "Annt" );\n')
		lines_save.append('var idAnno = charIDToTypeID( "Anno" );\n')
		lines_save.append('desc140.putEnumerated( idAntA, idAnnt, idAnno );\n')
		lines_save.append('executeAction( idpast, desc140, DialogModes.NO );\n')

		#invert alpha channel
		lines_save.append('var idInvr = charIDToTypeID( "Invr" );\n')
		lines_save.append('executeAction( idInvr, undefined, DialogModes.NO );\n')

		#select RGB Channel

		lines_save.append('var idslct = charIDToTypeID( "slct" );\n')
		lines_save.append('var desc164 = new ActionDescriptor();\n')
		lines_save.append('var idnull = charIDToTypeID( "null" );\n')
		lines_save.append('var ref124 = new ActionReference();\n')
		lines_save.append('var idChnl = charIDToTypeID( "Chnl" );\n')
		lines_save.append('var idChnl = charIDToTypeID( "Chnl" );\n')
		lines_save.append('var idRGB = charIDToTypeID( "RGB " );\n')
		lines_save.append('ref124.putEnumerated( idChnl, idChnl, idRGB );\n')
		lines_save.append('desc164.putReference( idnull, ref124 );\n')
		lines_save.append('executeAction( idslct, desc164, DialogModes.NO );\n')

		#fill it out with the foreground color

		lines_save.append('var idFl = charIDToTypeID( "Fl  " );\n')
		lines_save.append('var desc165 = new ActionDescriptor();\n')
		lines_save.append('var idUsng = charIDToTypeID( "Usng" );\n')
		lines_save.append('var idFlCn = charIDToTypeID( "FlCn" );\n')
		lines_save.append('var idFrgC = charIDToTypeID( "FrgC" );\n')
		lines_save.append('desc165.putEnumerated( idUsng, idFlCn, idFrgC );\n')
		lines_save.append('var idOpct = charIDToTypeID( "Opct" );\n')
		lines_save.append('var idPrc = charIDToTypeID( "#Prc" );\n')
		lines_save.append('desc165.putUnitDouble( idOpct, idPrc, 100.000000 );\n')
		lines_save.append('var idMd = charIDToTypeID( "Md  " );\n')
		lines_save.append('var idBlnM = charIDToTypeID( "BlnM" );\n')
		lines_save.append('var idNrml = charIDToTypeID( "Nrml" );\n')
		lines_save.append('desc165.putEnumerated( idMd, idBlnM, idNrml );\n')
		lines_save.append('executeAction( idFl, desc165, DialogModes.NO );\n')

		#image size

		lines_save.append('var idImgS = charIDToTypeID( "ImgS" );\n')
		lines_save.append('var desc166 = new ActionDescriptor();\n')
		lines_save.append('var idHght = charIDToTypeID( "Hght" );\n')
		lines_save.append('var idPxl = charIDToTypeID( "#Pxl" );\n')
		lines_save.append('desc166.putUnitDouble( idHght, idPxl, 512.000000 );\n')
		lines_save.append('var idscaleStyles = stringIDToTypeID( "scaleStyles" );\n')
		lines_save.append('desc166.putBoolean( idscaleStyles, true );\n')
		lines_save.append('var idCnsP = charIDToTypeID( "CnsP" );\n')
		lines_save.append('desc166.putBoolean( idCnsP, true );\n')
		lines_save.append('var idIntr = charIDToTypeID( "Intr" );\n')
		lines_save.append('var idIntp = charIDToTypeID( "Intp" );\n')
		lines_save.append('var idbicubicSharper = stringIDToTypeID( "bicubicSharper" );\n')
		lines_save.append('desc166.putEnumerated( idIntr, idIntp, idbicubicSharper );\n')
		lines_save.append('executeAction( idImgS, desc166, DialogModes.NO );\n')

		#save file as DDS in the project folder

		lines_save.append('var idsave = charIDToTypeID( "save" );\n')
		lines_save.append('var desc35 = new ActionDescriptor();\n')
		lines_save.append('var idAs = charIDToTypeID( "As  " );\n')
		lines_save.append('var desc36 = new ActionDescriptor();\n')
		lines_save.append('var idbarF = charIDToTypeID( "barF" );\n')
		lines_save.append('desc36.putBoolean( idbarF, true );\n')
		lines_save.append('var idfdev = charIDToTypeID( "fdev" );\n')
		lines_save.append('desc36.putDouble( idfdev, 3.000000 );\n')
		lines_save.append('var idfbia = charIDToTypeID( "fbia" );\n')
		lines_save.append('desc36.putDouble( idfbia, 0.000000 );\n')
		lines_save.append('var idurad = charIDToTypeID( "urad" );\n')
		lines_save.append('desc36.putDouble( idurad, 5.000000 );\n')
		lines_save.append('var iduamo = charIDToTypeID( "uamo" );\n')
		lines_save.append('desc36.putDouble( iduamo, 0.500000 );\n')
		lines_save.append('var iduthr = charIDToTypeID( "uthr" );\n')
		lines_save.append('desc36.putDouble( iduthr, 0.000000 );\n')
		lines_save.append('var idxstf = charIDToTypeID( "xstf" );\n')
		lines_save.append('desc36.putDouble( idxstf, 1.000000 );\n')
		lines_save.append('var idxthf = charIDToTypeID( "xthf" );\n')
		lines_save.append('desc36.putDouble( idxthf, 1.000000 );\n')
		lines_save.append('var idqual = charIDToTypeID( "qual" );\n')
		lines_save.append('desc36.putInteger( idqual, 70 );\n')
		lines_save.append('var iderdi = charIDToTypeID( "erdi" );\n')
		lines_save.append('desc36.putBoolean( iderdi, false );\n')
		lines_save.append('var iderdw = charIDToTypeID( "erdw" );\n')
		lines_save.append('desc36.putInteger( iderdw, 1 );\n')
		lines_save.append('var idusfa = charIDToTypeID( "usfa" );\n')
		lines_save.append('desc36.putBoolean( idusfa, false );\n')
		lines_save.append('var idtxfm = charIDToTypeID( "txfm" );\n')
		lines_save.append('desc36.putInteger( idtxfm, 3 );\n')
		lines_save.append('var idweig = charIDToTypeID( "weig" );\n')
		lines_save.append('desc36.putInteger( idweig, 0 );\n')
		lines_save.append('var idtmty = charIDToTypeID( "tmty" );\n')
		lines_save.append('desc36.putInteger( idtmty, 0 );\n')
		lines_save.append('var idmmty = charIDToTypeID( "mmty" );\n')
		lines_save.append('desc36.putInteger( idmmty, 32 );\n')
		lines_save.append('var idsmip = charIDToTypeID( "smip" );\n')
		lines_save.append('desc36.putInteger( idsmip, 0 );\n')
		lines_save.append('var idbina = charIDToTypeID( "bina" );\n')
		lines_save.append('desc36.putBoolean( idbina, false );\n')
		lines_save.append('var idprem = charIDToTypeID( "prem" );\n')
		lines_save.append('desc36.putBoolean( idprem, false );\n')
		lines_save.append('var idfilm = charIDToTypeID( "film" );\n')
		lines_save.append('desc36.putBoolean( idfilm, false );\n')
		lines_save.append('var idalpb = charIDToTypeID( "alpb" );\n')
		lines_save.append('desc36.putBoolean( idalpb, false );\n')
		lines_save.append('var idbord = charIDToTypeID( "bord" );\n')
		lines_save.append('desc36.putBoolean( idbord, false );\n')
		lines_save.append('var idbrdr = charIDToTypeID( "brdr" );\n')
		lines_save.append('desc36.putDouble( idbrdr, 0.000000 );\n')
		lines_save.append('var idbrdg = charIDToTypeID( "brdg" );\n')
		lines_save.append('desc36.putDouble( idbrdg, 0.000000 );\n')
		lines_save.append('var idbrdb = charIDToTypeID( "brdb" );\n')
		lines_save.append('desc36.putDouble( idbrdb, 0.000000 );\n')
		lines_save.append('var idmmft = charIDToTypeID( "mmft" );\n')
		lines_save.append('desc36.putInteger( idmmft, 2 );\n')
		lines_save.append('var idfdcl = charIDToTypeID( "fdcl" );\n')
		lines_save.append('desc36.putBoolean( idfdcl, false );\n')
		lines_save.append('var idfdaf = charIDToTypeID( "fdaf" );\n')
		lines_save.append('desc36.putBoolean( idfdaf, false );\n')
		lines_save.append('var idftworl = charIDToTypeID( "f2rl" );\n')
		lines_save.append('desc36.putDouble( idftworl, 0.500000 );\n')
		lines_save.append('var idftwogl = charIDToTypeID( "f2gl" );\n')
		lines_save.append('desc36.putDouble( idftwogl, 0.500000 );\n')
		lines_save.append('var idftwobl = charIDToTypeID( "f2bl" );\n')
		lines_save.append('desc36.putDouble( idftwobl, 0.500000 );\n')
		lines_save.append('var idftwoal = charIDToTypeID( "f2al" );\n')
		lines_save.append('desc36.putDouble( idftwoal, 0.500000 );\n')
		lines_save.append('var idfddl = charIDToTypeID( "fddl" );\n')
		lines_save.append('desc36.putInteger( idfddl, 0 );\n')
		lines_save.append('var idfafm = charIDToTypeID( "fafm" );\n')
		lines_save.append('desc36.putDouble( idfafm, 0.150000 );\n')
		lines_save.append('var idbafh = charIDToTypeID( "bafh" );\n')
		lines_save.append('desc36.putDouble( idbafh, 0.500000 );\n')
		lines_save.append('var iddthc = charIDToTypeID( "dthc" );\n')
		lines_save.append('desc36.putBoolean( iddthc, false );\n')
		lines_save.append('var iddthzero = charIDToTypeID( "dth0" );\n')
		lines_save.append('desc36.putBoolean( iddthzero, false );\n')
		lines_save.append('var idsmth = charIDToTypeID( "smth" );\n')
		lines_save.append('desc36.putInteger( idsmth, 0 );\n')
		lines_save.append('var idfilg = charIDToTypeID( "filg" );\n')
		lines_save.append('desc36.putDouble( idfilg, 2.200000 );\n')
		lines_save.append('var idfieg = charIDToTypeID( "fieg" );\n')
		lines_save.append('desc36.putBoolean( idfieg, false );\n')
		lines_save.append('var idfilw = charIDToTypeID( "filw" );\n')
		lines_save.append('desc36.putDouble( idfilw, 10.000000 );\n')
		lines_save.append('var idover = charIDToTypeID( "over" );\n')
		lines_save.append('desc36.putBoolean( idover, false );\n')
		lines_save.append('var idfblr = charIDToTypeID( "fblr" );\n')
		lines_save.append('desc36.putDouble( idfblr, 1.000000 );\n')
		lines_save.append('var idnmcv = charIDToTypeID( "nmcv" );\n')
		lines_save.append('desc36.putBoolean( idnmcv, false );\n')
		lines_save.append('var idncnv = charIDToTypeID( "ncnv" );\n')
		lines_save.append('desc36.putInteger( idncnv, 1009 );\n')
		lines_save.append('var idnflt = charIDToTypeID( "nflt" );\n')
		lines_save.append('desc36.putInteger( idnflt, 1040 );\n')
		lines_save.append('var idnmal = charIDToTypeID( "nmal" );\n')
		lines_save.append('desc36.putInteger( idnmal, 1034 );\n')
		lines_save.append('var idnmbr = charIDToTypeID( "nmbr" );\n')
		lines_save.append('desc36.putBoolean( idnmbr, false );\n')
		lines_save.append('var idnmix = charIDToTypeID( "nmix" );\n')
		lines_save.append('desc36.putBoolean( idnmix, false );\n')
		lines_save.append('var idnmiy = charIDToTypeID( "nmiy" );\n')
		lines_save.append('desc36.putBoolean( idnmiy, false );\n')
		lines_save.append('var idnmiz = charIDToTypeID( "nmiz" );\n')
		lines_save.append('desc36.putBoolean( idnmiz, false );\n')
		lines_save.append('var idnmah = charIDToTypeID( "nmah" );\n')
		lines_save.append('desc36.putBoolean( idnmah, false );\n')
		lines_save.append('var idnswp = charIDToTypeID( "nswp" );\n')
		lines_save.append('desc36.putBoolean( idnswp, false );\n')
		lines_save.append('var idnmsc = charIDToTypeID( "nmsc" );\n')
		lines_save.append('desc36.putDouble( idnmsc, 2.200000 );\n')
		lines_save.append('var idnmnz = charIDToTypeID( "nmnz" );\n')
		lines_save.append('desc36.putInteger( idnmnz, 0 );\n')
		lines_save.append('var idusbi = charIDToTypeID( "usbi" );\n')
		lines_save.append('desc36.putBoolean( idusbi, false );\n')
		lines_save.append('var idlien = charIDToTypeID( "lien" );\n')
		lines_save.append('desc36.putBoolean( idlien, false );\n')
		lines_save.append('var idshdi = charIDToTypeID( "shdi" );\n')
		lines_save.append('desc36.putBoolean( idshdi, false );\n')
		lines_save.append('var idshfi = charIDToTypeID( "shfi" );\n')
		lines_save.append('desc36.putBoolean( idshfi, false );\n')
		lines_save.append('var idshmm = charIDToTypeID( "shmm" );\n')
		lines_save.append('desc36.putBoolean( idshmm, true );\n')
		lines_save.append('var idshan = charIDToTypeID( "shan" );\n')
		lines_save.append('desc36.putBoolean( idshan, true );\n')
		lines_save.append('var idclrc = charIDToTypeID( "clrc" );\n')
		lines_save.append('desc36.putInteger( idclrc, 0 );\n')
		lines_save.append('var idvdxone = charIDToTypeID( "vdx1" );\n')
		lines_save.append('desc36.putBoolean( idvdxone, true );\n')
		lines_save.append('var idvdxtwo = charIDToTypeID( "vdx2" );\n')
		lines_save.append('desc36.putBoolean( idvdxtwo, true );\n')
		lines_save.append('var idvdxthree = charIDToTypeID( "vdx3" );\n')
		lines_save.append('desc36.putBoolean( idvdxthree, true );\n')
		lines_save.append('var idvdxfive = charIDToTypeID( "vdx5" );\n')
		lines_save.append('desc36.putBoolean( idvdxfive, true );\n')
		lines_save.append('var idvfourfourfour = charIDToTypeID( "v444" );\n')
		lines_save.append('desc36.putBoolean( idvfourfourfour, true );\n')
		lines_save.append('var idvfivefivefive = charIDToTypeID( "v555" );\n')
		lines_save.append('desc36.putBoolean( idvfivefivefive, true );\n')
		lines_save.append('var idvfivesixfive = charIDToTypeID( "v565" );\n')
		lines_save.append('desc36.putBoolean( idvfivesixfive, true );\n')
		lines_save.append('var idveighteighteight = charIDToTypeID( "v888" );\n')
		lines_save.append('desc36.putBoolean( idveighteighteight, true );\n')
		lines_save.append('var idalph = charIDToTypeID( "alph" );\n')
		lines_save.append('desc36.putBoolean( idalph, false );\n')
		lines_save.append('var idusra = charIDToTypeID( "usra" );\n')
		lines_save.append('desc36.putBoolean( idusra, false );\n')
		lines_save.append('var idusfs = charIDToTypeID( "usfs" );\n')
		lines_save.append('desc36.putInteger( idusfs, 0 );\n')
		lines_save.append('var idprev = charIDToTypeID( "prev" );\n')
		lines_save.append('desc36.putBoolean( idprev, false );\n')
		lines_save.append('var idrdep = charIDToTypeID( "rdep" );\n')
		lines_save.append('desc36.putInteger( idrdep, 3000 );\n')
		lines_save.append('var idlomm = charIDToTypeID( "lomm" );\n')
		lines_save.append('desc36.putBoolean( idlomm, false );\n')
		lines_save.append('var idsflp = charIDToTypeID( "sflp" );\n')
		lines_save.append('desc36.putBoolean( idsflp, false );\n')
		lines_save.append('var idlflp = charIDToTypeID( "lflp" );\n')
		lines_save.append('desc36.putBoolean( idlflp, false );\n')
		lines_save.append('var idscar = charIDToTypeID( "scar" );\n')
		lines_save.append('desc36.putDouble( idscar, 1.000000 );\n')
		lines_save.append('var idscag = charIDToTypeID( "scag" );\n')
		lines_save.append('desc36.putDouble( idscag, 1.000000 );\n')
		lines_save.append('var idscab = charIDToTypeID( "scab" );\n')
		lines_save.append('desc36.putDouble( idscab, 1.000000 );\n')
		lines_save.append('var idscaa = charIDToTypeID( "scaa" );\n')
		lines_save.append('desc36.putDouble( idscaa, 1.000000 );\n')
		lines_save.append('var idbiar = charIDToTypeID( "biar" );\n')
		lines_save.append('desc36.putDouble( idbiar, 0.000000 );\n')
		lines_save.append('var idbiag = charIDToTypeID( "biag" );\n')
		lines_save.append('desc36.putDouble( idbiag, 0.000000 );\n')
		lines_save.append('var idbiab = charIDToTypeID( "biab" );\n')
		lines_save.append('desc36.putDouble( idbiab, 0.000000 );\n')
		lines_save.append('var idbiaa = charIDToTypeID( "biaa" );\n')
		lines_save.append('desc36.putDouble( idbiaa, 0.000000 );\n')
		lines_save.append('var idsiar = charIDToTypeID( "siar" );\n')
		lines_save.append('desc36.putDouble( idsiar, 1.000000 );\n')
		lines_save.append('var idsiag = charIDToTypeID( "siag" );\n')
		lines_save.append('desc36.putDouble( idsiag, 1.000000 );\n')
		lines_save.append('var idsiab = charIDToTypeID( "siab" );\n')
		lines_save.append('desc36.putDouble( idsiab, 1.000000 );\n')
		lines_save.append('var idsiaa = charIDToTypeID( "siaa" );\n')
		lines_save.append('desc36.putDouble( idsiaa, 1.000000 );\n')
		lines_save.append('var idbiir = charIDToTypeID( "biir" );\n')
		lines_save.append('desc36.putDouble( idbiir, 0.000000 );\n')
		lines_save.append('var idbiig = charIDToTypeID( "biig" );\n')
		lines_save.append('desc36.putDouble( idbiig, 0.000000 );\n')
		lines_save.append('var idbiib = charIDToTypeID( "biib" );\n')
		lines_save.append('desc36.putDouble( idbiib, 0.000000 );\n')
		lines_save.append('var idbiia = charIDToTypeID( "biia" );\n')
		lines_save.append('desc36.putDouble( idbiia, 0.000000 );\n')
		lines_save.append('var idoutw = charIDToTypeID( "outw" );\n')
		lines_save.append('desc36.putBoolean( idoutw, false );\n')
		lines_save.append('var idclcL = charIDToTypeID( "clcL" );\n')
		lines_save.append('desc36.putBoolean( idclcL, true );\n')
		lines_save.append('var idNVIDIADthreeDDS = stringIDToTypeID( "NVIDIA D3D/DDS" );\n')
		lines_save.append('desc35.putObject( idAs, idNVIDIADthreeDDS, desc36 );\n')
		lines_save.append('var idIn = charIDToTypeID( "In  " );\n')
		lines_save.append('desc35.putPath( idIn, new File( "' + projectPath + '\\\\'+self.fileName+'_HangarShadowMap.dds" ) );\n')
		lines_save.append('var idDocI = charIDToTypeID( "DocI" );\n')
		lines_save.append('desc35.putInteger( idDocI, 1502 );\n')
		lines_save.append('var idCpy = charIDToTypeID( "Cpy " );\n')
		lines_save.append('desc35.putBoolean( idCpy, true );\n')
		lines_save.append('var idsaveStage = stringIDToTypeID( "saveStage" );\n')
		lines_save.append('var idsaveStageType = stringIDToTypeID( "saveStageType" );\n')
		lines_save.append('var idsaveBegin = stringIDToTypeID( "saveBegin" );\n')
		lines_save.append('desc35.putEnumerated( idsaveStage, idsaveStageType, idsaveBegin );\n')
		lines_save.append('executeAction( idsave, desc35, DialogModes.NO );\n')



		lines = []
		s = open(self.projectPath+"/psEdit.jsx", "w")
		s.writelines(lines_save)
		s.close()


	def generateShadowMap(self):

		mayaVerison = cmds.about(v = 1) #get maya version

		cmds.currentUnit( linear='m')

		# create projection plane
		if cmds.objExists('pasted__bake*'):
			cmds.delete('pasted__bake*')

		projPlane = cmds.polyPlane(w = 1, h=1, sx=1, sy =1, n = "pasted__bake")[0]
		projPlaneShape = cmds.listRelatives(projPlane, c=1, type="mesh")[0]
		cmds.rename(projPlaneShape, "pasted__bakeShape")

		cmds.xform(projPlane, ws=1, a=1, s=[18.636, 1, 18.636])

		cmds.setAttr(projPlane + ".translateY", -0.006)
		cmds.select(projPlane)

		#Do render
		self.meshTurtleAO(projPlaneShape)

		#delete temporary javascripts if they exist
		self.cleanProjectDir()

		#Create jsx
		self.generateShadowJSX()

		#run photoshop with the script
		projectPath = self.projectPath.replace("/", "\\")
		os.system('start photoshop.exe ' + projectPath + '\\psEdit.jsx')

		if mayaVerison.find("2015") != -1:
			# delete projection plane
			cmds.delete(projPlane)

			cmds.deleteUI("id_fakeShadowExporter")



	def tempProc(self):
		print("test it")

#our main function
def main():
	#load turtle plugin
	pluginStat = cmds.pluginInfo('Turtle.mll', query=True, l=True)
	if pluginStat == False:
		try:
			cmds.loadPlugin('Turtle.mll')
		except:
			print("There is no Turtle plugin in Maya")
			return

	if cmds.window("id_fakeShadowExporter",q=True,exists=True):
		cmds.deleteUI("id_fakeShadowExporter")

	try:
		dialog.close()
	except:
		pass

	dialog = myNewWindow()
	dialog.show()

