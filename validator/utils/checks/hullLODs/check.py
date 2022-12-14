import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 19

checkLabel = "8.1 Check lods of hulls"


def main():
    listTransforms = vl_listAllTransforms()
    returnList = []

    # checking all lods have hull
    lod0 = re.compile("lod0");
    lod0_list = []
    lod1 = re.compile("lod1");
    lod1_list = []
    lod2 = re.compile("lod2");
    lod2_list = []
    lod3 = re.compile("lod3");
    lod3_list = []
    lod4 = re.compile("lod4");
    lod4_list = []

    hull = re.compile("hull\Z");

    all_lods = cmds.ls('lod*', tr=1)

    # print 'ALL LODS', all_lods

    def checkingLods(groupName, lodList):

        lodsObject = []
        for x in listTransforms:
            if groupName.search(x) != None:
                lodsObject.append(x)
        result = False
        for x in lodsObject:
            if hull.search(x) != None:
                result = True
                lodList.append(x)
                break
        # print 'LOD LIST', lodList
        if not result:
            tmp = []
            tmp.append(groupName.pattern + " - dosn't have Hull object")
            tmp.append(groupName.pattern)
            returnList.append(tmp)

    if len(all_lods) == 1 and 'lod0' in all_lods[0]:
        # print 'PreExport'
        pass
    else:
        checkingLods(lod0, lod0_list)
        checkingLods(lod1, lod1_list)
        checkingLods(lod2, lod2_list)
        checkingLods(lod3, lod3_list)
        checkingLods(lod4, lod4_list)

        # check lods polycount
        if len(returnList) == 0:
            polycount_list = [ \
                [lod0_list[0], cmds.polyEvaluate(lod0_list[0], t=True)], \
                [lod1_list[0], cmds.polyEvaluate(lod1_list[0], t=True)], \
                [lod2_list[0], cmds.polyEvaluate(lod2_list[0], t=True)], \
                [lod3_list[0], cmds.polyEvaluate(lod3_list[0], t=True)], \
                [lod4_list[0], cmds.polyEvaluate(lod4_list[0], t=True)], \
                ]

            copy_polycount_list = [ \
                [lod0_list[0], cmds.polyEvaluate(lod0_list[0], t=True)], \
                [lod1_list[0], cmds.polyEvaluate(lod1_list[0], t=True)], \
                [lod2_list[0], cmds.polyEvaluate(lod2_list[0], t=True)], \
                [lod3_list[0], cmds.polyEvaluate(lod3_list[0], t=True)], \
                [lod4_list[0], cmds.polyEvaluate(lod4_list[0], t=True)], \
                ]

            copy_polycount_list.sort(key=lambda x: x[1])
            list.reverse(copy_polycount_list)

            for x in range(len(polycount_list)):
                if polycount_list[x][1] != copy_polycount_list[x][1]:
                    tmp = []
                    tmp.append(polycount_list[x][0] + " - polycount mismatching")
                    tmp.append(polycount_list[x][0])
                    returnList.append(tmp)

    return returnList
