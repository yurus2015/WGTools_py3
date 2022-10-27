import maya.utils
import maya.cmds as cmds
import subprocess

try:
    module_update = cmds.moduleInfo(path=True, moduleName='WRG')
    cmd = 'svn update ' + module_update
    subprocess.call(cmd, shell=False)
except:
    pass

try:
    import wargamingMenu.main

    maya.utils.executeDeferred('wargamingMenu.main.run()')
except:
    print('Open Wargaming Menu failed')

try:
    if not cmds.commandPort(":7001", query=True):
        cmds.commandPort(name=":7001")
    else:
        print('Command port opened')
except:
    print('Can`t open Blender port')

'''
try:
	import modelingToolset2019.main
	maya.utils.executeDeferred('modelingToolset2019.main.main()')
except:
	print('Load Modeling Toolset failed')

try:
	import validator.main
	maya.utils.executeDeferred('validator.main.main()')
except:
	print('Load Validator failed')
'''
