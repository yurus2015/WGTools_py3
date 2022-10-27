import importlib
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.cmds as cmds
import objects_tools.utils as utl
import objects_tools.export as export

importlib.reload(utl)
importlib.reload(export)

# todo refactory array icon
style = """
QPushButton {
    background-color: rgb(90, 90, 90);
    border-style: solid;
    border-width: 1px;
    border-radius: 3px;
    border-color: rgb(120, 120, 180);
    min-width: 3em;
    padding: 0px;
    width: 60px;
    transition: all 400ms;
}

QPushButton#exportChooseButton{
    qproperty-icon: url("d:/Development/WG/DevTools2022/scripts/py3/objects_tools/ui/images/arrow.png");
}

QPushButton:hover {
    background-color: rgb(50,50,50); 
}

QPushButton#havocComingSoonButton{
    width: 100%
}
"""

link_style = """
QPushButton#linkButtonStyle {
    background-color: transparent; 
    border: 0px;
    border-radius: 4px;
    text-align: left;
}

QPushButton#linkButtonStyle:hover {
    background-color: #4772b3; 
}


"""

link_style_preselect = """
QPushButton#linkButtonStyle {
    background-color: transparent; 
    border: 0px;
    border-radius: 4px;
    text-align: left;
}

QPushButton#linkButtonStyle:hover {
    background-color: #4772b3; 
}

QPushButton#linkButtonStyle:focus {
    background-color: #4772b3;
}

"""

expand_style = """
QPushButton#exportChooseButton {
    background-color: rgb(90, 90, 90);
    border-style: solid;
    border-width: 1px;
    border-radius: 3px;
    border-color: rgb(120, 120, 180);
    min-width: 3em;
    padding: 0px;
    width: 60px;
    transition: all 400ms;
    }

QPushButton#exportChooseButton {
    qproperty-icon: url("d:/Development/WG/DevTools2022/scripts/py3/objects_tools/ui/images/arrow_down.png");
}

QPushButton:hover#exportChooseButton {
    background-color: rgb(50,50,50); 
    }
"""

icon_style = """
QPushButton#objectsDeleteButton {
    image: url("d:/Development/WG/DevTools2022/scripts/py3/objects_tools/ui/images/delete.png");
    background-color: transparent; 
    border: 0px;
    width: 20px;
}

QPushButton#objectsDeleteButton:hover {
    image:url(d:/Temporary/Delmenextday/delete.png); 
    border:none
}
"""

toggle_style = """
QPushButton#toggleGroupBoxButton{
    background-color: transparent; 
    font-size: 16px;
    border: 0px;
    text-align: center;
}

QPushButton#toggleGroupBoxButton:hover{
    background-color : rgb(82, 133, 166);
}
"""

label_style = """
QLabel:hover {
    background-color : rgb(82, 133, 166);
}
"""


class ObjectsCentralWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.central_layout = QVBoxLayout()
        self.setLayout(self.central_layout)

        # custom frame blocks
        self.export_block = ObjectsExportingFrame()
        self.havok_block = ObjectsHavokFrame()
        vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.central_layout.addWidget(self.export_block)
        self.central_layout.addWidget(self.havok_block)
        self.central_layout.addItem(vertical_spacer)


class ObjectsFrame(QGroupBox):
    def __init__(self):
        QGroupBox.__init__(self)
        self.setStyleSheet("QGroupBox {border: 1px solid #8C8C8C;margin-top: 0.5em;} "
                           "QGroupBox::title {top: -8px;left: 18px;}")

        self.toggle_button = QPushButton(self)
        self.toggle_button.setGeometry(QRect(20, 0, 10, 10))
        self.toggle_button.setObjectName('toggleGroupBoxButton')
        self.toggle_button.setText('+')
        self.toggle_button.setStyleSheet(toggle_style)
        self.toggle_button.clicked.connect(self.toggle_visible_block)

    def toggle_visible_block(self):
        print('Toggle')


class ObjectsHavokFrame(ObjectsFrame):
    def __init__(self, *args):
        super().__init__()
        self.setTitle('    Havok Tools')
        main_export_layout = QVBoxLayout()
        main_export_layout.setAlignment(Qt.AlignTop)
        self.setLayout(main_export_layout)

        combobox_layout = QHBoxLayout()
        combobox_layout.setContentsMargins(0, 0, 0, 0)
        # todo in separate class?
        self.trank_combobox = QComboBox()
        self.trank_combobox.setFixedHeight(22)
        self.trank_combobox.setObjectName('customTrankCombo')
        # self.trank_combobox.currentIndexChanged.connect(self.save_current_path)

        self.paths = utl.Utils.load_option_var()
        print('Paths ', self.paths)
        current_branch = cmds.optionVar(q='current_branch')
        if self.paths:
            for i in range(len(self.paths)):
                self.trank_combobox.addItem(self.paths[i])
                if current_branch == self.paths[i]:
                    self.trank_combobox.setCurrentIndex(i)

        self.directory_button = ObjectsButton('Dir')
        self.directory_button.set_width(42)
        self.directory_button.clicked.connect(self.export_browser)
        # self.buttonDir = self.init_button(command=lambda: self.dir_browser())
        # self.directory_button.setStyleSheet("QPushButton {border:0px; background: rgb(0, 0, 0, 0);}")

        # combobox_layout.addWidget(self.trank_combobox)
        # combobox_layout.addWidget(self.directory_button)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignLeft)
        main_export_layout.addLayout(combobox_layout)
        main_export_layout.addLayout(buttons_layout)

        self.export_button = ObjectsButton('Coming soon')
        # self.export_button.set_width(60)
        self.export_button.clicked.connect(self.save_current_path)
        self.export_button.setObjectName('havocComingSoonButton')
        buttons_layout.addWidget(self.export_button)

    def save_current_path(self):
        utl.Utils.confirm_console('If you want...', False, True)
        print('save')

    def export_browser(self):  # open browser to set export path
        export_path = None
        try:
            export_path = cmds.fileDialog2(fm=3, dialogStyle=1)[0]
        except ValueError:
            pass

        if not export_path:
            return
        print('_______!!!!!!!!!!_____', self.paths)
        if export_path and 'content' in export_path:
            if export_path not in self.paths:
                self.trank_combobox.addItem(export_path)
                self.trank_combobox.setCurrentIndex(self.trank_combobox.count() - 1)
                self.paths.append(export_path)
                utl.Utils.save_option_var(export_path, delete=False)
        else:
            cmds.confirmDialog(title='Warning', message='Select "content*" dir in your branch',
                               button=['   OK   '], defaultButton='   OK   ')


class ObjectsExportingFrame(ObjectsFrame):
    def __init__(self, *args):
        super().__init__()
        self.setTitle('    Export ')
        main_export_layout = QVBoxLayout()
        main_export_layout.setAlignment(Qt.AlignTop)
        main_export_layout.setSpacing(0)
        self.setLayout(main_export_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.setMargin(0)
        buttons_layout.setSpacing(2)

        self.something_button = ObjectsButton('Set for export "content" directory')
        self.something_button.setMinimumWidth(60)
        self.something_button.clicked.connect(self.toggle_view_list)
        self.something_button.setObjectName('exportChooseButton')

        dir_button = ObjectsButton('...')
        dir_button.setFixedSize(50, 20)
        dir_button.clicked.connect(self.browser)

        buttons_layout.addWidget(self.something_button)
        buttons_layout.addWidget(dir_button)

        export_button_layout = QHBoxLayout()
        export_button_layout.setAlignment(Qt.AlignLeft)
        export_button_layout.setContentsMargins(0, 10, 0, 0)
        export_button_layout.setSpacing(0)

        export_button = ObjectsButton('Export')
        export_button.setFixedSize(90, 20)
        export_button.clicked.connect(self.do_export)
        export_button_layout.addWidget(export_button)
        main_export_layout.addLayout(buttons_layout)

        self.widgets_list = ObjectsListWidget()
        self.widgets_list.setVisible(False)

        main_export_layout.addWidget(self.widgets_list)
        main_export_layout.addLayout(export_button_layout)

        self.load_links_option()

    def items_list_widget(self):
        widgets = []
        for x in range(self.widgets_list.count()):
            item = self.widgets_list.item(x)
            widgets.append(self.widgets_list.itemWidget(item))
        return widgets

    def toggle_view_list(self):
        self.widgets_list.setVisible(not self.widgets_list.isVisible())
        self.something_button.setStyleSheet(style)
        if self.widgets_list.isVisible():
            self.something_button.setStyleSheet(expand_style)
            link_widget = self.items_list_widget()
            button_text = self.get_link_on_button()
            for lw in link_widget:
                if lw.get_link() == button_text:
                    lw.set_active_button()
                    return

    def browser(self):
        self.path_link = utl.Utils.browser_path()
        if self.path_link:
            if 'content' not in self.path_link:
                utl.Utils.confirm_console('Not correct path!\nPath should include "content" folder', False, True)
                answer = utl.Utils.confirm_dialog('Do you want to export to this directory?')
                print('ANS', answer)
                if answer != 'Ok':
                    return
            self.set_link_on_button(self.path_link)
            # check the same path
            if utl.Utils.same_link(self.path_link):
                return
            self.add_link_item(self.path_link)
            utl.Utils.save_option_var(self.path_link)

    def add_link_item(self, link):
        item = QListWidgetItem(self.widgets_list)
        item.setSizeHint(QSize(400, 24))
        custom_widget_item = ObjectsLinkWidget(self, item, link)
        self.widgets_list.setItemWidget(item, custom_widget_item)

    def set_link_on_button(self, link):
        self.something_button.setText(link)

    def get_link_on_button(self):
        return self.something_button.text()

    def load_links_option(self):
        links = utl.Utils.load_option_var()
        if links:
            for link in links:
                # check exists path
                if utl.Utils.path_exists(link):
                    self.add_link_item(link)
                else:
                    # remove invalid path from optionVar
                    utl.Utils.save_option_var(link, delete=True)
                utl.Utils.confirm_console('Test', True, False)

                self.set_link_on_button(links[-1])

    def do_export(self):
        link = self.get_link_on_button()
        export.main(link)


class ObjectsListWidget(QListWidget):
    def __init__(self):
        QListWidget.__init__(self)

    def enterEvent(self, event):
        self.raise_()
        for x in range(self.count()):
            item = self.item(x)
            link_widget = self.itemWidget(item)
            link_button = link_widget.get_link_button()
            link_button.setStyleSheet(link_style)


class ObjectsButton(QPushButton):
    def __init__(self, name=None):
        QPushButton.__init__(self)
        self.setFixedHeight(20)
        self.setText(name)
        self.setStyleSheet(style)

    def set_width(self, width=40):
        self.setFixedWidth(width)


class ObjectsLinkButton(ObjectsButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet(link_style)


class ObjectsLabel(QLabel):
    def __init__(self, text):
        QLabel.__init__(self)
        self.setText(text)
        # setting background color to label when mouse hover over it
        self.setStyleSheet(label_style)


class ObjectsLinkWidget(QWidget):
    def __init__(self, parent, item, link=None):
        QWidget.__init__(self)
        self.item = item
        self.link = link
        self.parent_widget = parent
        self.palette = self.palette()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)

        link_layout = QHBoxLayout()
        check_layout = QHBoxLayout()
        check_layout.setAlignment(Qt.AlignRight)

        self.label = ObjectsLinkButton(self.link)
        self.label.setObjectName("linkButtonStyle")
        self.label.clicked.connect(self.press_button_link)

        label_check = QLabel('Path not exists')
        delete_button = ObjectsButton()
        delete_button.setFixedSize(20, 20)
        delete_button.setObjectName('objectsDeleteButton')
        delete_button.clicked.connect(self.remove_item)
        delete_button.setStyleSheet(icon_style)

        self.setLayout(layout)
        layout.addLayout(link_layout)
        link_layout.addWidget(delete_button)
        link_layout.addWidget(self.label, 0)

    def get_list_widget(self):
        self.list_widget = self.parent().parent()
        return self.list_widget

    def press_button_link(self):
        self.parent_widget.toggle_view_list()
        self.parent_widget.set_link_on_button(self.get_link())

    def clear_list(self):
        print(self.parent().parent().clear())

    def remove_item(self):
        print(self.item)
        self.list_widget = self.get_list_widget()
        self.list_widget.takeItem(self.list_widget.row(self.item))
        utl.Utils.save_option_var(self.link, delete=True)
        print(self.list_widget.count())
        if self.parent_widget.get_link_on_button() == self.link:
            self.parent_widget.set_link_on_button('Set for export "content" directory')

    def get_link(self):
        return self.link

    def set_active_button(self):
        self.label.setFocus()
        self.label.setStyleSheet(link_style_preselect)

    def get_link_button(self):
        return self.label
