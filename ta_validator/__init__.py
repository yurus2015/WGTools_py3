from os.path import dirname, basename, isfile
import glob
import os

for root, dirs, files in os.walk(dirname(__file__)):
	print('ROOT', (root))
	print('DIR', (dirs))
	print('FILES', (files))

def reload_package():
	print('Package reload')
	# print 'Dir_name', dirname(__file__)


modules = glob.glob(dirname(__file__) + "/*.py")
# print 'ALL ', modules
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

from . import *
for module in __all__:
	print("Module: ", module)
	# reload(module)

del dirname, basename, isfile, glob, modules


# reload_package()