from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import os
import importlib
import modelingToolset.lib.uvChecker.utils.util as Util
importlib.reload(Util)
current_dir = os.path.dirname(os.path.abspath(__file__))


class ButtonIcon(QPushButton):
    def __init__(self, icon, text, parent=None):
        super(ButtonIcon, self).__init__()
        self.icon = icon
        self.text = text
        self.parent = parent
        self.grid = None

        self.setFixedSize(50, 50)
        self.setText(self.text)

        if self.icon:
            self.icon_image = self.icon + '.png'
            self.icon_path = os.path.join(current_dir, 'icons', self.icon_image)
            self._icon = QIcon(self.icon_path)
            self.setIcon(self._icon)
            self.setIconSize(QSize(50, 50))

    def set_grid(self, grid):
        self.grid = grid

    def get_icon(self):
        return self.icon


class ButtonAdd(ButtonIcon):
    def __init__(self, *args):
        super().__init__(*args)
        self.clicked.connect(self.adding_button)

    def adding_button(self):
        self.grid.adding_item()
        # Util.assign_checker_texture()


class ButtonCamouflage(ButtonIcon):
    def __init__(self, *args):
        super().__init__(*args)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.button_right_clicked)
        self.pop_menu = QMenu()
        self.clicked.connect(self.assign_texture)

    def path_texture(self):
        texture_name = self.get_icon()
        texture_path = os.path.join(current_dir, 'textures', texture_name) + '.tga'
        return texture_path

    def assign_texture(self):
        tile = self.path_texture()
        Util.assign_checker_texture(tile=tile)

    # context menu
    def button_right_clicked(self, QPos):
        button = self.sender()
        parent_position = button.mapToGlobal(QPoint(0, 0))
        menu_position = parent_position + QPos
        self.pop_menu.clear()
        self.context_menu()
        self.pop_menu.move(menu_position)
        self.pop_menu.show()

    def context_menu(self):
        delete_action = QAction('Remove', self)
        delete_action.triggered.connect(self.remove_button)
        set_action = QAction('Set...', self)
        set_action.triggered.connect(self.set_icon)
        self.pop_menu.addAction(set_action)
        self.pop_menu.addAction(delete_action)

    def remove_button(self):
        self.setParent(None)
        self.deleteLater()
        self.grid.reformat_items()
        self.grid.save_yaml()

    def set_icon(self):
        visible_icons = self.grid.all_camouflage_buttons()
        texture = Util.set_path(current_dir)
        icon = os.path.basename(texture)
        self.icon = os.path.splitext(icon)[0]
        self.icon_png = self.icon + '.png'

        icon_path = os.path.join(current_dir, 'icons', self.icon_png)
        if not os.path.exists(icon_path):
            Util.change_image_size(texture, icon_path)

        if self.icon in visible_icons:
            print('exist', self.icon, ' in ', visible_icons)
            return
            # todo confirm dialog

        cam_icon = QIcon(icon_path)
        self.setIcon(cam_icon)
        self.setIconSize(QSize(50, 50))

        self.grid.save_yaml()
