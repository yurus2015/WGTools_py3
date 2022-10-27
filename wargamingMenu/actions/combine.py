action_category = "Main Tools"
action_label = "Combine"
action_icon = "icon_combine.svg"

import sceneTools.combinePro as cmb
from importlib import reload

reload(cmb)
cmb.combineObject(True)
