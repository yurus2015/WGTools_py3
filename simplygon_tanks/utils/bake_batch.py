import maya.standalone
maya.standalone.initialize()
from sys import argv
import maya.cmds as cmds
import maya.mel as mel
#from simplygon_tanks.utils.tank_bake_2019 import Utils

def connect_textures(materials, textures, suffix):


	legacy_materials = materials.split(',')
	legacy_textures = textures.split(',')

	#print '\n'
	#print 'txt\n', legacy_textures
	#print '\n'
	#print 'mat\n', legacy_materials
	#print '\n', len(legacy_materials)

	for i in range(len(legacy_materials)):
		texture_name = legacy_textures[i] + suffix + '.tga'
		if os.path.isfile(texture_name):
			try:
				fileNode = cmds.listConnections(legacy_materials[i] + ".color")
				if fileNode:
					fileNode = fileNode[0]
				else:
					fileNode =cmds.shadingNode('file', asTexture=True, name = legacy_materials[i] + "_file")
					cmds.connectAttr (fileNode + ".outColor" , legacy_materials[i] + ".color", f=True )
				cmds.setAttr(fileNode + ".fileTextureName", texture_name, type="string")

			except:
				pass


def threadingBake(file, sources, targets, materials, textures, name, suffix):
	print '\nI HERE!'
	sources = sources.split(',')
	targets = targets.split(',')

	target_txt = ""
	for i in targets:
		target_txt += "\n-target " + i + ' -uvSet map1 -searchOffset 0.1 -maxSearchDistance 0.4 -searchCage "" '

	sources_txt = ""
	for i in sources:
		sources_txt += "\n-source " + i

	fileName = '\n-filename "' + name + suffix + '"'
	cmd = """surfaceSampler """+ target_txt + sources_txt + """
			-mapOutput diffuseRGB
			-mapWidth 256
			-mapHeight 256
			-max 1
			-mapSpace tangent
			-mapMaterials 1
			-shadows 1 """ + fileName + """
			-fileFormat "tga"
			-superSampling 2
			-filterType 0
			-filterSize 3
			-overscan 1
			-searchMethod 0
			-useGeometryNormals 1
			-ignoreMirroredFaces 0
			-flipU 0
			-flipV 0;
		"""

	cmds.file(file, force=True, open=True)
	connect_textures(materials, textures, suffix)
	mel.eval(cmd)


# Main program
def main():

	print 'STARTING'

	fileToOpen = argv[1]
	source = argv[2]
	target = argv[3]
	material = argv[4]
	textures = argv[5]
	name = argv[6]
	suffix = argv[7]

	print 'FIle ', fileToOpen
	print 'FIle ', source
	print 'FIle ', target
	print 'Mat ', material
	print 'TEX ', textures
	print 'Name ', name
	print 'SFX ', suffix

	threadingBake(fileToOpen, source, target, material, textures, name, suffix)

	print 'Success!'


if __name__ == "__main__":
	main()