# modificators

action_category = "TechArt Tools"
action_label = "Full Metal Toolset"

# running procedure


global fmtCleanStart
fmtCleanStart = False

import full_metal_toolset

global fmt
global fmtCleanStart

if fmtCleanStart:
    fmt.close()
    fmt = None
    packages = ['full_metal_toolset']
    for i in sys.modules.keys()[:]:
        for package in packages:
            if i.startswith(package):
                del sys.modules[i]
    import full_metal_toolset

    reload(full_metal_toolset)
    fmtCleanStart = False

try:
    import full_metal_toolset

    fmt.show()
except:
    fmt = full_metal_toolset.full_metal_gui.show()
