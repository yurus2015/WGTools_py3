import maya.cmds as cmds
from maya.mel import eval as meval
import os

checkId = 400
checkLabel = "5.4 Check BSP & S_WALL smoothgroup"


def removeDupplicateList(currentList):
    resultList = list(set(currentList))
    return resultList


def main():
    #

    returnList = []

    listAllMesh = cmds.ls(type='transform')
    listAllMesh = cmds.filterExpand(listAllMesh, sm=12)
    if listAllMesh:
        listAllMesh = removeDupplicateList(listAllMesh)

        for mesh in listAllMesh:
            if '_bsp' in mesh.split('|')[-1] or 's_wall' in mesh.split('|')[-1] or 'ramp' in mesh.split('|')[-1]:
                cmds.select(mesh)
                cmds.selectType(pe=True)
                cmds.polySelectConstraint(m=3, t=0x8000, sm=1, w=2)  # to get hard edges
                hards = cmds.ls(sl=1)
                cmds.polySelectConstraint(m=0)  # turn off edge smoothness constraint
                cmds.polySelectConstraint(sm=0, w=0)  # turn off edge smoothness constraint
                cmds.select(d=1)
                if hards:
                    tmp = []
                    tmp.append(mesh + " has hard edges")
                    tmp.append(hards)
                    returnList.append(tmp)

    return returnList
