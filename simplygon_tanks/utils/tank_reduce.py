import maya.cmds as cmds
import maya.mel
from maya.mel import eval as meval
import re, os, traceback
# import validator.resources.validator_API as vl
import math
# import generic as gen
import getpass
import subprocess


def confirmDialog(text, do):
    result = cmds.confirmDialog(title='Tank Simplygon', message=text, button=['   OK   '], defaultButton='   OK   ')
    if do == 'err':
        raise ValueError()


class Utils(object):
    def __inti__(self):
        pass

    @classmethod
    def groupCheckAndCreate(cls, path=None):
        pathHierarchy = []
        newPath = ""
        if path:
            pathHierarchy = path.split("|")[1:]
        for idx, i in enumerate(pathHierarchy):
            path = newPath + "|" + i
            if cmds.objExists(path):
                newPath = path
            else:
                newObj = cmds.group(n=i, empty=1)
                if idx != 0: cmds.parent(newObj, newPath)
                newPath = path

        return newPath

    @classmethod
    def checkType(cls, obj):
        result = None
        if isinstance(obj, (list, tuple)):
            result = "list"
        else:
            if cmds.listRelatives(obj, c=1, f=1, type="transform"):
                result = "group"
            elif cmds.listRelatives(obj, c=1, f=1, type="mesh"):
                result = "mesh"

        return result

    @classmethod
    def clearTextures(cls):
        materialNode = cmds.ls(mat=1)
        nodeMaterialStruct = {}
        for node in materialNode:
            connectedAttrs = cmds.listConnections(node, d=0, s=1, c=1)
            if connectedAttrs:
                connectedAttrs = connectedAttrs[::2]
                for attr in connectedAttrs:
                    plugAttr = cmds.connectionInfo(attr, sfd=True)
                    nodeMaterialStruct[attr] = plugAttr

        if nodeMaterialStruct:
            for i in nodeMaterialStruct:
                cmds.disconnectAttr(nodeMaterialStruct[i], i)
        return nodeMaterialStruct

    @classmethod
    def reAssignTextures(cls, nodeMaterialStruct=None):
        if not nodeMaterialStruct: return
        for i in nodeMaterialStruct:
            cmds.connectAttr(nodeMaterialStruct[i], i)


class AutoSimplygon(object):
    def __init__(self, selection=None, coeffs=None, proxy=None):
        self.inititalSelection = []
        if selection:
            self.inititalSelection = selection
        self.coeff_count = coeffs
        self.simplygonData = []

        self.prepareData()

        try:
            print('ON SIMPLYGON CLIENT')
            self.on_offServer('on')
        except:
            print('SIMPLYGON CLIENT NOT LOAD')

        if not proxy:
            self.runSimplygon()

        self.runSimplygonProxy()

        try:
            print('OFF SIMPLYGON CLIENT')
            self.on_offServer('off')
        except:
            print('SIMPLYGON CLIENT NOT EXIT')

        try:
            self.setPivotLod4()
        except:
            print('LOD4 trable')

        try:
            cmds.delete('Simplygon*')
        except:
            pass

        try:
            cmds.delete('tank_proxy*')
        except:
            pass

        mayaFileName = cmds.file(q=True, sn=1, shn=1)

        if '_crash' in mayaFileName.lower():
            try:
                self.assignDefoultshaders()
            except:
                pass

            self.transferCrashData()  # transfer UVs from origs to crush
        else:  # not crash
            try:
                lod4shader = cmds.shadingNode("blinn", asShader=True, n='tank_proxy')
                lod4 = cmds.ls('lod4', tr=1)
                cmds.select(lod4)
                cmds.hyperShade(assign=lod4shader)
            except:
                pass

        self.autoMapLayout()

    def melCmdReduce(self, coeffs):
        lod_count = 3

        cmd = 'SimplygonSecurity -su "user" -sp "user";\n'
        cmd += 'SPL -Clear;\n'
        cmd += 'SPL -CreateObject SPL tankReductionSPL;\n'  # sampleReductionSPL Create SPL script

        cmd_reduction = ''
        cmd_processor = ''
        cmd_node = ''
        cmd_write = ''
        # reduction Settings
        for index in range(lod_count):
            cmd_reduction += 'SPL -CreateObject ReductionSettings reductionSettings_lod' + str(index) + ';\n'
            cmd_reduction += 'SPL -SetValue reductionSettings_lod' + str(index) + ' TriangleRatio ' + str(
                coeffs[index]) + '\n'
            cmd_reduction += '-SetValue reductionSettings_lod' + str(index) + ' Enabled true;\n'

            # reduction Processor
            cmd_processor += 'SPL -CreateObject ReductionProcessor reductionProcessor_lod' + str(index) + ';\n'
            cmd_processor += 'SPL -SetValue reductionProcessor_lod' + str(
                index) + ' ReductionSettings reductionSettings_lod' + str(index) + ';\n'

            # process Node
            cmd_node += 'SPL -CreateObject ProcessNode processNode_lod' + str(index) + ';\n'
            cmd_node += 'SPL -SetString processNode_lod' + str(index) + ' Name processNode_lod' + str(index) + '\n'
            cmd_node += '-SetValue processNode_lod' + str(index) + ' DefaultTBNType SG_TANGENTSPACEMETHOD_ORTHONORMAL\n'
            cmd_node += '-SetValue processNode_lod' + str(index) + ' Processor reductionProcessor_lod' + str(
                index) + ';\n'

            # write Node
            cmd_write += 'SPL -CreateObject WriteNode writeNode_lod' + str(index) + ';\n'
            cmd_write += 'SPL -SetString writeNode_lod' + str(index) + ' Format ssf\n'
            cmd_write += '-SetString writeNode_lod' + str(index) + ' Name writeNode_lod' + str(index) + ';\n'
        # cmd_write += '-AddObject processNode Children writeNode;\n'

        # add children
        children = 'SPL -AddObject processNode_lod0 Children writeNode_lod0\n'
        children += '-AddObject processNode_lod0 Children processNode_lod1\n'
        children += '-AddObject processNode_lod1 Children writeNode_lod1\n'
        children += '-AddObject processNode_lod1 Children processNode_lod2\n'
        children += '-AddObject processNode_lod2 Children writeNode_lod2;\n'

        cmd_container = 'SPL -CreateObject ContainerNode containerNode;\n'
        cmd_container += 'SPL -SetString containerNode Name containerNode\n'
        cmd_container += '-AddObject containerNode Children processNode_lod0;\n'

        # parent node to script
        cmd_graph = 'SPL -SetValue tankReductionSPL ProcessGraph containerNode;\n'
        cmd_execute = 'Simplygon -b -spl "tankReductionSPL";'
        cmd += cmd_reduction + cmd_processor + cmd_node + cmd_write + children + cmd_container + cmd_graph + cmd_execute

        return cmd

    def melCmdProxy(self):
        cmd = 'SimplygonSecurity -su "user" -sp "user";\n'
        cmd += 'SPL -Clear;\n'
        cmd += 'SPL -CreateObject SPL tankProxySPL;\n'  # sampleReductionSPL Create SPL script

        # proxy
        proxy_reduction = 'SPL -CreateObject RemeshingSettings proxy_lod;\n'
        proxy_reduction += 'SPL -SetValue proxy_lod OnScreenSize 20\n'
        proxy_reduction += '-SetValue proxy_lod SurfaceTransferMode SG_SURFACETRANSFER_ACCURATE\n'
        proxy_reduction += '-SetValue proxy_lod MaxTriangleSize 32\n'
        proxy_reduction += '-SetValue proxy_lod MergeDistance 4\n'
        proxy_reduction += '-SetValue proxy_lod Enabled true;\n'

        proxy_map = 'SPL -CreateObject MappingImageSettings mapping_proxy;\n'
        proxy_map += 'SPL -SetValue mapping_proxy GenerateTexCoords true\n'
        proxy_map += '-SetValue mapping_proxy Enabled true;\n'

        proxy_processor = 'SPL -CreateObject RemeshingProcessor remeshingProcessor_proxy;\n'
        proxy_processor += 'SPL -SetValue remeshingProcessor_proxy RemeshingSettings proxy_lod\n'
        proxy_processor += '-SetValue remeshingProcessor_proxy  MappingImageSettings mapping_proxy;\n'

        proxy_node = 'SPL -CreateObject ProcessNode processNode_proxy;\n'
        proxy_node += 'SPL -SetString processNode_proxy Name processNode_proxy\n'
        proxy_node += '-SetValue processNode_proxy DefaultTBNType SG_TANGENTSPACEMETHOD_ORTHONORMAL\n'
        proxy_node += '-SetValue processNode_proxy Processor remeshingProcessor_proxy;\n'

        proxy_write = 'SPL -CreateObject WriteNode writeNode_proxy;\n'
        proxy_write += 'SPL -SetString writeNode_proxy Format ssf\n'
        proxy_write += '-SetString writeNode_proxy Name writeNode_proxy;\n'

        proxy = proxy_reduction + proxy_map + proxy_processor + proxy_node + proxy_write

        # add children
        children = 'SPL -AddObject processNode_proxy Children writeNode_proxy;\n'

        # container node (add process node to container node)
        cmd_container = 'SPL -CreateObject ContainerNode containerNode;\n'
        cmd_container += 'SPL -SetString containerNode Name containerNode\n'
        cmd_container += '-AddObject containerNode Children processNode_proxy;\n'

        # parent node to script
        cmd_graph = 'SPL -SetValue tankProxySPL ProcessGraph containerNode;\n'
        cmd_execute = 'Simplygon -b -spl "tankProxySPL";'
        cmd += proxy + children + cmd_container + cmd_graph + cmd_execute

        return cmd

    def assignDefoultshaders(self):  # need for lod4 in crash
        lod4 = cmds.ls('lod4', tr=1)
        lod4_transform = cmds.listRelatives(lod4[0], c=1, typ='transform')
        materials = ["tank_chassis_01", "tank_guns", "tank_hull_01", "tank_hull_02", "tank_turret_01", "tank_turret_02",
                     "tank_turret_03"]
        for transform in lod4_transform:
            long_transform = cmds.ls(transform, l=1)
            cmds.select(long_transform)
            for mat in materials:
                if str(transform) in mat:
                    cmds.hyperShade(assign=mat)

            if 'gun' in transform:
                cmds.hyperShade(assign="tank_guns")

    def transferCrashData(self):
        print("Transfering UV data")
        lod0 = cmds.ls("lod0", tr=1)[0]
        lod0_relatives = cmds.listRelatives(lod0, c=1, f=1)

        lod4 = cmds.ls("lod4", tr=1)[0]
        lod4_relatives = cmds.listRelatives(cmds.listRelatives(lod4, c=1, f=1, ad=1, type="mesh"), p=1, f=1,
                                            type="transform")

        for i in lod4_relatives:
            # case 1
            if "gun" in i.lower() or "turret" in i.lower() or "hull" in i.lower():
                for j in lod0_relatives:
                    if i.lower().split("|")[-1] in j.lower():
                        # check j is a group or a mesh
                        if cmds.listRelatives(j, c=1, type="mesh"):
                            # select original mesh + lod4 mesh
                            cmds.select(j)  # lod0
                            cmds.select(i, add=1)  # lod4
                            # transfer attributes
                            cmds.transferAttributes(transferPositions=0, \
                                                    transferNormals=0, \
                                                    transferUVs=2, \
                                                    transferColors=0, \
                                                    sampleSpace=0, \
                                                    sourceUvSpace="map1", \
                                                    targetUvSpace="map1", \
                                                    searchMethod=3, \
                                                    flipUVs=0, \
                                                    colorBorders=1)
                            cmds.delete(ch=1)

                        else:
                            # group
                            # do combine  -- !!!! HULL if has one mesh in group
                            original_relatives = cmds.ls(cmds.listRelatives(j, c=1, type="transform", f=1),
                                                         l=1)  # list of relatives of the group
                            combined = None

                            if len(original_relatives) > 1:
                                cmds.select(j)
                                copy = cmds.ls(cmds.duplicate(n="copy", rr=1), l=1)
                                combined = cmds.ls(cmds.polyUnite(copy, n="combinedMesh", ch=0), l=1)[0]
                                cmds.delete(ch=1)
                            else:
                                combined = original_relatives[0]

                            # select combined mesh + lod4 mesh
                            cmds.select(combined)  # combined
                            cmds.select(i, add=1)  # lod4

                            # transfer attributes
                            cmds.transferAttributes(transferPositions=0, \
                                                    transferNormals=0, \
                                                    transferUVs=2, \
                                                    transferColors=0, \
                                                    sampleSpace=0, \
                                                    sourceUvSpace="map1", \
                                                    targetUvSpace="map1", \
                                                    searchMethod=3, \
                                                    flipUVs=0, \
                                                    colorBorders=1)

                            cmds.delete(ch=1)

                            # delete combined mesh
                            if len(original_relatives) > 1:
                                cmds.delete(combined)

            elif "chassis" in i.lower():  # i = lod4
                # get relatives (children)
                lod0_chassis = [x for x in lod0_relatives if "chassis" in x.lower()]
                lod0_chassisRelatives = cmds.ls(cmds.listRelatives(lod0_chassis, f=1, c=1), l=1)

                # for RIGHT side
                originals = []
                if "_R" in i:
                    originals.extend([x for x in lod0_chassisRelatives if "_R" in x])

                elif "_L" in i:
                    originals.extend([x for x in lod0_chassisRelatives if "_L" in x])

                # select everything that has _R / _L
                cmds.select(originals)
                copy = cmds.ls(cmds.duplicate(n="copy"), l=1)
                cmds.delete(ch=1)

                # combine selection and delete history from resulted mesh
                combined = None
                if len(copy) > 1:
                    combined = cmds.ls(cmds.polyUnite(copy, n="combinedMesh", ch=0), l=1)[0]
                    cmds.delete(ch=1)
                else:
                    combined = copy[0]

                cmds.select(combined)  # combined
                cmds.select(i, add=1)  # lod4

                # do transfer attributes
                cmds.transferAttributes(transferPositions=0, \
                                        transferNormals=0, \
                                        transferUVs=2, \
                                        transferColors=0, \
                                        sampleSpace=0, \
                                        sourceUvSpace="map1", \
                                        targetUvSpace="map1", \
                                        searchMethod=3, \
                                        flipUVs=0, \
                                        colorBorders=1)

                # delete combined mesh
                cmds.delete(ch=1)
                cmds.delete(combined)

    def prepareData(self):
        allMeshes = cmds.ls(type="mesh", l=1)
        if len(self.inititalSelection) == 1:
            if cmds.listRelatives(self.inititalSelection[0], type="transform"):
                if "chassis" in self.inititalSelection[0]:
                    chassis_rels = cmds.listRelatives(self.inititalSelection[0], c=1, type="transform", f=1)
                    chassis_L = []
                    chassis_R = []
                    for j in chassis_rels:
                        if "_L" in j:
                            chassis_L.append(j)
                        elif "_R" in j:
                            chassis_R.append(j)
                    if chassis_L: self.simplygonData.append(chassis_L)
                    if chassis_R: self.simplygonData.append(chassis_R)
                    print('chassis ', chassis_L, chassis_R)
                else:
                    self.simplygonData.append(self.inititalSelection[0])
            else:
                self.simplygonData.append(self.inititalSelection[0])

        elif len(self.inititalSelection) > 1:
            for i in self.inititalSelection:
                if cmds.listRelatives(i, c=1, type="transform"):
                    if "chassis" in i:
                        chassis_rels = cmds.listRelatives(i, c=1, type="transform", f=1)
                        chassis_L = []
                        chassis_R = []
                        for j in chassis_rels:
                            if "_L" in j:
                                chassis_L.append(j)
                            elif "_R" in j:
                                chassis_R.append(j)
                        if chassis_L: self.simplygonData.append(chassis_L)
                        if chassis_R: self.simplygonData.append(chassis_R)
                    else:
                        self.simplygonData.append(self.inititalSelection[0])
                else:
                    self.simplygonData.append(i)

        elif len(self.inititalSelection) == 0:
            lod0_data = []
            lod0_rels = cmds.listRelatives("|lod0", c=1, type="transform", f=1)
            for i in lod0_rels:
                if "chassis" in i:
                    chassis_rels = cmds.listRelatives(i, c=1, type="transform", f=1)
                    chassis_L = []
                    chassis_R = []

                    for j in chassis_rels:
                        if "_L" in j:
                            chassis_L.append(j)
                        elif "_R" in j:
                            chassis_R.append(j)

                    if chassis_L: self.simplygonData.append(chassis_L)
                    if chassis_R: self.simplygonData.append(chassis_R)
                else:
                    self.simplygonData.append(i)

    def typeCoeffReduce(self, obj):
        if Utils.checkType(obj) == "mesh":
            pass
        if Utils.checkType(obj) == "group":
            pass
        if Utils.checkType(obj) == "list":
            obj = obj[0]

        if "gun" in obj:
            coeff = 0.40
        elif "hull" in obj:
            coeff = 0.30
        elif "chassis" in obj:
            coeff = 0.40
        elif "turret" in obj:
            coeff = 0.30

        return coeff

    def removeDupplicateList(self, currentList):
        resultList = list(set(currentList))
        return resultList

    def setPivotLod4(self):
        lod4_child = cmds.listRelatives('lod4', ad=1, typ='transform', f=1)
        lod4_child = cmds.filterExpand(lod4_child, sm=12)
        lod4_child = self.removeDupplicateList(lod4_child)
        lod4_child = cmds.ls(lod4_child, l=1)
        if lod4_child:
            for child in lod4_child:
                if 'hull' in child or 'turret' in child or 'gun' in child:
                    lod0_child = 'lod0' + child.split('lod4')[1]
                    pivot = cmds.xform(lod0_child, q=1, rp=1, ws=1)
                    cmds.xform(child, rp=pivot, sp=pivot)

    def on_offServer(self, enable):
        cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
        CREATE_NO_WINDOW = 0x08000000
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        gui = False
        service = False
        for line in proc.stdout:
            if 'LocalAgentGUI.exe' in line:
                if enable == 'off':
                    subprocess.call('taskkill /F /IM Simplygon.Cloud.Yoda.Backend.LocalAgentGUI.exe',
                                    creationflags=CREATE_NO_WINDOW)
                    print('Kill agent')
                    gui = True
                if enable == 'on':
                    print('Agent executed')
                    gui = True

            if 'LocalAgentService.exe' in line:
                splLine = line.split('\"')
                if enable == 'off':
                    subprocess.call('taskkill /F /IM Simplygon.Cloud.Yoda.Backend.LocalAgentService.exe',
                                    creationflags=CREATE_NO_WINDOW)
                    print('Kill service')
                    service = True
                if enable == 'on':
                    print('Service executed', line)
                    service = True

        if not gui and enable == 'on':  # when False
            subprocess.Popen(["C://Simplygon//Grid//Agent//Simplygon.Cloud.Yoda.Backend.LocalAgentGUI.exe"],
                             shell=False)
        # subprocess.Popen(["C://Program Files//Simplygon//Grid//Agent//Simplygon.Cloud.Yoda.Backend.LocalAgentGUI.exe"], shell=False)
        if not service and enable == 'on':
            subprocess.Popen(["C://Simplygon//Grid//Agent//Simplygon.Cloud.Yoda.Backend.LocalAgentService.exe"],
                             shell=False)
        # subprocess.Popen(["C://Program Files//Simplygon//Grid//Agent//Simplygon.Cloud.Yoda.Backend.LocalAgentService.exe"], shell=False)

    def _send_to_simplygon(self, command):
        for x in range(10):
            try:
                resultList = meval(command)
                print('EXPORTED!')
                break
            except Exception:
                traceback.print_exc()

        return resultList

    def runSimplygonProxy(self):
        sceneTextures = Utils.clearTextures()
        cmds.select(d=1)

        for i in self.simplygonData:
            if Utils.checkType(i) == "mesh":
                cmds.select(i)

                meshName = i.split("|")[-1]
                meshPath = i[:-1 * (len(meshName) + 1)]
                meshPathList = meshPath.split("|")[1:]
                print('OBJECT COEFF MESH', i)

                evalCommand = self.melCmdProxy()
                resultList = self._send_to_simplygon(evalCommand)

                print('RESULT PRESET LIST ', resultList)

                if resultList:
                    for j in resultList:
                        lod = 'lod4'
                        destinationPath = "|" + lod
                        for k in range(1, len(meshPathList)):
                            destinationPath += "|" + meshPathList[k]
                        # create path
                        parentPath = Utils.groupCheckAndCreate(destinationPath)
                        newDAGPath = cmds.ls(cmds.parent(j, parentPath), sl=1, l=1)
                        cmds.rename(newDAGPath, meshName)

            elif Utils.checkType(i) == "group":
                cmds.select(i)

                groupName = i.split("|")[-1]
                groupPath = i
                groupPathList = groupPath.split("|")[1:]

                print('OBJECT COEFF group', i)

                evalCommand = self.melCmdProxy()
                resultList = self._send_to_simplygon(evalCommand)

                print('RESULT PRESET LIST ', resultList)

                if resultList:
                    for j in resultList:
                        lod = "lod4"
                        destinationPath = "|" + lod
                        for k in range(1, len(groupPathList)):
                            destinationPath += "|" + groupPathList[k]

                        parentPath = Utils.groupCheckAndCreate(destinationPath)
                        newDAGPath = cmds.ls(cmds.parent(j, parentPath), sl=1, l=1)

                        if lod == "lod4":
                            newName = j.split("|")[-1][: -1 * (len(j.split("_")[-1]) + 1)]
                            cmds.rename(newDAGPath, groupName.split('_')[0])

            elif Utils.checkType(i) == "list":
                cmds.select(i)

                print('OBJECT COEFF list', i)

                evalCommand = self.melCmdProxy()
                resultList = self._send_to_simplygon(evalCommand)

                print('RESULT PRESET LIST ', resultList)

                if resultList:
                    for j in resultList:
                        meshName = j.split("|")[-1]
                        meshPath = j[:-1 * (len(meshName) + 1)]
                        meshPathList = meshPath.split("|")[1:]

                        lod = "lod4"
                        destinationPath = "|" + lod

                        if lod == "lod4":
                            destinationPath += "|" + "chassis_01"

                        parentPath = Utils.groupCheckAndCreate(destinationPath)
                        newDAGPath = cmds.ls(cmds.parent(j, parentPath), sl=1, l=1)

                        if lod == "lod4":
                            if "_L" in i[0]:
                                cmds.rename(newDAGPath, "chassis_L")
                            elif "_R" in i[0]:
                                cmds.rename(newDAGPath, "chassis_R")

        print('RECONNECT TEXTURES')
        Utils.reAssignTextures(sceneTextures)

    def runSimplygon(self):
        print('DATA TO SIMPLYGON ', self.simplygonData)
        print('DETACH TEXTURES')  # BUG WOTA-111852
        count1, count2, count3, lod_c1, lod_c2, lod_c3 = self.coeff_count[0], self.coeff_count[1], self.coeff_count[2], \
                                                         self.coeff_count[3], self.coeff_count[4], self.coeff_count[5]
        sceneTextures = Utils.clearTextures()
        cmds.select(d=1)

        for i in self.simplygonData:
            if Utils.checkType(i) == "mesh":
                cmds.select(i)
                meshName = i.split("|")[-1]
                meshPath = i[:-1 * (len(meshName) + 1)]
                meshPathList = meshPath.split("|")[1:]

                coeff = self.typeCoeffReduce(i)
                print('OBJECT COEFF', i, coeff)

                lods_coff = [lod_c1 * coeff, lod_c2, lod_c3]
                evalCommand = self.melCmdReduce(lods_coff)
                resultList = self._send_to_simplygon(evalCommand)

                print('RESULT PRESET LIST ', resultList)

                if resultList:
                    for j in resultList:
                        lod = j.lower().split("_")[-1]
                        destinationPath = "|" + lod
                        for k in range(1, len(meshPathList)):
                            destinationPath += "|" + meshPathList[k]
                        # create path
                        parentPath = Utils.groupCheckAndCreate(destinationPath)
                        newDAGPath = cmds.ls(cmds.parent(j, parentPath), sl=1, l=1)
                        cmds.rename(newDAGPath, meshName)

            elif Utils.checkType(i) == "group":
                cmds.select(i)
                groupName = i.split("|")[-1]
                groupPath = i
                groupPathList = groupPath.split("|")[1:]

                coeff = self.typeCoeffReduce(i)
                print('OBJECT COEFF 2', i, coeff)

                lods_coff = [lod_c1 * coeff, lod_c2, lod_c3]
                evalCommand = self.melCmdReduce(lods_coff)
                resultList = self._send_to_simplygon(evalCommand)

                print('RESULT PRESET LIST ', resultList)

                if resultList:
                    for j in resultList:
                        lod = j.lower().split("_")[-1]
                        destinationPath = "|" + lod

                        for k in range(1, len(groupPathList)):
                            destinationPath += "|" + groupPathList[k]

                        parentPath = Utils.groupCheckAndCreate(destinationPath)
                        newDAGPath = cmds.ls(cmds.parent(j, parentPath), sl=1, l=1)

                        if lod == "lod4":
                            newName = j.split("|")[-1][: -1 * (len(j.split("_")[-1]) + 1)]
                            cmds.rename(newDAGPath, groupName.split('_')[0])
                        else:
                            newName = j.split("|")[-1][: -1 * (len(j.split("_")[-1]) + 1)]
                            cmds.rename(newDAGPath, newName)

            elif Utils.checkType(i) == "list":
                cmds.select(i)
                print('LIST ', i)
                tracks = cmds.ls('track_*')
                cmds.select(tracks, d=1)

                coeff = self.typeCoeffReduce(i)
                print('OBJECT COEFF', i, coeff)

                lods_coff = [lod_c1 * coeff, lod_c2, lod_c3]
                evalCommand = self.melCmdReduce(lods_coff)
                resultList = self._send_to_simplygon(evalCommand)

                print('RESULT PRESET LIST ', resultList)

                if resultList:
                    for j in resultList:
                        meshName = j.split("|")[-1]
                        meshPath = j[:-1 * (len(meshName) + 1)]
                        meshPathList = meshPath.split("|")[1:]

                        lod = j.lower().split("_")[-1]
                        destinationPath = "|" + lod

                        if lod == "lod4":
                            destinationPath += "|" + "chassis_01"
                        else:
                            for k in range(1, len(meshPathList)):
                                destinationPath += "|" + meshPathList[k]

                        parentPath = Utils.groupCheckAndCreate(destinationPath)
                        newDAGPath = cmds.ls(cmds.parent(j, parentPath), sl=1, l=1)

                        if lod == "lod4":
                            if "_L" in i[0]:
                                cmds.rename(newDAGPath, "chassis_L")
                            elif "_R" in i[0]:
                                cmds.rename(newDAGPath, "chassis_R")
                        else:
                            newName = j.split("|")[-1][: -1 * (len(j.split("_")[-1]) + 1)]
                            if "track" in newDAGPath[0]:
                                cmds.delete(newDAGPath)
                            else:
                                cmds.rename(newDAGPath, newName)

        print('RECONNECT TEXTURES')
        Utils.reAssignTextures(sceneTextures)

    def autoMapLayout(self):
        self.processingObjects = []
        allMeshes = cmds.ls(type="mesh", l=1)
        for i in allMeshes:
            if 'lod4' in i:
                uvset = cmds.polyUVSet(i, query=True, currentUVSet=True)
                if uvset != 'map1':
                    cmds.polyUVSet(i, rename=True, newUVSet='map1')
                self.processingObjects.append(i)

        self.processingObjects = list(set(self.processingObjects))

        for i in self.processingObjects:
            cmds.polyAutoProjection(i, \
                                    layoutMethod=0, \
                                    projectBothDirections=0, \
                                    insertBeforeDeformers=1, \
                                    createNewMap=0, \
                                    layout=2, \
                                    scaleMode=1, \
                                    optimize=0, \
                                    planes=6, \
                                    percentageSpace=0.2, \
                                    worldSpace=0)

        cmds.delete(self.processingObjects, ch=1)
        cmds.select(self.processingObjects)

        cmds.polyMultiLayoutUV(layoutMethod=1, \
                               scale=2, \
                               rotateForBestFit=2, \
                               flipReversed=1, \
                               percentageSpace=0.2, \
                               layout=2, \
                               prescale=2, \
                               sizeU=1, \
                               sizeV=1, \
                               offsetU=0, \
                               offsetV=0)

        cmds.select(self.processingObjects)
        cmds.delete(ch=1)
