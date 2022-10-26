# -*- coding: utf-8 -*-
import maya.OpenMayaUI as omu
import maya.cmds as cmds
import os
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import style_catalog.utils.utilites as utl
reload(utl)
import resource

X_CATALOG = r'\\by1-wdstor-01.corp.wargaming.local\WOT_art_photogrammetry\Tanks_3DSt\Catalog'

def get_window_pointer():
    # Get and return Maya Main window pointer
    main_window_ptr = omu.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(long(main_window_ptr), QWidget)

    return maya_main_window


class CatalogWindow(QDialog):
    def __init__(self):
        super(CatalogWindow, self).__init__()

        self.setParent(get_window_pointer())
        self.setWindowFlags(Qt.Window)
        self.setObjectName('StyleCatalogWindow')
        self.setWindowTitle('Catalog Tools')
        self.init_ui()

        self.save_position_window()

    def init_ui(self):
        self.central_layout = QVBoxLayout()
        self.central_layout.setSpacing(10)
        self.central_layout.setContentsMargins(10, 15, 10, 15)
        self.central_layout.setAlignment(Qt.AlignTop)

        # Group boxes
        self.tool_box = CatalogGroupBox(title='Tools')
        self.material_box = CatalogGroupBox(title='Textures')
        self.export_box = CatalogGroupBox(title='Export')
        self.render_box = CatalogGroupBox(title='Render')

        self.info_line = QLineEdit()
        self.info_line.setEnabled(False)
        self.info_line.setText('Info line')
        self.info_line.setStyleSheet("color: yellow;")
        utl.Settings.info_line = self.info_line

        # Vertical Layouts
        # textures
        self.textures_layout = CatalogVerticalLayout()
        self.export_layout = CatalogExportWidget()

        # Horizontal Layout
        self.tools_layout = CatalogHorizontalLayout()
        self.render_layout = CatalogHorizontalLayout()

        # Buttons not custom widget
        # tools
        self.detach_button = CatalogButton('Detach', utl.detach_command)
        self.align_face_button = CatalogButton('Align Face', utl.set_align_tool)
        self.tools_help_button = CatalogButton(width=20, icon=':help.svg',
                                               cmd=lambda: self.clicked_help('Tools', utl.Settings.tools_help))
        self.material_help_button = CatalogButton(width=20, icon=':help.svg',
                                               cmd=lambda: self.clicked_help('Textures and Material', utl.Settings.material_help))
        self.render_help_button = CatalogButton(width=20, icon=':help.svg',
                                                  cmd=lambda: self.clicked_help('Render',
                                                                                utl.Settings.render_help))

        # material
        self.assign_button = CatalogButton('Create/Assign Material', utl.material_command)

        # render
        self.gate_button = CatalogButton(width=20, icon=':gate.svg', checkable=True, cmd=utl.shading_mode)
        self.render_button = CatalogButton('Render', utl.render_command)
        self.chain_button = CatalogButton(width=20, icon=':chain.svg', checkable=True, cmd=utl.button_chain_state)
        self.photoshop_button = CatalogButton('Send to PS', utl.photoshop_command)

        # Custom widgets
        # material
        self.texture_albedo = CatalogTextureBrowser(label='Albedo', map_type='AM')
        self.texture_normal = CatalogTextureBrowser(label='Normal', map_type='NM')

        self.texture_albedo.set_widget(self.texture_normal)
        self.texture_normal.set_widget(self.texture_albedo)


        # export
        self.export_broser_path = CatalogExportPath()

        # Parenting layouts to groupbox
        self.tool_box.setLayout(self.tools_layout)
        self.render_box.setLayout(self.render_layout)
        self.material_box.setLayout(self.textures_layout)
        self.export_box.setLayout(self.export_layout)

        # Parenting buttons to layouts
        # tools
        self.tools_layout.addWidget(self.detach_button)
        self.tools_layout.addWidget(self.align_face_button)
        self.tools_layout.addWidget(self.tools_help_button)

        # render
        self.render_layout.addWidget(self.gate_button)
        self.render_layout.addWidget(self.render_button)
        self.render_layout.addWidget(self.chain_button)
        self.render_layout.addWidget(self.photoshop_button)
        self.render_layout.addWidget(self.render_help_button)

        # Parenting custom widgets to layout
        # materials
        self.textures_layout.addWidget(self.material_help_button, alignment=Qt.AlignRight)
        self.textures_layout.addLayout(self.texture_albedo)
        self.textures_layout.addLayout(self.texture_normal)
        self.textures_layout.addWidget(self.assign_button)

        self.setLayout(self.central_layout)

        self.central_layout.addWidget(self.tool_box)
        self.central_layout.addWidget(self.material_box)
        self.central_layout.addWidget(self.export_box)
        self.central_layout.addWidget(self.render_box)
        self.central_layout.addWidget(self.info_line)

        self.export_layout.export_path_check()

    def clicked_check(self):
        if self.newobject_checkbox.isChecked():
            self.export_broser_path.change_text_button('Name object')
        else:
            self.export_broser_path.change_text_button('Existing object name')

    def clicked_help(self, title, message):
        help_box = CatalogHelpBox(title, message)
        return help_box.exec_()

    def save_position_window(self):
        self.settings = QSettings('StyleCatalogWindow')
        if self.settings.value('geometry') is not None:
            self.restoreGeometry(self.settings.value('geometry'))

    def closeEvent(self, event):
        self.settings.setValue('geometry', self.saveGeometry())

    def export_path_check(self):
        if os.path.exists(X_CATALOG):
            self.new_export_layout.set_line_text(X_CATALOG)
            utl.Settings.export_path = X_CATALOG
        else:
            self.new_export_layout.line.setStyleSheet("color: red;")
            self.new_export_layout.set_line_text('Network catalog not found')
            print('X: disk not attached. Set any directory')


class CatalogHelpBox(QMessageBox):
    def __init__(self, title=None, message=None):
        super(CatalogHelpBox, self).__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.setDefaultButton(QMessageBox.Ok)


class CatalogExportWidget(QVBoxLayout):
    def __init__(self, parent=None):
        super(CatalogExportWidget, self).__init__(parent)
        self.setSpacing(5)
        self.setContentsMargins(5, 0, 5, 10)

        # check box and help button
        self.cb_layout = CatalogHorizontalLayout()
        self.cb_layout.setContentsMargins(2, 5, 0, 0)
        self.object_checkbox = QCheckBox('Create new object')  # todo separate class
        self.object_checkbox.toggled.connect(self.check_box_action)
        self.help_button = CatalogButton(width=20, icon=':help.svg',
                                        cmd=lambda: self.clicked_help('Export', utl.Settings.export_help))
        self.cb_layout.addWidget(self.object_checkbox)
        self.cb_layout.addWidget(self.help_button, alignment=Qt.AlignRight)

        # name
        self.name_layout = CatalogHorizontalLayout()
        self.name_layout.setContentsMargins(0, 0, 0, 0)
        self.name_line = QLineEdit()
        self.name_line.setEnabled(False)
        self.name_line.textChanged.connect(self.change_name)
        self.name_label = QLabel('Name object')
        self.name_label.setMinimumWidth(75)

        self.name_layout.addWidget(self.name_line)
        self.name_layout.addWidget(self.name_label, alignment=Qt.AlignRight)

        # browser
        self.browser_layout = CatalogHorizontalLayout()
        self.browser_layout.setContentsMargins(0, 0, 0, 0)
        self.line = QLineEdit()
        self.line.setMinimumWidth(200)
        self.line.setReadOnly(True)
        self.line.setEnabled(True)

        self.browser_button = QPushButton('Existing object path')
        self.browser_button.setFixedHeight(21)
        self.browser_button.clicked.connect(self.set_export_dir)

        self.browser_layout.addWidget(self.line)
        self.browser_layout.addWidget(self.browser_button)

        # export button
        self.export_button = QPushButton('Export FBX/MB')
        self.export_button.clicked.connect(self.export_command)

        self.addLayout(self.cb_layout)
        self.addLayout(self.name_layout)
        self.addLayout(self.browser_layout)
        self.addWidget(self.export_button)

    def check_box_action(self):
        if self.object_checkbox.isChecked():
            self.name_line.setEnabled(True)
            self.name_line.setFocus()
            self.browser_button.setText('Set any dir')
        else:
            self.name_line.setEnabled(False)
            self.browser_button.setText('Existing object name')

    def set_export_dir(self):
        open_directories = None
        if os.path.exists(self.line.text()):
            open_directories = self.line.text()
        root = QFileDialog.getExistingDirectory(None, 'Pick Export Folder', open_directories)
        if root:
            self.line.setText(root)
            if not self.object_checkbox.isChecked():
                dirs = root.rsplit('/', 1)[0]
                name = root.rsplit('/', 1)[1]
                self.name_line.setText(name)
                self.line.setText(dirs)
                utl.Settings.name_object = name
                utl.Settings.export_path = dirs

    def clicked_help(self, title, message):
        help_box = CatalogHelpBox(title, message)
        return help_box.exec_()

    def export_path_check(self):
        if os.path.exists(X_CATALOG):
            self.line.setText(X_CATALOG)
            utl.Settings.export_path = X_CATALOG

    def change_name(self):
        utl.Settings.name_object = self.name_line.text()

    def export_command(self):
        utl.load_fbx_plugin()
        path = self.line.text()
        utl.export_command(path)


class CatalogGroupBox(QGroupBox):
    def __init__(self, parent=None, title=None):
        super(CatalogGroupBox, self).__init__(parent, title)
        self.setTitle(title)
        self.setStyleSheet("QGroupBox {border: 1px solid #8C8C8C;margin-top: 0.5em;} QGroupBox::title {top: -8px;left: 18px;}")


class CatalogVerticalLayout(QVBoxLayout):
    def __init__(self, parent=None):
        super(CatalogVerticalLayout, self).__init__(parent)
        self.setSpacing(3)
        self.setContentsMargins(5, 10, 5, 5)


class CatalogHorizontalLayout(QHBoxLayout):
    def __init__(self, parent=None):
        super(CatalogHorizontalLayout, self).__init__(parent)
        self.setSpacing(3)
        self.setContentsMargins(5, 10, 5, 5)


class CatalogButton(QPushButton):
    def __init__(self, label=None, cmd=None, icon=None, width=None, checkable=False, *args, **kwargs):
        super(CatalogButton, self).__init__(*args, **kwargs)
        self.execute_command = cmd
        self.setText(label)
        self.setFixedHeight(20)
        self.setCheckable(checkable)
        if width:
            self.setFixedWidth(width)
        if cmd:
            self.clicked.connect(self.command)
        if icon:
            ic = QPixmap(icon)
            self.setIcon(ic)

    def command(self):
        print('Press', self.execute_command)
        try:
            self.execute_command(self)
            print('Run')
        except:
            self.execute_command()
            print('nonself')

    def set_command(self, cmd):
        self.execute_command = cmd

    def change_text(self):
        utl.Settings.name_object = self.text()


class CatalogExportPath(QHBoxLayout):
    def __init__(self, parent=None):
        super(CatalogExportPath, self).__init__(parent)

        self.line = QLineEdit()
        self.line.setMinimumWidth(200)
        self.line.setReadOnly(True)
        self.line.setEnabled(False)

        self.browser_button = QPushButton('Existing object name')
        self.browser_button.setFixedHeight(21)
        self.browser_button.clicked.connect(self.set_export_dir)

        self.addWidget(self.line)
        self.addWidget(self.browser_button)

    def set_export_dir(self):
        pass

    def change_text_button(self, text):
        self.browser_button.setText(text)


class CatalogTextureBrowser(QHBoxLayout):
    def __init__(self, parent=None, label=None, map_type='AM'):
        super(CatalogTextureBrowser, self).__init__(parent)
        self.setSpacing(3)
        self.setContentsMargins(0, 0, 0, 0)

        self.label = label
        self.suffix = map_type
        self.anti_suffix = None
        self.widget_line = None
        self.width = 30
        self.height = 20

        self.line = QLineEdit()
        self.line.setObjectName('Line_'+self.suffix)
        self.line.setMinimumWidth(200)
        self.line.setReadOnly(True)
        self.line.setEnabled(False)
        self.line.textChanged.connect(self.edit_settings)

        self.button = QPushButton(self.label)
        self.button.setMinimumWidth(self.width)
        self.button.setMaximumHeight(self.height)
        self.button.clicked.connect(self.button_command)

        self.addWidget(self.line)
        self.addWidget(self.button)

    def button_command(self):
        maya_file = cmds.file(q=True, loc=True)
        file_path = os.path.dirname(maya_file)
        file_name = QFileDialog.getOpenFileName(None, 'Choose Texture', file_path, 'Image Files (*.tga)',
                                               options=QFileDialog.DontResolveSymlinks | QFileDialog.ReadOnly)

        if os.path.isfile(file_name[0]):
            texture_path = str(file_name[0])
            if self.suffix == 'AM':
                self.anti_suffix = 'NM'
            else:
                self.anti_suffix = 'AM'

            if self.suffix in texture_path:
                self.line.setText(texture_path)
                anti_path = self.set_second_path(texture_path, self.anti_suffix)
                self.widget_line.setText(anti_path)
                utl.Settings.info_line.setText('OK')
            else:
                utl.Settings.info_line.setText('WARNING: Select correct file - ' + self.suffix)

    def set_widget(self, widget):
        self.widget_line = widget.line

    def set_second_path(self, texture_path, second_suffix):
        second_path = texture_path.replace('_' + self.suffix, '_' + second_suffix)
        return second_path

    def edit_settings(self):
        if self.suffix == 'AM':
            utl.Settings.albedo_map = self.line.text()
        else:
            utl.Settings.normal_map = self.line.text()
