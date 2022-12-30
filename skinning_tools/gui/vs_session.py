from PySide2.QtCore import QRectF
from PySide2.QtGui import QColor

from skinning_tools.gui.viewport.vs_scene import VSScene, GraphicsScene

from skinning_tools.gui.viewport.vs_context_menu import ContextMenuMain


class Session:
    active_tool = 'create_node'
    active_transform = 'translate'

    scene_width = 50000
    scene_height = 50000
    scene_left = GraphicsScene()
    scene_left.set_graphics_scene(scene_width, scene_height)

    scene_right = GraphicsScene()
    scene_right.set_graphics_scene(scene_width, scene_height)

    context_menu = ContextMenuMain()
    # context_menu.set_scene(scene)

    min_zoom = 0.1
    max_zoom = 4.0
    zoom_clamp = True


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
        # self.scene_width = 50000
        # self.scene_height = 50000
        # self.scene = GraphicsScene()
        # self.scene.set_graphics_scene(self.scene_width, self.scene_height)

        # Mouse settings
        self.min_zoom = 0.1
        self.max_zoom = 2.5
        self.zoom_clamp = True

        # Keyboard settings

        # context menu
        # self.context_menu = None

    # def add_item(self, item):
    #     self.scene.addItem(item)
    #
    # def context_menu_init(self):
    #     # Context menu
    #     self.context_menu = ContextMenuMain()
    #     self.add_item(self.context_menu)
