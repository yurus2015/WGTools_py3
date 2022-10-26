#modificators

action_category = "TechArt Tools"
action_label = "Collider Creation Toolset"

#running procedure


import CCToolset.main
global cctInstance

try:
    cctInstance
    cctInstance.main()
except:
    cctInstance = CCToolset.main.run()


