import subprocess, sys, traceback, itertools
from comtypes.client import CreateObject, GetActiveObject


PHOTOSHOP_VERSION = ['80', '90', '100', '110', '120', '130', '140', '150', '160', '170']


def running_photoshop():
	for v in PHOTOSHOP_VERSION:
		try:
			app = GetActiveObject('Photoshop.Application.' + v)
			print('APP', app, v)
			return app, v
		except Exception:
			print('FAILED VERSION ' + v)
	return None, None


def run_photoshop():
	app = CreateObject('Photoshop.Application', dynamic=True)
	return app


def _action_script(app, template, color=None, gray=None):
	print('COLOR', color)
	color_layer = None
	gray_layer = None
	app.open(template)
	doc = app.activeDocument
	layers = doc.layerSets
	for layer in layers:
		print(layer.name)
		art_layers = layer.layers
		# return
		for art_layer in art_layers:
			print('ART', art_layer.name)
			if art_layer.name == 'color_background':
				print('CB')
				color_layer = art_layer
				# doc.activeLayer = art_layer
				# # paste_image(app, color)
				# id_Plc = app.charIDToTypeID("Plc ")
				# ad = CreateObject("Photoshop.ActionDescriptor", dynamic=True)
				# id_null = app.charIDToTypeID("null")
				# ad.putPath(id_null, color)
				# app.executeAction(id_Plc, ad)
				# break
			if art_layer.name == 'gray_background':
				print('GB')
				gray_layer = art_layer

	# bug in cycle paste image
	doc.activeLayer = color_layer
	paste_image(app, color)
	doc.activeLayer = gray_layer
	paste_image(app, gray)


def action_script(app, version, template, gray_file=None, color_file=None):
	app.open(template)
	docRef = app.activeDocument
	print('DOC', docRef.fullName)
	layers = docRef.layerSets
	for layer in layers:
		print(layer.name)
		art_layers = layer.layers
		for art_layer in art_layers:
			print('ART', art_layer.name)
			if art_layer.name == 'color_background':
				docRef.activeLayer = art_layer
				paste_action(app, version, color_file)


def paste_image(app, file):
	print('FILE', file)
	id_Plc = app.charIDToTypeID("Plc ")
	ad = CreateObject("Photoshop.ActionDescriptor", dynamic=True)
	id_null = app.charIDToTypeID("null")
	ad.putPath(id_null, file)
	app.executeAction(id_Plc, ad)


def paste_action(app, version, file):
	idPlc = app.charIDToTypeID("Plc ")
	idPlc = app.charIDToTypeID("Plc ")
	ad = CreateObject("Photoshop.ActionDescriptor." + version)
	idnull = app.charIDToTypeID("null")
	ad.putPath(idnull, file)
	app.executeAction(idPlc, ad)

	# docRef.activeLayer = docRef.layerSets.getByName("gray_object").layers.getByName("gray_background")
	# docRef.layers.getByName('gray_object').layers.getByName('gray_background')

	# activeDocument.activeLayer = activeDocument.layerSets[groupname].artLayers.getByName (actLay);
	# layer = docRef.artLayers.getByName("gray_background")
	# docRef.activeLayer = docRef.layerSets["add_gray_light"].artLayers.getByName("gray_background")
