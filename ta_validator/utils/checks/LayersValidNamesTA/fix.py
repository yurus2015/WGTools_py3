import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 33

checkLabel = "1.9 Check layers of objects "

def deleteCurrentLayers():
    displayLayers = cmds.ls(type = "displayLayer", l=1)
    displayLayers.remove("defaultLayer")
    if displayLayers:
    	cmds.delete(displayLayers)

def main(*args):



    fileName = cmds.file(q=1,sn=1)

    if not "collision" in fileName:

        deleteCurrentLayers()
        displayLayers = []

        lodList = cmds.ls("*lod*", l=1)

        if lodList:
            for lod in lodList:

                relatives = cmds.listRelatives(lod, c=1, f=1)

                for rel in relatives:

                    if rel.find("bsp") == -1:
                        layerName = rel.split("|")[-1].title()
                        if layerName not in displayLayers:
                            displayLayers.append(layerName)
                            cmds.createDisplayLayer(n=layerName, empty=1)
                        cmds.editDisplayLayerMembers(layerName, rel)







