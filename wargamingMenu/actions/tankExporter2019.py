# modificators

action_category = "Tank Tools"
action_label = "Tank Exporter 2019 Beta"
action_icon = "icon_tankExport.png"
# running procedure

import tank_export.tank_export_2019 as te

reload(te)
te.main()
