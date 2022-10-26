"""
This API is responsible for work with havok
"""

settings = {
    "nodes": "hkNodeRigidBody"
            }

import maya.cmds as cmds

'''check if havok plugin is turned on or even exist|install in maya'''

def check_havok_plugin():
    try:
        cmds.pluginInfo("hctMayaSceneExport.mll", q=True)
        return True
    except:
        return False

def get_havok_nodes():
    rigid_body_nodes = cmds.ls(type = "hkNodeRigidBody")
    return rigid_body_nodes

