import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 33


def deleteCurrentLayers():
    displayLayers = cmds.ls(type="displayLayer", l=1)
    displayLayers.remove("defaultLayer")
    if displayLayers:
        cmds.delete(displayLayers)


def main(*args):
    deleteCurrentLayers()
    displayLayers = []

    lodList = cmds.ls("*lod*", l=1)

    if lodList:
        for lod in lodList:

            relatives = cmds.listRelatives(lod, c=1, f=1)

            for rel in relatives:

                if rel.find("bsp") == -1:
                    layerName = rel.split("|")[-1].title()  # object name lower case

                    if layerName not in displayLayers:  # at the beginning its actually empty

                        displayLayers.append(layerName)
                        cmds.createDisplayLayer(n=layerName, empty=1)

                    cmds.editDisplayLayerMembers(layerName, rel)

    # sorting
    dLayers = cmds.ls(l=1, type="displayLayer")
    dLayers.remove("defaultLayer")

    layer_hull = []
    layer_turret = []
    layer_gun = []
    layer_chassis = []

    for layer in dLayers:
        if "Hull" in layer:
            layer_hull.append(layer)
        elif "Turret" in layer:
            layer_turret.append(layer)
        elif "Gun" in layer:
            layer_gun.append(layer)
        elif "Chassis" in layer:
            layer_chassis.append(layer)

    layer_hull = sorted(layer_hull, reverse=True)
    layer_turret = sorted(layer_turret, reverse=True)
    layer_gun = sorted(layer_gun, reverse=True)
    layer_chassis = sorted(layer_chassis, reverse=True)
    resultLayer = layer_chassis + layer_gun + layer_turret + layer_hull

    for idx, i in enumerate(resultLayer):
        objects = cmds.editDisplayLayerMembers(i, q=1, fn=1)
        cmds.delete(i)
        cmds.createDisplayLayer(n=i, empty=1)
        cmds.editDisplayLayerMembers(i, objects)
        cmds.setAttr(i + '.displayOrder', idx + 1)
