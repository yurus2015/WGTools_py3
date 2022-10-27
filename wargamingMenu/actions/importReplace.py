# modificators
action_category = "Main Tools"
action_label = "Import|Replace"
action_icon = "icon_importReplace.svg"
# running procedure

import sceneTools.importReplaceEditor as ire
from importlib import reload

reload(ire)
ire.main()
