action_category = "Main Tools"
action_label = "Validator"
action_icon = "icon_validator.png"

packages = ['ta_validator']
for i in sys.modules.keys():
    for package in packages:
        if i.startswith(package):
            del sys.modules[i]

import ta_validator.main as vld
vld.main(autoload = False)
