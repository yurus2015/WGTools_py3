import maya.OpenMaya as om


class FactoryScene():

    @classmethod
    def find_all_tracks(cls):
        # TODO: refactor 1. return track as a list of nodes: ([track, bounding box, barycentric pivot], [track..])
        # TODO: write c++ command fo this function
        it = om.MItDag(om.MItDag.kDepthFirst, om.MFn.kMesh)

        # List to store the mesh objects
        mesh_list = []
        track_list = []
        wheel_list = []
        # Set the threshold for the length difference
        threshold = 10.0

        # Iterate over the DAG nodes
        while not it.isDone():
            # Get the current DAG node as an MObject
            obj = it.currentItem()

            # Create an MFnDagNode object for the node
            dag_node_fn = om.MFnDagNode(obj)

            # Get the bounding box for the mesh
            bbox = dag_node_fn.boundingBox

            # Get the minimum y value of the bounding box
            min_y = bbox.min.y

            # Get the length of the bounding box along the y-axis
            y_length = bbox.max.y - bbox.min.y

            # Get the length of the bounding box along the z-axis
            z_length = bbox.max.z - bbox.min.z

            # Check if the length of the bounding box along the y-axis is equal to the length along the z-axis
            if abs(y_length - z_length) > threshold:
                # Add the mesh object and its min y value to the list
                mesh_list.append((dag_node_fn.fullPathName(), min_y))
            else:
                # Wheels need checking additionally
                wheel_list.append(dag_node_fn.fullPathName())

            # Move to the next DAG node
            it.next()

        # Sort the list of mesh objects by the min y value
        mesh_list.sort(key=lambda x: x[1])

        # Extract the mesh with the minimum y value but only if value near to first element
        if mesh_list:
            track_list.append(mesh_list[0])
            for i in range(1, len(mesh_list)):
                if abs(mesh_list[0][1] - mesh_list[i][1]) < threshold:
                    track_list.append(mesh_list[i])

        # Extract the list of mesh objects from the sorted list
        sorted_track_list = [mesh[0] for mesh in track_list]

        return (sorted_track_list)
