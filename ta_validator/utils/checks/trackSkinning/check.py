import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 47

checkLabel = "Check skinning of tracks"

def main():
    print('<< ' + checkLabel.upper() + ' >>')
    tracks_R, tracks_L = vl_findTracksInLods()
    returnList = []

    def searchClusters(array):
        listJoints = cmds.ls (type="joint")

        if len(listJoints) > 0:
            for x in array:
                shape = cmds.listRelatives(x, f=True)
                cluster = False
                for x in shape:
                    if cmds.listConnections (x, c = True, type = "skinCluster") != None:
                        cluster = True
                        break

                if not cluster:
                    tmp = []
                    tmp.append(x)
                    tmp.append(x)
                    returnList.append(tmp)

    searchClusters(tracks_R)
    searchClusters(tracks_L)



    return  returnList
