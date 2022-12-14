from PySide2.QtGui import QColor

from skinning_tools.gui.viewport.vs_scene import VSScene, GraphicsScene


class Serializable:
    def __init__(self):
        self.id = id(self)

    # def id(self):
    def serialize(self):
        raise NotImplemented()

    def deserialize(self, data, hashmap={}):
        raise NotImplemented()


class Scene(Serializable):

    def __init__(self):
        super(Scene, self).__init__()
        # self.nodes = []
        self.scene_width = 50000
        self.scene_height = 50000
        self.scene = GraphicsScene()
        self.scene.set_graphics_scene(self.scene_width, self.scene_height)

        # Mouse settings
        self.min_zoom = 0.1
        self.max_zoom = 2.5
        self.zoom_clamp = True
