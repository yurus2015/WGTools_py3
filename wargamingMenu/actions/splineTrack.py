# modificators

action_category = "Tank Tools"
action_label = "Spline Track"
action_icon = "icon_splineTrack.png"

# running procedure

import spline_track.main

reload(spline_track.main)
global splineTrack
try:
    splineTrack
    splineTrack.main()
except:
    splineTrack = spline_track.main.main()
