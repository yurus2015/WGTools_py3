# modificators
action_category = "Tank Tools"
action_label = "Map border to hard"
action_icon = "icon_hardmap.svg"
# running procedure

import sceneTools.mapHard as mh
from importlib import reload

reload(mh)
mh.map_border_hard()
