from .utils import Utils
from .gui import *


def run():
	menu_name = "Wargaming"

	# get menubar pointer
	menu_bar = Utils.getMenuPanel()

	# cleanup menubar from wargamingMenu_3.0
	Utils.cleanUpMenu(namesList=[menu_name])

	# create menu
	wg_menu = createCMenu(menu_bar, menu_name)

	# move menu previous position
	Utils.moveMenuPosition(wg_menu)
