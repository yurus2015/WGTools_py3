import sys

packages = list(sys.modules.keys())
for p in packages:
    if p.startswith('modelingToolset'):
        del sys.modules[p]

import modelingToolset.main as modeling_toolset

# from importlib import reload
#
# reload(modeling_toolset)
modeling_toolset.main()
