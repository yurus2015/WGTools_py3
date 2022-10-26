import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 55
checkLabel = "4.17 Check numbers of UV sets"


def main(*args):
	#If there are more than 1 UVSet for non tracks OR more than 2 UVSets for tracks -
	#check if those sets have some uvs, iv sets have no uvs - delete them
	#if there are some uvs - return message for each not fixed object like "Object has extra UV sets with UVs in there. Make a decision to delete them or leave them"
    for obj in args:
        #if this is a track object
        if obj.find("track") != -1:
            uvSets = cmds.polyUVSet (obj, query = True, allUVSets=True) #get all uvSets
            if uvSets:
                if len(uvSets) > 2:
                    for idx, i in enumerate(uvSets):
                        if idx > 1:
                            cmds.polyUVSet(obj,  currentUVSet=True,  uvSet=i)
                            uvs = cmds.ls(cmds.polyListComponentConversion(obj, tuv=1), fl=1, l=1)
                            if len(uvs) < 2: #if there are no uvs in the current uv set
                                #delete the uv set
                                cmds.polyUVSet(obj, delete=True )

        else:
            uvSets = cmds.polyUVSet (obj, query = True, allUVSets=True) #get all uvSets
            if uvSets:
                if len(uvSets) > 1:
                    for idx, i in enumerate(uvSets):
                        if idx > 0:
                            cmds.polyUVSet(obj,  currentUVSet=True,  uvSet=i)
                            uvs = cmds.ls(cmds.polyListComponentConversion(obj, tuv=1), fl=1, l=1)
                            if len(uvs) < 2: #if there are no uvs in the current uv set
                                #delete the uv set
                                cmds.polyUVSet(obj, delete=True )
	return []