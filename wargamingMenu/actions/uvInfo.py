#modificators

action_category = "Main Tools"
action_label = "Map Percent"
action_icon = "icon_mapPercent.png"

#running procedure

import uvTools.wg_uiInfo
from importlib import reload
reload(uvTools.wg_uiInfo)
uvTools.wg_uiInfo.main(100)