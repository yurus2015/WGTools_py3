import json
from .constants import PATHJSON
import os

dir = os.path.dirname(__file__)


class DataJson():
    def __init__(self):
        pass

    @classmethod
    def read_json(cls):
        widgets = os.path.join(dir, PATHJSON)
        with open(widgets) as f:
            data = json.load(f)

        return data
