packages = list(sys.modules.keys())
for p in packages:
    if p.startswith('modelingToolset'):
        del sys.modules[p]

from importlib import reload
import modelingToolset.main as modelToolset
reload(modelToolset)
modelToolset.main()
