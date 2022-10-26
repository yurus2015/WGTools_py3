import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 55
checkLabel = "4.17 Check numbers of UV sets"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    objList = vl_listAllTransforms()
    track_L, track_R = vl_findTracksInLods()

    listTrackNames = []
    track_L = re.compile('track_L');     listTrackNames.append(track_L)
    track_R = re.compile('track_R');     listTrackNames.append(track_R)

    returnList = []

    for obj in objList:
        #if this is a track object
        if obj.find("track") != -1:
            uvSets = cmds.polyUVSet (obj, query = True, allUVSets=True) #get all uvSets
            if uvSets:
                if len(uvSets) > 2:
                    stat = 0
                    for idx, i in enumerate(uvSets):
                        if idx > 1:
                            cmds.polyUVSet(obj,  currentUVSet=True,  uvSet=i)
                            uvs = cmds.ls(cmds.polyListComponentConversion(obj, tuv=1), fl=1, l=1)
                            if len(uvs) < 2: #if there are no uvs in the current uv set
                                stat = 1
                                break
                    tmp = []
                    if stat:
                        tmp.append(obj + " has more than 2 UVSets. And some of them are empty!")
                    else:
                        tmp.append(obj + " has more than 2 UVSets.")
                    tmp.append(obj)
                    returnList.append(tmp)
        else:
            uvSets = cmds.polyUVSet (obj, query = True, allUVSets=True) #get all uvSets
            if uvSets:
                if len(uvSets) > 1:
                    stat = 0
                    for idx, i in enumerate(uvSets):
                        if idx > 0:
                            cmds.polyUVSet(obj,  currentUVSet=True,  uvSet=i)
                            uvs = cmds.ls(cmds.polyListComponentConversion(obj, tuv=1), fl=1, l=1)
                            if len(uvs) < 2: #if there are no uvs in the current uv set
                                stat = 1
                                break
                    tmp = []
                    if stat:
                        tmp.append(obj + " has more than 1 UVSets. And some of them are empty!")
                    else:
                        tmp.append(obj + " has more than 1 UVSets.")
                    tmp.append(obj)
                    returnList.append(tmp)


    # for x in range(len(objList)):
        # track=False

        # #check if there are some tracks in the objList
        # for y in listTrackNames:
        #     temp = y.search(objList[x])
        #     if temp !=None:
        #       track = True

        # #if we found no tracks
        # if not track:
        #     uvSets = cmds.polyUVSet (objList[x], query = True, allUVSets=True)
        #     if uvSets:
        #         if len(uvSets) > 1:
        #             tmp = []
        #             tmp.append(objList[x])
        #             tmp.append(objList[x])
        #             returnList.append(tmp)
        # else: #if there are some tracks
        #     uvSets = cmds.polyUVSet (objList[x], query = True, allUVSets=True)
        #     if uvSets:
        #         if len(uvSets) > 2:
        #             tmp = []
        #             tmp.append(objList[x])
        #             tmp.append(objList[x])
        #             returnList.append(tmp)



    return  returnList
