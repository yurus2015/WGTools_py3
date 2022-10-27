import maya.standalone

# Start Maya in batch mode
maya.standalone.initialize()
from sys import argv
import maya.cmds as cmds
import maya.mel as mel


# import re
# import os


def deleteLods():
    print
    'delete Lods'
    try:
        cmds.delete(all=1, constructionHistory=1)
    except:
        pass

    try:
        cmds.delete('lod0')
    except:
        pass
    try:
        cmds.delete('lod1')
    except:
        pass
    try:
        cmds.delete('lod2')
    except:
        pass
    try:
        cmds.delete('lod3')
    except:
        pass

    try:
        cmds.delete('nodes')
    except:
        pass


def deleteShaders():
    materials = cmds.ls(mat=1)
    for mat in materials:
        try:
            cmds.delete(mat)
        except:
            pass

    print
    'delete Shaders'


def deleteLayers():
    layers = cmds.ls(typ='displayLayer')
    for lay in layers:
        try:
            cmds.delete(lay)
        except:
            pass
    print
    'delete Layers'


def optimizeScene():
    print
    'optimaze Scene'
    """scene optimization"""
    mel.eval('''
			string $which[] = {
			"nurbsSrfOption",
			"nurbsCrvOption",
			"unusedNurbsSrfOption",
			"clipOption",
			"poseOption",
			"ptConOption",
			"pbOption",
			"deformerOption",
			"unusedSkinInfsOption",
			"expressionOption",
			"groupIDnOption",
			"animationCurveOption",
			"snapshotOption",
			"unitConversionOption",
			"shaderOption",
			"cachedOption",
			"transformOption",
			"displayLayerOption",
			"renderLayerOption",
			"setsOption",
			"partitionOption",
			"referencedOption",
			"brushOption",
			"unknownNodesOption",
			"shadingNetworksOption"
			};
			scOpt_saveAndClearOptionVars(1);
			scOpt_setOptionVars( $which );
			cleanUpScene( 1 );
			scOpt_saveAndClearOptionVars(0);
		''')


def exportAll():
    mayaTempDir = cmds.internalVar(userTmpDir=True)
    cmds.file(mayaTempDir + 'lod4.mb', force=True, ea=True, type="mayaBinary")
    print
    'Export lod4'


def main():
    fileToOpen = argv[1]
    cmds.file(fileToOpen, force=True, open=True)

    deleteLods()
    deleteShaders()
    deleteLayers()
    exportAll()


if __name__ == "__main__":
    main()
