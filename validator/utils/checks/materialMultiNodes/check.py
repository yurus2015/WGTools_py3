import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 1003
checkLabel = "10.0 Check multiply materials"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []

    allSceneMaterials = cmds.ls(mat=1)

    # check assigned mat
    for mat in allSceneMaterials:
        tmp = []
        cmds.select(mat)
        cmds.hyperShade(objects=mat)
        faces = cmds.ls(cmds.filterExpand(sm=34), l=1)

        if faces:
            # Horrible Dirty Shit for havok preset
            if "havok" in cmds.file(q=1, sn=1):
                if "havok" not in faces[0].split("|")[1]:
                    continue

            tmp.append(mat + " assigned to faces, need assign to object")
            tmp.append(faces)
            returnList.append(tmp)
            cmds.select(cl=1)

    return returnList
