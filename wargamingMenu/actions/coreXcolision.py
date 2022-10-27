# modificators

action_category = "TechArt Tools"
action_label = "CoreX Collision"
action_icon = "icon_tankExport.png"
# running procedure

import corex.fbx_export.main as fbxe

reload(fbxe)
fbxe.main()
