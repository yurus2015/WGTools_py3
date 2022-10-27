class meshRebuilder(object):
    def __init__(self):
        self.__layers = {}
        self.__selection = []
        self.__layers_order = []

    def saveLayers(self):
        self.__selection = cmds.ls(sl=True);
        if len(self.__selection) > 0:
            for x in self.__selection:
                listConnections = cmds.listConnections(x, t="displayLayer")
                if listConnections != None:
                    for n in listConnections:
                        if self.__layers.get(n) == None:
                            self.__layers[n] = []
                        else:
                            self.__layers[n].append(x)

        else:
            self.__listLayers = cmds.ls(type="displayLayer")
            print('Layers', self.__listLayers)
            self.__layers_order = range(len(self.__listLayers))
            for index, i in enumerate(self.__listLayers):
                order = cmds.getAttr(i + '.displayOrder')
                print('Order ', order)
                self.__layers[index] = cmds.editDisplayLayerMembers(i, query=True, fn=1)
                print('Members layers', self.__layers[index])
                self.__layers_order[index] = [self.__layers[index], order, i]

    def loadLayers(self):
        if not len(self.__layers_order):
            return

        layers_order_sorted = sorted(self.__layers_order, key=lambda x: x[1])
        for x in layers_order_sorted:
            print('Layers load', x[2])
            if x[2] != 'defaultLayer':
                try:
                    cmds.createDisplayLayer(x[0], n=x[2])
                except:
                    print('Layer ' + x[2] + ' was empty. Dont created')


try:
    cmds.loadPlugin("meshRebuilder")
except:
    print('Plugin dint load')

rebuilder = meshRebuilder()
rebuilder.saveLayers()
cmds.rebuildMesh()
rebuilder.loadLayers()
