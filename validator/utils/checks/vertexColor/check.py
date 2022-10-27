# from PySide import QtCore, QtGui
import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI

# from shiboken import wrapInstance

checkId = 201
checkLabel = "Check Vertex Color"


# def getMayaWindow():
#	main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
#	return wrapInstance(long(main_window_ptr), QtGui.QWidget)

def removeDupplicateList(currentList):
    resultList = list(set(currentList))
    return resultList


def main():
    returnList = []
    mesh = cmds.ls(typ='mesh')
    if mesh:
        transfs = cmds.listRelatives(mesh, p=1, type='transform', f=1)
        transfs = removeDupplicateList(transfs)
        for m in transfs:

            c_sets = cmds.polyColorSet(m, query=True, allColorSets=True)
            if c_sets:
                # transf = cmds.listRelatives(m, p = 1, type  = 'transform', f =1)
                if 'HP' in m:
                    continue

                tmp = []
                tmp.append(m + " - has vertex color")
                tmp.append(m)
                returnList.append(tmp)

    return returnList
