#modificators

action_category = "Tank Tools"
action_label = "Bake Hangar Shadow"
action_icon = "icon_hangarShadow.png"


#running procedure
import hangarShadow.hangarShadow as hs
reload(hs)
hs.main()
