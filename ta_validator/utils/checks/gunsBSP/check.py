import maya.cmds as cmds
import re

from validator2019.utils.validator_API import *
checkId = 14

checkLabel = "Check BSP of guns"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    listTransforms = vl_listAllTransforms()
    returnList = []
    listGuns = []
    listGuns_bsp = []
    gun = re.compile("gun")
    bsp = re.compile("bsp")
    for x in listTransforms:
        if gun.search(x) is not None and bsp.search(x) is None:
            listGuns.append(x)
        if gun.search(x) is not None and bsp.search(x) is not None:
            listGuns_bsp.append(x)

    for x in listGuns:
        gun_bsp = re.compile(x.replace('|', '-') +"_bsp")
        result = False
        for y in listGuns_bsp:
            if gun_bsp.search(y.replace('|', '-')) is not None:
                result = True
        if not result:
            tmp = []
            tmp.append(x)
            tmp.append(x)
            returnList.append(tmp)


    return  returnList
