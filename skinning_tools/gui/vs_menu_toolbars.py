from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from skinning_tools.gui.vs_constants import MENU_ACTIONS
from skinning_tools.gui.vs_constants import TOOLBAR_TOOLS, TOOLBAR_SYSTEM, TOOLBAR_ITEMS


# create class menu bar
class VSMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super(VSMenuBar, self).__init__(parent)
        self.setObjectName('VSMenuBar')
        self.main_window = parent
        self.create_ui()

    # todo refactor
    def create_ui(self):
        # for each menu action create menu
        for menu_name, menu_actions in MENU_ACTIONS.items():
            menu = self.addMenu(menu_name)
            menu.setTearOffEnabled(True)
            for action_name, action in menu_actions.items():
                # create action
                action = QAction(action_name, self)
                # add action to menu
                menu.addAction(action)
            # # connect action to function
            # action.triggered.connect(action['function'])
            # # add shortcut
            # if 'shortcut' in action:
            #     action.setShortcut(action['shortcut'])
            # # add icon
            # if 'icon' in action:
            #     action.setIcon(QIcon(action['icon']))
            # # add checkable
            # if 'checkable' in action:
            #     action.setCheckable(action['checkable'])
            # # add checked
            # if 'checked' in action:
            #     action.setChecked(action['checked'])
            # # add enabled
            # if 'enabled' in action:
            #     action.setEnabled(action['enabled'])
            # # add tooltip
            # if 'tooltip' in action:
            #     action.setToolTip(action['tooltip'])
            # # add status tip
            # if 'status_tip' in action:
            #     action.setStatusTip(action['status_tip'])
            # # add data
            # if 'data' in action:
            #     action.setData(action['data'])
            # # add menu
            # if 'menu' in action:
            #     action.setMenu(action['menu'])
            # # add separator
            # if 'separator' in action:
            #     menu.addSeparator()
            # # add widget
            # if 'widget' in action:
            #     menu.addWidget(action['widget'])
            # # add action
            # if 'action' in action:
            #     menu.addAction(action['action'])


class VSToolBar(QToolBar):
    def __init__(self, parent=None):
        super(VSToolBar, self).__init__(parent)
        self.main_window = parent
        self.setMovable(True)
        self.setFloatable(True)


# create main tool bar class
class VSToolBarTools(VSToolBar):
    def __init__(self):
        super(VSToolBarTools, self).__init__()
        # add actions to tool bar
        for tool in TOOLBAR_TOOLS:
            self.addAction(tool)


class VSToolBarSystem(VSToolBar):
    def __init__(self):
        super(VSToolBarSystem, self).__init__()
        # add actions to tool bar
        for tool in TOOLBAR_SYSTEM:
            self.addAction(tool)


class VSToolBarItems(VSToolBar):
    def __init__(self):
        super(VSToolBarItems, self).__init__()
        # add actions to tool bar
        for tool in TOOLBAR_ITEMS:
            self.addAction(tool)
