#modificators

action_category = "Historical Tools"
action_label = "Blueprint Share"

#running procedure
import historicalTools.blueprintplus as bpp
reload(bpp)
bpp.main()
