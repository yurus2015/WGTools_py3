import maya.cmds as cmds
from validator.utils.validator_API import *
import re

checkId = 707
checkLabel = "1.18 Check prefix"


def main():
    prefixes = ['^hd_', '^cw_']
    return_list = []

    for x in vl_listRootGroups():
        checkValue = False
        for i in prefixes:
            if re.search(i, x):
                checkValue = True
                print('PREFIX ', x)
        if not checkValue:
            message = x + " object doesn't have any from these (" + (
                ''.join(str(e[1:] + " ") for e in prefixes)) + ") prefixes"
            return_list.append([message, x])

    return return_list
