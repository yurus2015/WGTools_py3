import maya.cmds as cmds
from validator2019.utils.validator_API import *

checkId = 704
checkLabel = "3.14 Check objects group names and lods existance"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    return_list = []

    file_name = cmds.file(q=True, sn=True).split("/")[-1][:-3]
    for x in vl_listRootGroups():
        if not file_name == x[0:len(file_name)]:
            message = "%s object and scene name are not equal" % x
            return_list.append([message, x])

    for x in vl_listRootGroups():
        if not cmds.objExists(x + "|lod0"):
            message = "%s object dosn't have lod0" % x
            return_list.append([message, x])
        if not cmds.objExists(x + "|lod1"):
            message = "%s object dosn't have lod1" % x
            return_list.append([message, x])

    return return_list
