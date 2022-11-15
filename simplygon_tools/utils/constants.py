import os
from pathlib import Path

HOST_PORT = '10.151.248.30:55001'
HOST = '10.151.248.30'
PORT = 55001

CURRENT_DIR = os.path.realpath(__file__)
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../../.."))
ALT_PARENT = str(Path(CURRENT_DIR).parents[4])

COMMON_FILES = os.path.join(str(ALT_PARENT), "simplygon")
FBX_PRESET = os.path.join(COMMON_FILES, 'fbx.fbximportpreset')
SPL_PRESET = os.path.join(COMMON_FILES, 'lods.spl')

INPUT_FILES = os.path.join(COMMON_FILES, "input", "export.fbx")
OUTPUT_FILES = os.path.join(COMMON_FILES, "output")
IMPORT_FILES = os.path.join(OUTPUT_FILES, "lods", 'export')

SIMPLYGON_EXE = os.path.join(COMMON_FILES, 'SimplygonBatch.exe')
