import time

from maya import cmds


# function subtract list from list
def subtract_list(list1, list2):
    return list(set(list1) - set(list2))


# function remove duplicates from list
def remove_dup(list1):
    return list(set(list1))


# function get baricentric coordinates from 2d object don't use bounding box
def get_baricentric_coordinates(obj):
    # get all vertices
    vertices = cmds.ls(obj + ".vtx[*]", fl=True)
    # get all coordinates
    coordinates = []
    for v in vertices:
        coordinates.append(cmds.xform(v, q=True, ws=True, t=True))
    # get baricentric coordinates
    baricentric = [0, 0, 0]
    for c in coordinates:
        baricentric[0] += c[0]
        baricentric[1] += c[1]
        baricentric[2] += c[2]
    baricentric[0] /= len(coordinates)
    baricentric[1] /= len(coordinates)
    baricentric[2] /= len(coordinates)
    return baricentric

    # create simple function for take the time execute it


import time


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        return result

    return wrapper


# function will take in an list  and return of odd numbers list

def odd_numbers(list1):
    return [x for x in list1 if x % 2 != 0]


sample_list = list(range(10000000))
time_it(odd_numbers)(sample_list)

# write pyside2 window for maya with tree buttons: first button change color other buttons to red, second button change color other buttons to green, third button change color oter buttons to blue

from PySide2 import QtWidgets, QtCore, QtGui

# create maya main window
maya_window = QtWidgets.QApplication.activeWindow()

# create main window
main_window = QtWidgets.QDialog(maya_window)
main_window.setWindowTitle("Test Window")
main_window.setFixedSize(400, 400)

# create main layout
main_layout = QtWidgets.QVBoxLayout()
main_window.setLayout(main_layout)

# create tree widget
tree_widget = QtWidgets.QTreeWidget()
tree_widget.setHeaderHidden(True)
tree_widget.setRootIsDecorated(False)
main_layout.addWidget(tree_widget)

# create first button
first_button = QtWidgets.QPushButton("First Button")
main_layout.addWidget(first_button)

# create second button
second_button = QtWidgets.QPushButton("Second Button")
main_layout.addWidget(second_button)

# create third button
third_button = QtWidgets.QPushButton("Third Button")
main_layout.addWidget(third_button)

# create tree widget items
for i in range(10):
    item = QtWidgets.QTreeWidgetItem()
    item.setText(0, f"Item {i}")
    tree_widget.addTopLevelItem(item)

# create tree widget item buttons
for i in range(tree_widget.topLevelItemCount()):
    item = tree_widget.topLevelItem(i)
    # create button
    button = QtWidgets.QPushButton("Button")
    # add button to tree widget
    tree_widget.setItemWidget(item, 0, button)


# create function for change color of buttons
def change_color_of_buttons(color):
    for i in range(tree_widget.topLevelItemCount()):
        item = tree_widget.topLevelItem(i)
        button = tree_widget.itemWidget(item, 0)
        button.setStyleSheet(f"background-color:{color}")


# create function for first button
def first_button_func():
    change_color_of_buttons("red")


# create function for second button
def second_button_func():
    change_color_of_buttons("green")


# create function for third button
def third_button_func():
    change_color_of_buttons("blue")


# connect first button
first_button.clicked.connect(first_button_func)

# connect second button
second_button.clicked.connect(second_button_func)

# connect third button
third_button.clicked.connect(third_button_func)

# show window
main_window.show()

# create maya main window
maya_window = QtWidgets.QApplication.activeWindow()

# create main window
main_window = QtWidgets.QDialog(maya_window)
main_window.setWindowTitle("Test Window")
main_window.setFixedSize(400, 400)

# create main layout
