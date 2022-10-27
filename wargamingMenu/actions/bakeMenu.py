# modificators

action_category = "Tank Tools"
action_label = "Baker"
action_icon = "icon_bakeMenu.png"

# running procedure


import wg_modelingToolset.lib.utl_baker.main as bk

reload(bk)
ops = bk.ToolUnit()
ops.runAction()
