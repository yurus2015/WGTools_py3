import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya


def validation_bounding_box(wheel):
    minimum = cmds.getAttr(wheel + '.boundingBoxMin')
    maximum = cmds.getAttr(wheel + '.boundingBoxMax')
    height = maximum[0][1] - minimum[0][1]
    width = maximum[0][2] - minimum[0][2]
    if ("%.4f" % height) == ("%.4f" % width):
        return True
    return False


def mesh_baricentric(wheel):
    # Get the MObject for the mesh
    sel_list = OpenMaya.MSelectionList()
    dag = OpenMaya.MDagPath()  # don't need this?
    sel_list.add(wheel)
    dag_path = sel_list.getDagPath(0)

    # Create a mesh function set
    mesh_fn = OpenMaya.MFnMesh(dag_path)

    # Get the coordinates of all the vertices in the mesh
    vertex = OpenMaya.MPointArray()  # don't need this?
    vertex = mesh_fn.getPoints(OpenMaya.MSpace.kWorld)

    # Calculate the coordinates of the center
    n = len(vertex)
    center_x = sum([point.x for point in vertex]) / n
    center_y = sum([point.y for point in vertex]) / n
    center_z = sum([point.z for point in vertex]) / n
    center = (center_x, center_y, center_z)

    return center


# create function for check maya current units
def maya_current_units():
    if cmds.currentUnit(q=True, linear=True) == 'cm':
        return 100
    return 1
