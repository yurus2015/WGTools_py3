import maya.cmds as cmds
import re, os
from importlib import reload
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

# from PySide2.QtWebKitWidgets import QWebView, QWebFrame, QWebPage, QWebElement

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
import maya.OpenMayaUI as omu
import shutil
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import fromstring
import webbrowser

from simplygon_tanks.utils.tank_bake_2019 import SUFIXES
import simplygon_tanks.widgets.line_edit
import simplygon_tanks.utils.generic as gen
import simplygon_tanks.widgets.lodSwitch
import simplygon_tanks.widgets.distanceVar

# import simplygon_tanks.widgets.helpWidget

reload(simplygon_tanks.widgets.distanceVar)
reload(simplygon_tanks.widgets.lodSwitch)
reload(simplygon_tanks.utils.generic)
reload(simplygon_tanks.widgets.line_edit)
# reload(simplygon_tanks.widgets.helpWidget)

from simplygon_tanks.widgets.line_edit import SG_LineEdit, SG_ButtonLineEdit, SG_Browser
from simplygon_tanks.widgets.lodSwitch import SG_lodSwitch
from simplygon_tanks.widgets.distanceVar import SG_lodDistance

# from simplygon_tanks.widgets.helpWidget import SG_helpImage
# from widgets.headerWidget import HeaderWidget

RANGE = 5


def mainWindowPointer():
    ptr = omu.MQtUtil.mainWindow()  # pointer for the main window
    return wrapInstance(int(ptr), QWidget)


class Simplygon_Wnd(QDialog):
    def __init__(self, parent=mainWindowPointer()):
        QDialog.__init__(self, parent)
        self.setWindowTitle("Simplygon Tanks")
        self.setModal(False)
        self.setWindowFlags(Qt.Window)

        width_ui = 500
        height_ui = 390  # 370

        self.setObjectName("SimplygonTanks")

        self.myQMenuBar = QMenuBar(self)
        self.myQMenuBar.setGeometry(0, 0, 200, 18)

        widgetAction = QAction('Help', self.myQMenuBar)
        widgetAction.triggered.connect(self.helpClicked)

        self.myQMenuBar.addAction(widgetAction)

        self.setLayout(self.directorybox())

        # script job
        self.numJob = self.scriptJob()
        self.numJobSel = self.scriptJobSelect()
        self.numJobName = self.scriptJobNameChange()
        self.checkOpenFile()

        # save position window
        self.settings = QSettings("SimplygonTanks")
        if not self.settings.value("geometry") == None:
            self.restoreGeometry(self.settings.value("geometry"))

        for widget in parent.findChildren(QDialog):
            if widget is not self:
                if widget.objectName() == self.objectName():
                    widget.close()

        self.resize(self.minimumSizeHint())

    def scriptJob(self):
        jobNum = cmds.scriptJob(e=["SceneOpened", self.checkOpenFile], p="SimplygonTanks")
        return jobNum

    def scriptJobSelect(self):
        jobNum = cmds.scriptJob(e=["SelectionChanged", self.checkOpenFile], p="SimplygonTanks")
        return jobNum

    def scriptJobNameChange(self):
        jobNum = cmds.scriptJob(e=["NameChanged", self.checkOpenFile], p="SimplygonTanks")
        return jobNum

    def checkOpenFile(self):
        a_count0, a_count1, a_count2, a_count3, cfc1, cfc2, cfc3 = 'No lod0', '-', '-', '-', '-', '-', '-'
        if gen.emptyScene():
            if gen.isTank():
                if gen.isCrash():
                    try:
                        a_count0, a_count1, a_count2, a_count3, cfc1, cfc2, cfc3 = gen.polycountCompute()
                        a_count0, a_count1, a_count2, a_count3 = int(a_count0), int(a_count1), int(a_count2), int(
                            a_count3)
                    except:
                        pass
                    self.tableWidget.item(1, 1).setText(str(a_count0))
                    self.tableWidget.item(1, 2).setText(str(a_count1))
                    self.tableWidget.item(1, 3).setText(str(a_count2))
                    self.tableWidget.item(1, 4).setText(str(a_count3))
                    self.tableWidget.item(2, 1).setText(str(a_count0))

                    tracks0, tracks1, tracks2, tracks3 = gen.checkTracksLod()
                    if tracks0:
                        self.tableWidget.item(1, 0).setText(' Tracks Crash')
                        self.rb_hierachyButton.setEnabled(True)
                    else:
                        self.tableWidget.item(1, 0).setText('Wheels Crash')
                        self.rb_hierachyButton.setEnabled(False)
                else:
                    try:
                        a_count0, a_count1, a_count2, a_count3, cfc1, cfc2, cfc3 = gen.polycountCompute()
                        a_count0, a_count1, a_count2, a_count3 = int(a_count0), int(a_count1), int(a_count2), int(
                            a_count3)
                    except:
                        pass
                    self.tableWidget.item(1, 1).setText(str(a_count0))
                    self.tableWidget.item(1, 2).setText(str(a_count1))
                    self.tableWidget.item(1, 3).setText(str(a_count2))
                    self.tableWidget.item(1, 4).setText(str(a_count3))
                    self.tableWidget.item(2, 1).setText(str(a_count0))

                    tracks0, tracks1, tracks2, tracks3 = gen.checkTracksLod()
                    if tracks0:
                        self.tableWidget.item(1, 0).setText(' Tracks Tank')
                        self.rb_hierachyButton.setEnabled(True)
                    else:
                        self.tableWidget.item(1, 0).setText('Wheels Tank')
                        self.rb_hierachyButton.setEnabled(False)
            else:
                self.tableWidget.item(1, 1).setText('-')
                self.tableWidget.item(1, 2).setText('-')
                self.tableWidget.item(1, 3).setText('-')
                self.tableWidget.item(1, 4).setText('-')

                self.tableWidget.item(2, 1).setText('Not selected')

                selected = cmds.filterExpand(sm=12)
                if selected:
                    triangles = cmds.polyEvaluate(selected, t=True)
                    self.tableWidget.item(2, 1).setText(str(triangles))
                    self.tableWidget.item(2, 2).setText('Enter value')
                    self.tableWidget.item(2, 3).setText('Enter value')
                    self.tableWidget.item(2, 4).setText('Enter value')
        else:
            self.tableWidget.item(1, 0).setText('  Auto')
            self.tableWidget.item(1, 1).setText('-')
            self.tableWidget.item(1, 2).setText('-')
            self.tableWidget.item(1, 3).setText('-')
            self.tableWidget.item(1, 4).setText('-')

            self.tableWidget.item(2, 1).setText('-')
            self.tableWidget.item(2, 2).setText('-')
            self.tableWidget.item(2, 3).setText('-')
            self.tableWidget.item(2, 4).setText('-')

    def returnManualValue(self):
        value1, value2, value3 = self.tableWidget.item(2, 2).text(), self.tableWidget.item(2,
                                                                                           3).text(), self.tableWidget.item(
            2, 4).text()
        return value1, value2, value3

    def closeEvent(self, event):
        try:
            cmds.delete('switcher')
            cmds.scriptEditorInfo(writeHistory=True)
        except:
            pass

        # restore position window
        self.settings.setValue("geometry", self.saveGeometry())

        # kill scriptJobs
        cmds.scriptJob(k=self.numJob, force=True)
        cmds.scriptJob(k=self.numJobSel, force=True)
        cmds.scriptJob(k=self.numJobName, force=True)

    def showHideDistaceLayout(self):
        if self.distAction.isChecked():
            self.setFixedSize(500, 500)
        else:
            self.setFixedSize(500, 390)

    def helpClicked(self):
        self.helpWnd = SG_helpImage()
        self.helpWnd.show()

    def tableBox(self):
        self.table_frame = QFrame()
        self.table_frame.setStyleSheet("#addElementFrame{background-white;}")
        self.table_frame.setFrameShape(QFrame.Box)
        self.table_frame.setFrameShadow(QFrame.Sunken)
        self.table_frame.setMinimumHeight(55)
        self.table_frame.setMaximumHeight(78)
        self.table_frame.setMinimumWidth(550)

        self.tableWidget = QTableWidget(3, 7)
        self.tableWidget.horizontalHeader().setVisible(0)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tableWidget.verticalHeader().setVisible(0)
        self.tableWidget.verticalHeader().setDefaultSectionSize(25)

        self.tableWidget.setMinimumWidth(550)
        self.tableWidget.setWordWrap(0)
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.setAlternatingRowColors(1)

        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableWidget.setTextElideMode(Qt.ElideNone)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setObjectName("allFormatsTable")

        table_box = QVBoxLayout()
        table_box.setSpacing(0)

        self.tableWidget.setParent(self.table_frame)
        table_box.addWidget(self.table_frame)

        brush = QBrush(QColor(200, 200, 255, 255))
        w_brush = QBrush(QColor(255, 255, 255, 255))
        g_brush = QBrush(QColor(200, 255, 200, 255))

        for row in range(1, 3):
            for col in range(1, 5):
                item = QTableWidgetItem()
                item.setText('Enter value')
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
                item.setForeground(g_brush)
                if row == 1:
                    # item.setFlags(False)
                    item.setForeground(brush)
                # if row == 2 and col == 1:
                #     item.setFlags(False)
                # item.setForeground(w_brush)
                self.tableWidget.setItem(row, col, item)

        item_l0 = QTableWidgetItem('lod0')
        item_l0.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
        item_l0.setForeground(w_brush)
        # item_l0.setFlags(0)
        self.tableWidget.setItem(0, 1, item_l0)

        item_l1 = QTableWidgetItem('lod1')
        item_l1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
        item_l1.setForeground(w_brush)
        # item_l1.setFlags(0)
        self.tableWidget.setItem(0, 2, item_l1)

        item_l2 = QTableWidgetItem('lod2')
        item_l2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
        item_l2.setForeground(w_brush)
        # item_l2.setFlags(0)
        self.tableWidget.setItem(0, 3, item_l2)

        item_l3 = QTableWidgetItem('lod3')
        item_l3.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
        item_l3.setForeground(w_brush)
        # item_l3.setFlags(0)
        self.tableWidget.setItem(0, 4, item_l3)

        item_l4 = QTableWidgetItem('lod4')
        item_l4.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
        item_l4.setForeground(w_brush)
        # item_l4.setFlags(0)
        self.tableWidget.setItem(0, 5, item_l4)

        item_bld = QTableWidgetItem('  Auto')
        item_bld.setForeground(brush)
        # item_bld.setFlags(0)
        self.tableWidget.setItem(1, 0, item_bld)

        item_manual = QTableWidgetItem('  Manual')
        item_manual.setForeground(g_brush)
        # item_manual.setFlags(0)
        self.tableWidget.setItem(2, 0, item_manual)

        item_proxy = QTableWidgetItem('  proxy')
        item_proxy.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
        # item_proxy.setFlags(0)
        self.tableWidget.setItem(1, 5, item_proxy)

        item_proxy_m = QTableWidgetItem('  proxy')
        item_proxy_m.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
        # item_proxy_m.setFlags(0)
        self.tableWidget.setItem(2, 5, item_proxy_m)

        self.r0_Widget = QWidget()
        self.r0_Layout = QHBoxLayout(self.r0_Widget)
        self.r0_Layout.setContentsMargins(0, 0, 0, 0)
        self.table0_reduceButton = QPushButton("&Reduce")
        self.table0_reduceButton.setFixedWidth(50)
        self.table0_reduceButton.setFixedHeight(20)
        self.table0_reduceButton.clicked.connect(gen.only_reduce)  # simpligon command

        self.r0_Layout.addWidget(self.table0_reduceButton, Qt.AlignHCenter | Qt.AlignVCenter)
        self.tableWidget.setCellWidget(1, 6, self.r0_Widget)

        self.r1_Widget = QWidget()
        self.r1_Layout = QHBoxLayout(self.r1_Widget)
        self.r1_Layout.setContentsMargins(0, 0, 0, 0)
        self.table1_reduceButton = QPushButton("&Reduce")
        self.table1_reduceButton.setFixedWidth(50)
        self.table1_reduceButton.setFixedHeight(20)
        self.table1_reduceButton.clicked.connect(gen.common_reduce)  # simpligon command

        self.r1_Layout.addWidget(self.table1_reduceButton)
        self.r1_Layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
        self.tableWidget.setCellWidget(2, 6, self.r1_Widget)

        return table_box

    def reducebox(self):
        self.rb_frame = QFrame()
        self.rb_frame.setStyleSheet("#addElementFrame{background-white;}")
        self.rb_frame.setFrameShape(QFrame.Box)
        self.rb_frame.setFrameShadow(QFrame.Sunken)
        self.rb_frame.setMinimumHeight(134)
        self.rb_frame.setMaximumHeight(134)

        self.rb_buttonbox = QDialogButtonBox(self)
        self.rb_buttonbox.setOrientation(Qt.Horizontal)

        self.rb_hierachyButton = QPushButton("&Lods Hierarchy")
        self.rb_proxyGenerateButton = QPushButton("&Proxy lod generate")
        self.rb_proxyLodButton = QPushButton("&Import proxy lod")
        self.rb_hierachyButton.clicked.connect(gen.create_hierarchy)
        self.rb_proxyGenerateButton.clicked.connect(gen.proxy_generate)
        self.rb_proxyLodButton.clicked.connect(gen.importProxy)

        self.rb_box = QVBoxLayout(self.rb_frame)
        self.rb_table = self.tableBox()

        self.rb_buttonbox.addButton(self.rb_hierachyButton, QDialogButtonBox.ActionRole)
        self.rb_buttonbox.addButton(self.rb_proxyGenerateButton, QDialogButtonBox.ActionRole)
        self.rb_buttonbox.addButton(self.rb_proxyLodButton, QDialogButtonBox.ActionRole)

        self.rb_box.addLayout(self.rb_table)
        self.rb_box.addWidget(self.rb_buttonbox)

        return self.rb_frame

    def directorybox(self):
        valid_filename = gen.nameCurrentFile()

        #################Simplygon Frame
        self.sg_frame = QFrame()
        self.sg_frame.setStyleSheet("#addElementFrame{background-white;}")
        self.sg_frame.setFrameShape(QFrame.Box)
        self.sg_frame.setFrameShadow(QFrame.Sunken)
        self.sg_frame.setMinimumHeight(110)
        self.sg_frame.setMaximumHeight(110)

        ############## Texture dirs Browser
        self.textureBox = SG_Browser('Texture Dir', 100, 20, 'dir')

        ############## Texture track file Browser
        self.trackBox = SG_Browser('Track Texture File', 100, 20, 'file')

        ############## switchLods
        self.switchBox = QFrame()
        self.switchBox.setStyleSheet("#addElementFrame{background-white;}")
        self.switchBox.setFrameShape(QFrame.Box)
        self.switchBox.setFrameShadow(QFrame.Sunken)
        self.switchBox.setMinimumHeight(90)
        self.switchBox.setMaximumHeight(90)

        self.switcher = SG_lodSwitch(self.switchBox)
        self.switcher.setMinimumWidth(460)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.switcher.setSizePolicy(sizePolicy)
        '''
		############## distance LOD
		self.distanceBox =  QFrame()
		self.distanceBox.setStyleSheet("#addElementFrame{background-white;}")
		self.distanceBox.setFrameShape(QFrame.Box)
		self.distanceBox.setFrameShadow(QFrame.Sunken)

		self.distWidget = SG_lodDistance(self.distanceBox)
		self.distWidget.setMinimumWidth(460)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		self.distWidget.setSizePolicy(sizePolicy)
		'''
        self.spacerItem = QSpacerItem(200, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        """
		Creates a box containing the standard Cancel and OK buttons.
		"""
        self.buttonbox = QDialogButtonBox(self)
        self.buttonbox.setOrientation(Qt.Horizontal)
        self.onlybakeButton = QPushButton("&Bake Proxy")
        self.buttonbox.addButton(self.onlybakeButton, QDialogButtonBox.ActionRole)

        for i in range(len(SUFIXES)):
            checkBox = QCheckBox(SUFIXES[i])
            checkBox.setObjectName(SUFIXES[i])
            if i < RANGE:
                checkBox.setChecked(True)
            self.buttonbox.addButton(checkBox, QDialogButtonBox.ActionRole)

        self.onlybakeButton.clicked.connect(gen.tank_bake_2019)

        ##############Main box
        main_box = QVBoxLayout()
        main_box.setSpacing(5)
        main_box.setAlignment(Qt.AlignTop)

        sg_box = QVBoxLayout(self.sg_frame)

        sg_box.addLayout(self.textureBox)
        sg_box.addLayout(self.trackBox)
        sg_box.addWidget(self.buttonbox)

        main_box.addItem(self.spacerItem)
        main_box.addWidget(self.reducebox())
        main_box.addWidget(self.sg_frame)
        main_box.addWidget(self.switchBox)
        # main_box.addWidget(self.distanceBox)
        return main_box


def createTankUI():
    ###########delete window and dialog
    if cmds.window("SimplygonTanks", q=True, exists=True):
        cmds.deleteUI("SimplygonTanks")

    try:
        cmds.deleteUI('MayaWindow|SimplygonTanks')
    except:
        pass

    try:
        dialog.close()
        dialog.deleteLater()
    except:
        # pass
        print('don`t close dialog')
    ############
    dialog = Simplygon_Wnd()
    dialog.show()
    # currentVersion = cmds.about(v=1)
    # if '2016 Extension 2' in currentVersion or '2018' in currentVersion:
    #
    # else:
    #     result = cmds.confirmDialog(title='Maya Version',
    #                                 message='Need version Maya 2016 Extension 2 (2016.5) or later\nUsing Maya 2014 for your risk',
    #                                 button=['I`m progressive man(2016)', 'I`m luddit(2014)'], defaultButton='Yes')
    #     if result == 'I`m progressive man(2016)':
    #         return
    #     else:
    #         dialog = Simplygon_Wnd()
    #         dialog.show()


def main():
    createTankUI()
