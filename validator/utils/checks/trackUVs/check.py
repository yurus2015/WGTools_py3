"""This script checks whether certain criteria are met
for the tracks in a Maya scene. The range must be a multiple of one.
Check if the UV range is within an allowed range
(determined by the tolerance and the length of the UV range)
"""

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya


def main():
    # Initialize an empty list to store the results
    return_list = []

    # Set the tolerance for UV scale checking
    tolerance = 0.002

    # Check if the scene is a crash scene
    file_name = cmds.file(q=True, sn=True, shn=True)
    if "crash" not in file_name:

        # Get a list of all transforms in the scene that contain the word "track"
        track_list = cmds.ls("*track*", l=1, type="transform")
        if not track_list:
            # If there are no tracks, return the empty list
            return []

        # Create a selection list to store the tracks that have mesh children
        selection_list = OpenMaya.MSelectionList()
        for i in track_list:
            if cmds.listRelatives(i, type="mesh", f=1):
                selection_list.add(i)

        # Iterate over the selected tracks
        iterator = OpenMaya.MItSelectionList(selection_list)

        while not iterator.isDone():

            # Get the DAG path for the current track
            dag_path = OpenMaya.MDagPath()
            iterator.getDagPath(dag_path)

            # Create an MFnMesh object for the current track
            fn_mesh = OpenMaya.MFnMesh(dag_path)

            # Get the UVs for the current track
            u_array = OpenMaya.MFloatArray()
            v_array = OpenMaya.MFloatArray()
            fn_mesh.getUVs(u_array, v_array)

            # Calculate the length of the UV range in the V direction
            length = max(v_array) - min(v_array)
            length = round(length, 3)

            # Get the decimal part of the length
            decimal = float("0." + str(length).split(".")[-1])

            # Get the integer part of the length
            actual = int(str(length).split(".")[0])

            # Calculate the upper bound of the allowed UV range
            actual_upper = actual + 1

            # Check if the UV range is within the allowed range
            if actual_upper - decimal < actual_upper - tolerance:
                # If the UV range is not within the allowed range, 
                # create a message and add it to the results list
                tmp = [dag_path.fullPathName() + " UVs must have " + str(float(actual)) + " or " + str(
                    float(actual + 1)) + " of V scale", dag_path.fullPathName()]

                return_list.append(tmp)

            next(iterator)

    return return_list
