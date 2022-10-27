# modificators

action_category = "TechArt Tools"
action_label = "CoreX Collision"
action_icon = "icon_tankExport.png"
# running procedure

import coldWarTools.objExport.cw_obj_exporter as coe

reload(coe)
coe.main()
