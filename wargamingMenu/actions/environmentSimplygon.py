# modificators

action_category = "Objects"
action_label = "Environment Simplygon"

# running procedure


import simplygon.wg_EnvSimplygon

global envSimplygon
try:
    envSimplygon
    envSimplygon.show()
except:
    envSimplygon = simplygon.wg_EnvSimplygon.main()
