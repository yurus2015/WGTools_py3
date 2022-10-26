#modificators

action_category = "Historical Tools"
action_label = "Blueprint Share"

#running procedure
import historicalTools.wg_blueprintShare
reload(historicalTools.wg_blueprintShare)
historicalTools.wg_blueprintShare.main()
