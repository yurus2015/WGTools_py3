# from style_catalog.gui.style_window import*
import maya.cmds as cmds
import style_catalog.gui.style_window as sw
reload(sw)


def main():
    if cmds.window('StyleCatalogWindow', q=True, exists=True):
        cmds.deleteUI('StyleCatalogWindow')

    window = sw.CatalogWindow()
    window.show()
    print(window.objectName())


if __name__ == '__main__':
    # cmds.scriptEditorInfo(ch=True)
    print('Catalog1_')
    main()
