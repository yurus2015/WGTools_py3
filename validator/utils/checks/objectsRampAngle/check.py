import maya.cmds as cmds
import maya.OpenMaya as om
import math

checkId = 1255
checkLabel = "Check ramp angle"


############################################
#
#				Utilites
#
############################################
def dotproduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))


def length(v):
    return math.sqrt(dotproduct(v, v))


def angle(v1, v2):
    return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


############################################
#
#				Main
#
############################################
def main():
    ramp_meshes = cmds.ls('*ramp*', typ='transform', l=True)

    selection = om.MSelectionList()
    selection.clear()
    for x in ramp_meshes:
        selection.add(x)
    # om.MGlobal.getActiveSelectionList(selection)
    selection_iter = om.MItSelectionList(selection)

    obj = om.MObject()

    return_list = []

    # Loop through iterator objects
    while not selection_iter.isDone():
        selection_iter.getDependNode(obj)
        dagPath = om.MDagPath.getAPathTo(obj)
        faceIter = om.MItMeshPolygon(dagPath)
        normal = om.MVector()
        list_badFace = []
        # Loop through iterator faces
        while not faceIter.isDone():
            faceIter.getNormal(normal, om.MSpace.kWorld)
            # print ('normal : [%s, %s, %s]' % (normal.x, normal.y, normal.z))
            try:
                angle_face = math.degrees(angle([normal.x, normal.y, normal.z], [0, 1, 0]))
            # print angle_face
            except:
                angle_face = 90.0

            # Check angle more than 40 degree
            if angle_face > 40.0:
                id = faceIter.index()
                list_badFace.append(dagPath.fullPathName() + ".f[" + str(id) + "]")

            # tmp = []
            # tmp.append(dagPath.fullPathName()[:len(dagPath.fullPathName()) - len(dagPath.fullPathName().split("|")[-1])-1] + ".f[" + str(id) + "]")
            # tmp.append(dagPath.fullPathName()[:len(dagPath.fullPathName()) - len(dagPath.fullPathName().split("|")[-1])-1] + ".f[" + str(id) + "]")
            # return_list.append(tmp)

            next(faceIter)
        if list_badFace:
            tmp = []
            tmp.append(dagPath.fullPathName() + " ramp has faces with angle more 40 degrees")
            tmp.append(list_badFace)
            return_list.append(tmp)

        next(selection_iter)

    return return_list
