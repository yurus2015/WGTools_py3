import maya.cmds as cmds

# from validator.utils.validator_API import *

checkId = 33


def checkIsGroup(obj):
    objRelatives = cmds.ls(cmds.listRelatives(obj, c=1), type="mesh", l=1, fl=1)
    if len(objRelatives) == 1:
        return False
    else:
        return True


def main():
    returnList = []
    wrongChildLayer = []
    lodList = cmds.ls("*lod*", type="transform", l=1)
    for lod in lodList:
        lodChilds = cmds.listRelatives(lod, ad=1, f=1, type='mesh')
        for child in lodChilds:
            try:
                cmds.editDisplayLayerMembers('defaultLayer', child)
            except:
                None

            childTransform = cmds.listRelatives(child, p=1, f=1, type='transform')
            childLayer = cmds.listConnections(childTransform[0], type="displayLayer")
            # print 'Layer', childLayer[0]
            if childLayer == None:
                tmp = []
                tmp.append(str(childTransform[0]) + " - is not attached to any layer")
                tmp.append(str(childTransform[0]))
                returnList.append(tmp)
            else:
                if 'hull' in childTransform[0] and 'Hull' not in childLayer[0]:
                    # print 'Hull_transform', childTransform[0], 'Layer?', childLayer[0]
                    wrongChildLayer.append(childTransform[0])
                if 'turret' in childTransform[0] and 'Turret' not in childLayer[0]:
                    wrongChildLayer.append(childTransform[0])
                if 'gun' in childTransform[0] and 'Gun' not in childLayer[0]:
                    wrongChildLayer.append(childTransform[0])
                if 'chassis' in childTransform[0] and 'Chassis' not in childLayer[0]:
                    # print 'Chassis_transform', childTransform[0], 'Layer?', childLayer[0]
                    wrongChildLayer.append(childTransform[0])
    if wrongChildLayer:
        for wrong in wrongChildLayer:
            tmp = []
            tmp.append(str(wrong) + " - attached to a wrong layer")
            tmp.append(str(wrong))
            returnList.append(tmp)

    return returnList
