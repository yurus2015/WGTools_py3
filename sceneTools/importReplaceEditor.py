from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import shiboken2
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omu
import maya.cmds as cmds
import os, posixpath


def mainWindowPointer():
    ptr = omu.MQtUtil.mainWindow()  # pointer for the main window
    return wrapInstance(int(ptr), QWidget)


class Utils(object):
    @classmethod
    def maya_scene_name(cls):
        rawFilePath = cmds.file(q=True, exn=True)
        pathName = posixpath.split(rawFilePath)
        if pathName:
            return pathName[0], pathName[1]
        else:
            return '', ''

    @classmethod
    def deleteReference(cls):
        for ref in cmds.ls(references=True):
            try:
                cmds.file(unloadReference=ref)
            except:
                pass
        for ref in cmds.ls(references=True):
            try:
                cmds.file(rr=1, f=1, referenceNode=ref)
            except:
                pass

        cls.withoutMaterial()

    @classmethod
    def withoutMaterial(cls):
        emptyShading = []
        meshes = cmds.ls(o=1, s=1)
        meshes = cmds.filterExpand(meshes, sm=12)
        if meshes:
            meshes = cmds.listRelatives(meshes, s=True, f=1)
            for m in meshes:
                shader = cmds.listConnections(m, type='shadingEngine')
                if not shader:
                    emptyShading.append(m)

        emptyShading = cmds.listRelatives(emptyShading, p=True, f=1)
        cls.objectsWithoutMaterialsUtil(emptyShading)
        cmds.select(d=1)

    @classmethod
    def objectsWithoutMaterialsUtil(cls, meshes):
        if meshes:
            for i in meshes:
                if "gun" in i or "Gun" in i:
                    cls.correctMat(i, "tank_guns")
                elif "turret" in i or "Turret" in i:
                    cls.correctMat(i, "tank_turret_01")
                elif "hull" in i or "Hull" in i:
                    cls.correctMat(i, "tank_hull_01")
                elif "track_L" in i or "Track_L" in i:
                    cls.correctMat(i, "track_mat_L")
                elif "track_R" in i or "Track_R" in i:
                    cls.correctMat(i, "track_mat_R")
                elif "chassis" in i or "Chassis" in i or "w_" in i or "W_" in i or "wd_" in i or "Wd_" in i:
                    cls.correctMat(i, "tank_chassis_01")
        return []

    @classmethod
    def correctMat(cls, obj, matName):
        existingMatList = cmds.ls(mat=1)
        correctMatName = matName

        if obj.find("turret") != -1 or obj.find("Turret") != -1:
            num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            if obj[-1] in num:
                correctMatName = correctMatName.replace(correctMatName[-1], obj[-1])

        if correctMatName in existingMatList:
            # if material exists
            cmds.select(obj)
            cmds.hyperShade(assign=correctMatName)
        else:
            # create new material and assign it
            newMat = cmds.shadingNode('lambert', n=correctMatName, asShader=1)
            cmds.select(obj)
            cmds.hyperShade(assign=newMat)

    @classmethod
    def visibleReferenceObjects(cls):
        meshes = cmds.ls('*:*', o=1, s=1)
        for m in meshes:
            cmds.setAttr(m + '.visibility', 0)

    @classmethod
    def referenceLoadUnload(cls, file):
        path, file_short = cls.maya_scene_name()
        cls.deleteReference()
        if file_short in file:
            cmds.confirmDialog(title='Warning', message='Current file opened', button=['   OK   '],
                               defaultButton='   OK   ')
        else:
            cmds.file(file, reference=True, namespace='r')
            filters = cmds.itemFilter(bn=('*:*'), neg=1)
            cmds.outlinerEditor('outlinerPanel1', e=1, showReferenceNodes=False, showReferenceMembers=False,
                                filter=filters)
        cls.visibleReferenceObjects()

    @classmethod
    def importAction(cls):
        sel = cmds.ls(sl=1)
        if sel:
            new = cmds.duplicate(sel)
            new = cmds.ls(new, l=1)
            meshes = cmds.listRelatives(new, ad=1, s=1, f=1)
            for m in meshes:
                cmds.setAttr(m + '.visibility', 1)
            try:
                cmds.parent(w=1)
            except:
                pass
        else:
            cmds.confirmDialog(title='Warning', message='Select object(s) from left panel', button=['   OK   '],
                               defaultButton='   OK   ')

    @classmethod
    def replaceAction(cls):
        pair = cmds.filterExpand(fp=1, sm=12)
        if len(pair) == 2:
            if 'r:' in pair[0] and 'r:' not in pair[1]:
                cmds.connectAttr(pair[0] + '.outMesh', pair[1] + '.inMesh',
                                 f=1)  # -f r:gun_02_Shape.outMesh gun_02_Shape.inMesh;
        else:
            cmds.confirmDialog(title='Warning', message='Select one object from left panel and one from right panel',
                               button=['   OK   '], defaultButton='   OK   ')

    @classmethod
    def two_up_folder(cls, file):
        two_up = os.path.abspath(os.path.join(file, "../.."))
        return two_up

    @classmethod
    def source_folder(cls, two_up_folder, folder_name):
        srs_folder = None
        for root, dirs, files in os.walk(two_up_folder):
            for name in dirs:
                if name == folder_name:
                    print((os.path.join(root, name)))
                    srs_folder = os.path.join(root, name)
                    break
        if srs_folder:
            return srs_folder
        else:
            cmds.confirmDialog(title='Warning', message='Directory ' + folder_name + ' doesn`t exist',
                               button=['   OK   '], defaultButton='   OK   ')
            cmds.error()

    @classmethod
    def source_file(cls, source_folder, file_name):
        srs_file = None
        for root, dirs, files in os.walk(source_folder):
            for name in files:
                if name == file_name:
                    print((os.path.join(root, name)))
                    srs_file = os.path.join(root, name)
                    break
        if srs_file:
            return srs_file
        else:
            cmds.confirmDialog(title='Warning', message='File ' + source_folder + '/' + file_name + ' doesn`t exist',
                               button=['   OK   '], defaultButton='   OK   ')
            cmds.error()

    @classmethod
    def silent_mode_load(cls, source_file):
        cls.deleteReference()
        cmds.file(source_file, reference=True, namespace='r')

    @classmethod
    def silent_mode_selection(cls):
        # selected = cmds.listRelatives(cmds.filterExpand(fp=1, sm=12), p=1, pa=1)
        selected = cmds.ls(sl=1, l=1, tr=1)
        if selected:
            return selected
        else:
            cmds.confirmDialog(title='Warning', message='Select some mesh(es)', button=['   OK   '],
                               defaultButton='   OK   ')
            cmds.error()

    @classmethod
    def silent_mode_references(cls, item):
        reference = item.replace("|", "|r:")

        if not cmds.objExists(reference):
            cmds.confirmDialog(title='Warning', message='Object ' + item + ' doesn`t exist in source file', \
                               button=[' OK '], defaultButton='   OK   ')
            return

        reference = cmds.ls(reference, l=1)[0]
        return reference

    @classmethod
    def silent_mode_connect(cls, ref, item):
        cmds.connectAttr(ref + '.outMesh', item + '.inMesh', f=1)

    @classmethod
    def silent_mode_parenting(cls, item, child):
        parent = cmds.listRelatives(item, p=1, f=1)
        cmds.delete(item)
        if parent:
            cmds.parent(child, parent)
        else:
            cmds.rename(child, item)

    @classmethod
    def silent_mode_layer(cls, item):
        display_layer = cmds.listConnections(item, type="displayLayer")
        if display_layer:
            return display_layer[0]
        else:
            return None

    @classmethod
    def silent_mode_duplicate(cls, ref):
        cmds.select(ref)
        duplicate_ref = cmds.duplicate(rr=1, un=1)
        duplicate_ref = cmds.ls(sl=1, l=1)
        return duplicate_ref

    @classmethod
    def silent_mode_unskinned(cls, duplicate):
        try:
            cmds.skinCluster(duplicate, e=1, ub=1)
            cmds.delete('nodes_01')
        except:
            pass

    @classmethod
    def silent_mode_clear(cls):
        try:
            cmds.delete('nodes_01')
        except:
            pass

    @classmethod
    def silent_mode_replace(cls, ref, item, layer):
        duplicate_ref = cls.silent_mode_duplicate(ref)
        cls.silent_mode_unskinned(duplicate_ref)
        # cls.silent_mode_clear()
        if layer:
            cmds.editDisplayLayerMembers(layer, duplicate_ref)

        cls.silent_mode_parenting(item, duplicate_ref)

    @classmethod
    def silent_mode(cls, source_folder_name):
        selection = cls.silent_mode_selection()

        current_file_path = cmds.file(q=True, exn=True)
        if not os.path.isfile(current_file_path):
            cmds.confirmDialog(title='Warning', message='Save file before', button=['   OK   '],
                               defaultButton='   OK   ')
            cmds.error()

        if source_folder_name in current_file_path:
            cmds.confirmDialog(title='Warning', message='The open file is in the ' + source_folder_name + ' directory ',
                               button=['   OK   '], defaultButton='   OK   ')
            cmds.error()

        upper_folders = cls.two_up_folder(current_file_path)
        srs_folder = cls.source_folder(upper_folders, source_folder_name)
        current_file_name = posixpath.split(current_file_path)[1]
        srs_file = cls.source_file(srs_folder, current_file_name)
        cls.silent_mode_load(srs_file)

        for item in selection:
            ref = cls.silent_mode_references(item)
            layer = cls.silent_mode_layer(item)
            if ref:
                cls.silent_mode_replace(ref, item, layer)

        cls.deleteReference()


class ImportReplace_Wnd(QDialog):
    def __init__(self, parent=mainWindowPointer()):
        QDialog.__init__(self, parent)

        self.setWindowTitle("Import/Replace")
        self.setModal(False)
        self.setMinimumWidth(360)
        self.setMinimumHeight(500)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setObjectName("ImportReplaceObject")

        self.browserLine()
        self.filesList()
        self.buttons()
        self.layouts()

        # save position window
        self.settings = QtCore.QSettings("ImportReplaceObject")
        if not self.settings.value("geometry") == None:
            self.restoreGeometry(self.settings.value("geometry"))

    def browserLine(self):
        self.directory_lbl = QLabel("Dir")
        self.lineEdit = QLineEdit()
        self.select_dir_btn = self.initButton(command=lambda: self.dirBrowser(), icon=":fileOpen.png", w=42, h=20)
        self.select_dir_btn.setToolTip("Select directory with files")

    def filesList(self):
        path, file = Utils.maya_scene_name()
        filter_file = []
        self.lineEdit.setText(path)

        self.model = QFileSystemModel()
        self.model.setRootPath(path)
        self.model.setFilter(QtCore.QDir.Files)
        for entry in os.listdir(path):
            print('Entity', entry)
            if entry != file and '.mb' in entry:
                print('ADDD', file, entry)
                filter_file.append(entry)
        print('Filter', filter_file)
        # if not filter_file:
        # 	filter_file.append('')
        self.model.setNameFilters(filter_file)
        self.model.setNameFilterDisables(False)

        # ListView
        self.ls = QListView(self)
        self.ls.setModel(self.model)
        self.ls.setRootIndex(self.model.setRootPath(path))
        self.ls.setMaximumHeight(100)
        self.selModel = self.ls.selectionModel()

        self.ls.clicked.connect(self.onclick)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setObjectName('outLayout')

        cmds.setParent('outLayout')
        paneLayoutName_1 = cmds.paneLayout()
        panel_1 = cmds.outlinerPanel()
        outliner_1 = cmds.outlinerPanel(panel_1, query=True, outlinerEditor=True)
        cmds.outlinerEditor(outliner_1, edit=True, mainListConnection='worldList', selectionConnection='modelList',
                            showShapes=False, showReferenceNodes=False, showReferenceMembers=False,
                            showAttributes=False, showConnected=False, showAnimCurvesOnly=False, autoExpand=False,
                            showDagOnly=True, ignoreDagHierarchy=False, expandConnections=False, showNamespace=True,
                            showCompounds=True, showNumericAttrsOnly=False, highlightActive=True,
                            autoSelectNewObjects=False, doNotSelectNewObjects=False, transmitFilters=False,
                            showSetMembers=False, setFilter='defaultSetFilter', ignoreHiddenAttribute=False,
                            ignoreOutlinerColor=False)
        filters = cmds.itemFilter(bn=('*:*'))
        cmds.outlinerEditor(outliner_1, e=1, filter=filters)

        ptr = omu.MQtUtil.findControl(panel_1)
        paneLayoutQt_1 = shiboken2.wrapInstance(int(ptr), QtWidgets.QWidget)

        cmds.setParent('outLayout')
        paneLayoutName_2 = cmds.paneLayout()
        panel_2 = cmds.outlinerPanel()
        outliner_2 = cmds.outlinerPanel(panel_2, query=True, outlinerEditor=True)
        cmds.outlinerEditor(outliner_2, edit=True, mainListConnection='worldList', selectionConnection='modelList',
                            showShapes=False, showReferenceNodes=False, showReferenceMembers=False,
                            showAttributes=False, showConnected=False, showAnimCurvesOnly=False, autoExpand=False,
                            showDagOnly=True, ignoreDagHierarchy=False, expandConnections=False, showNamespace=True,
                            showCompounds=True, showNumericAttrsOnly=False, highlightActive=True,
                            autoSelectNewObjects=False, doNotSelectNewObjects=False, transmitFilters=False,
                            showSetMembers=False, setFilter='defaultSetFilter', ignoreHiddenAttribute=False,
                            ignoreOutlinerColor=False)
        mesh = cmds.itemFilter(byType='mesh')
        difFilter = cmds.itemFilter(difference=(mesh, filters))
        cmds.outlinerEditor(outliner_2, e=1, filter=difFilter)

        ptr = omu.MQtUtil.findControl(panel_2)
        paneLayoutQt_2 = shiboken2.wrapInstance(int(ptr), QtWidgets.QWidget)

        self.splitter.addWidget(paneLayoutQt_1)
        self.splitter.addWidget(paneLayoutQt_2)

    def buttons(self):
        self.import_btn = self.initButton(title='Import', command=lambda: Utils.importAction(), h=20)
        self.import_btn.setToolTip("Import selected")
        self.replace_btn = self.initButton(title='Replace', command=lambda: Utils.replaceAction(), h=20)
        self.replace_btn.setToolTip("Replace selected from left panel to right panel")

    def initButton(self, parent=None, title="", command=None, icon=None, w=None, h=None):
        self._button = QPushButton(title)
        if command:
            self._button.clicked.connect(command)
        if icon:
            self._button.setIcon(QIcon(icon))
        if w:
            self._button.setMinimumWidth(w)
            self._button.setMaximumWidth(w)
        if h:
            self._button.setMinimumHeight(h)
            self._button.setMaximumHeight(h)
        return self._button

    def dirBrowser(self):  # open browser to set export path
        bpath = None
        try:
            bpath = cmds.fileDialog2(fm=3, dialogStyle=1)[0]
        except:
            pass

        if bpath:
            self.lineEdit.setText(bpath)
            self.ls.setRootIndex(self.model.setRootPath(bpath))
        else:
            cmds.confirmDialog(title='Warning', message='Select dir with *.mb files', button=['   OK   '],
                               defaultButton='   OK   ')

    def layouts(self):
        main_layout = QVBoxLayout(self)

        browser_layout = QHBoxLayout(self)
        browser_layout.addWidget(self.directory_lbl)
        browser_layout.addWidget(self.lineEdit)
        browser_layout.addWidget(self.select_dir_btn)

        treeLayout = QVBoxLayout(self)
        treeLayout.addWidget(self.ls)
        treeLayout.addWidget(self.splitter)

        buttonLayout = QHBoxLayout(self)
        buttonLayout.addWidget(self.import_btn)
        buttonLayout.addWidget(self.replace_btn)

        main_layout.addLayout(browser_layout)
        main_layout.addLayout(treeLayout)
        main_layout.addLayout(buttonLayout)

    def onclick(self, index):
        item = self.selModel.selection().indexes()[0]
        path = self.lineEdit.text()
        path = path + '/' + item.data()
        Utils.referenceLoadUnload(path)

    def closeEvent(self, event):
        # restore position window
        self.settings.setValue("geometry", self.saveGeometry())
        Utils.deleteReference()

    def scriptJob(self):
        cmds.scriptJob(uid=["ImportReplaceObject", lambda: Utils.deleteReference()])


def main():
    if cmds.window("ImportReplaceObject", q=True, exists=True):
        cmds.deleteUI("ImportReplaceObject")
    try:
        cmds.deleteUI('MayaWindow|ImportReplaceObject')
    except:
        pass

    try:
        dialog = ImportReplace_Wnd()
        dialog.close()
    except:
        pass

    dialog = ImportReplace_Wnd()
    dialog.show()
