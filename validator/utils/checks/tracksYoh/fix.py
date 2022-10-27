import maya.cmds as cmds
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'check'))
from . import check


def rename(tracks, side):
    temp_list = []
    for track in tracks:
        track = cmds.ls(track[0], l=1)[0]
        no_name = cmds.rename(track, 'noname')
        temp_list.append(no_name)
    for i in range(len(temp_list)):
        cmds.rename(temp_list[i], 'track_' + side + str(i))


def main(*args):
    if args:
        lods = check.valid_lods()
        for lod in lods:
            tracks = check.all_tracks(lod)
            left, right = check.side_track(tracks)

            rename(left, 'L')
            rename(right, 'R')

    return []
