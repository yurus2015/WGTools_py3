import json
from validator.gui.constants import PATHPRESET
import os

dir = os.path.dirname(__file__)


class PresetsJson():
    def __init__(self):
        pass

    @classmethod
    def read_json(cls):
        presets = os.path.join(dir, PATHPRESET)
        print(presets)
        with open(presets) as f:
            data = json.load(f)

        return data
