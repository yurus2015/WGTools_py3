from importlib import reload

action_category = "Tank Tools"
action_label = "Simplygon Tanks"
action_icon = "icon_simplygonTank.png"

#running procedure
import simplygon_tanks.wg_simplygon_main as wgsm
reload(wgsm)
wgsm.main()