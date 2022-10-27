import maya.cmds as cmds
import re
from validator.utils.validator_API import *

checkId = 8
checkLabel = "1.11 Check placement of chassis"


def main():
    #

    tracks_R, tracks_L = vl_findTracksInLods()
    return_list = []

    for x in tracks_R:
        #                                                  0    1    2    3    4    5
        # The values returned are in the following order: xmin ymin zmin xmax ymax zmax.
        bb = cmds.xform(x, q=True, bb=True)
        if round((bb[3] + bb[0]) / 2, 3) < 0:
            tmp = [x, x]
            return_list.append(tmp)

    for x in tracks_L:
        #                                                  0    1    2    3    4    5
        # The values returned are in the following order: xmin ymin zmin xmax ymax zmax.
        bb = cmds.xform(x, q=True, bb=True)
        if round((bb[3] + bb[0]) / 2, 3) > 0:
            tmp = [x, x]
            return_list.append(tmp)

    return return_list
