import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 57
checkLabel = "4.16 Check name of UV sets"


def main(*args):
    objList = vl_listAllTransforms()
    returnList = []
    for x in objList:
        uvSets = cmds.polyUVSet(x, query=True, allUVSets=True)
        if uvSets:
            if len(uvSets) == 1 and uvSets[0] != 'map1':
                cmds.polyUVSet(x, rename=True, newUVSet='map1', uvSet=uvSets[0])

            else:
                if len(uvSets) == 2:
                    if uvSets[0] != 'map1':
                        try:
                            cmds.polyUVSet(x, rename=True, newUVSet='map1', uvSet=uvSets[0])
                        except:
                            pass
                    if uvSets[1] != 'map2':
                        try:
                            cmds.polyUVSet(x, rename=True, newUVSet='map2', uvSet=uvSets[1])
                        except:
                            pass

    return []
