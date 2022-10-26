action_category = "Main Tools"
action_label = "Validator"
action_icon = "icon_validator.png"

packages = ['validator']
for i in sys.modules.keys():
    for package in packages:
        if i.startswith(package):
            del sys.modules[i]

import validator.main as vld
vld.main(autoload=False)
