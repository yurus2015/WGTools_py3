import maya.cmds as cmds
from maya.mel import eval as meval
import maya.OpenMayaUI as omu
import os
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

from shiboken2 import wrapInstance
from PySide2.QtWebKitWidgets import QWebView, QWebPage

currentFilePath = os.path.dirname(os.path.realpath(__file__))
parentDir = currentFilePath.split('widgets')[0]


def mainWindowPointer():
    ptr = omu.MQtUtil.mainWindow()  # pointer for the main window
    return wrapInstance(long(ptr), QWidget)


class SG_helpImage(QWidget):
    def __init__(self, parent=mainWindowPointer()):
        super(SG_helpImage, self).__init__(parent)

        self.setWindowFlags(Qt.Window)
        self.setWindowTitle('Simplygon Help')
        cursorPosition = QCursor.pos()
        self.setGeometry(cursorPosition.x(), cursorPosition.y(), 605, 800)

        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout(self)  # main layout
        self.topLayout = QFrame()  # close layout
        self.topLayout.setMinimumHeight(8)
        self.topLayout.setMaximumHeight(8)
        vebWiew = QWebView()
        # url = QUrl.fromLocalFile('d:/BRANCH3/devtools/scripts/simplygon/docs/simplygon_doc.html')
        url = QUrl.fromLocalFile(parentDir + 'docs/simplygon_doc.html')
        vebWiew.setUrl(url)

        self.mainLayout.addWidget(self.topLayout)
        self.mainLayout.addWidget(vebWiew)

    def anotherSlot(self):
        self.close()
        self.deleteLater()
    # print "now I'm in Main.anotherSlot"


class ClickableLabel(QLabel):
    clicked = Signal(str)

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.setPixmap(parentDir + 'images/close_btn.png')

    def mousePressEvent(self, event):
        self.clicked.emit(self.objectName())


class Browser(QWebView):
    def __init__(self):
        QWebView.__init__(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
        self.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("border:5px; background: rgb(0, 0, 0);")
        self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.linkClicked.connect(self.test)

    @Slot(QUrl)
    def test(self, url):
        link = url.toString().encode('Windows-1251')
        webbrowser.open(link)

    def event(self, event):
        if event.type() == 11:
            self.close()
            self.deleteLater()
            return False
        return QWidget.event(self, event)


class SG_lodSwitch(QWidget):
    def __init__(self, parent=None):
        super(SG_lodSwitch, self).__init__(parent)

        self.initUI()

    def initUI(self):
        # create main layout
        self.mainLayout = QGridLayout(self)  # main layout
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.setColumnMinimumWidth(14, 5)

        self.textLaybel_01 = QLabel('All Lods')
        self.textLaybel_01.setStyleSheet("Text-align:center")
        self.textLaybel_02 = QLabel('Lods 0-3')
        self.textLaybel_02.setStyleSheet("Text-align:center")
        self.textLaybel_03 = QLabel('lod0')
        self.textLaybel_03.setStyleSheet("Text-align:center")
        self.textLaybel_04 = QLabel('lod1')
        self.textLaybel_04.setStyleSheet("Text-align:center")
        self.textLaybel_05 = QLabel('lod2')
        self.textLaybel_05.setStyleSheet("Text-align:center")
        self.textLaybel_06 = QLabel('lod3')
        self.textLaybel_06.setStyleSheet("Text-align:center")
        self.textLaybel_07 = QLabel('lod4')
        self.textLaybel_07.setStyleSheet("Text-align:right")

        self.swLods_Slider = QSlider()
        self.swLods_Slider.setRange(0, 6)
        self.swLods_Slider.setSingleStep(1)
        self.swLods_Slider.setOrientation(Qt.Horizontal)

        self.swLods_Slider.setTickPosition(QSlider.TicksAbove)
        self.swLods_Slider.setTickInterval(1)

        self.radio1 = QRadioButton("Virtual LOD")
        self.radio2 = QRadioButton("Distance LOD")

        self.radio1.toggled.connect(self.radio1_clicked)
        self.radio2.toggled.connect(self.radio2_clicked)

        self.radio1.setChecked(True)

        self.mainLayout.addWidget(self.textLaybel_01, 0, 1, 1, 2)
        self.mainLayout.addWidget(self.textLaybel_02, 0, 3, 1, 2)
        self.mainLayout.addWidget(self.textLaybel_03, 0, 5, 1, 2)
        self.mainLayout.addWidget(self.textLaybel_04, 0, 7, 1, 2)
        self.mainLayout.addWidget(self.textLaybel_05, 0, 9, 1, 2)
        self.mainLayout.addWidget(self.textLaybel_06, 0, 11, 1, 2)
        self.mainLayout.addWidget(self.textLaybel_07, 0, 13, 1, 2)

        self.mainLayout.setAlignment(self.textLaybel_01, Qt.AlignHCenter)
        self.mainLayout.setAlignment(self.textLaybel_02, Qt.AlignHCenter)
        self.mainLayout.setAlignment(self.textLaybel_03, Qt.AlignHCenter)
        self.mainLayout.setAlignment(self.textLaybel_04, Qt.AlignHCenter)
        self.mainLayout.setAlignment(self.textLaybel_05, Qt.AlignHCenter)
        self.mainLayout.setAlignment(self.textLaybel_06, Qt.AlignHCenter)
        self.mainLayout.setAlignment(self.textLaybel_07, Qt.AlignHCenter)

        self.mainLayout.addWidget(self.swLods_Slider, 1, 2, 1, 12)

        self.mainLayout.addWidget(self.radio1, 2, 2, 1, 5)
        self.mainLayout.addWidget(self.radio2, 2, 5, 1, 5)

        self.mainLayout.setAlignment(self.radio1, Qt.AlignLeft)

        # connect
        self.swLods_Slider.valueChanged.connect(self.switchLods)

    def changeConturView(self, state):
        if state == Qt.Checked:
            # print 'Execute script'-displayAppearance smoothShaded
            panel = cmds.getPanel(typ='modelPanel')
            for p in panel:
                cmds.modelEditor(p, e=1, dl="active", displayAppearance='smoothShaded')
        else:
            # print 'Set defoult light'
            panel = cmds.getPanel(typ='modelPanel')
            for p in panel:
                cmds.modelEditor(p, e=1, dl="default")

    def switchLodsColorLabel(self, value):
        # print 'Value', value
        allLabelsLod = (
            self.textLaybel_01, self.textLaybel_02, self.textLaybel_03, self.textLaybel_04, self.textLaybel_05,
            self.textLaybel_06, self.textLaybel_07)
        for index in range(len(allLabelsLod)):
            if index == value:
                allLabelsLod[index].setStyleSheet("color: rgb(80, 200, 0)")
            else:
                allLabelsLod[index].setStyleSheet("color: rgb(200, 200, 200)")

    def switchLodsVisible(self, show, hide):
        for u in show:
            try:
                cmds.setAttr(u + '.visibility', 1)

            except:
                pass

        for h in hide:
            try:
                cmds.setAttr(h + '.visibility', 0)
            except:
                pass

    def switchLods(self):
        self.lods = ['lod0', 'lod1', 'lod2', 'lod3', 'lod4']
        self.value = self.swLods_Slider.value()
        self.switchLodsColorLabel(self.value)
        if self.value == 0:
            self.switchLodsVisible(self.lods, [])

        if self.value == 1:
            self.switchLodsVisible(self.lods[:4], self.lods[4:])
        for index in range(2, 7):
            if self.value == index:
                self.switchLodsVisible(self.lods[index - 2:index - 1], self.lods[:index - 2] + self.lods[index - 1:])

    def radio1_clicked(self, enabled):
        if enabled:
            try:
                cmds.delete('switcher')
                self.swLods_Slider.setEnabled(True)
                cmds.scriptJob(kill=self.sliderScriptJob, force=True)
            except:
                pass

    def radio2_clicked(self, enabled):
        if enabled:
            if not cmds.objExists('switcher'):
                self.lod_switcher = cmds.createNode('lodGroup', n='switcher')
            else:
                self.lod_switcher = 'lod_switcher'
                cmds.select(self.lod_switcher)
            meval('doHideInOutliner 1;')
            cmds.connectAttr('perspShape.worldMatrix[0]', self.lod_switcher + '.cameraMatrix', f=1)
            cmds.connectAttr(self.lod_switcher + '.output[0]', 'lod0.visibility', f=1)
            cmds.connectAttr(self.lod_switcher + '.output[1]', 'lod1.visibility', f=1)
            cmds.connectAttr(self.lod_switcher + '.output[2]', 'lod2.visibility', f=1)
            cmds.connectAttr(self.lod_switcher + '.output[3]', 'lod3.visibility', f=1)
            cmds.connectAttr(self.lod_switcher + '.output[4]', 'lod4.visibility', f=1)

            cmds.setAttr(self.lod_switcher + '.threshold[0]', cmds.optionVar(q='distance_lod_0'))
            cmds.setAttr(self.lod_switcher + '.threshold[1]', cmds.optionVar(q='distance_lod_1'))
            cmds.setAttr(self.lod_switcher + '.threshold[2]', cmds.optionVar(q='distance_lod_2'))
            cmds.setAttr(self.lod_switcher + '.threshold[3]', cmds.optionVar(q='distance_lod_3'))

            self.swLods_Slider.setEnabled(False)
            self.moveSlider()

            self.sliderScriptJob = cmds.scriptJob(attributeChange=[self.lod_switcher + '.activeLevel', self.moveSlider],
                                                  p='Simplygon', rp=1)

    def moveSlider(self):
        level = cmds.getAttr(self.lod_switcher + '.activeLevel')
        self.swLods_Slider.setValue(level + 2)

    def deleteLodNode(self):
        try:
            cmds.delete('switcher')
        # print 'NODE'
        except:
            pass
