import re
import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 151
checkLabel = "Check HP Existance"


def main():
    returnList = []

    pattern_HP0 = re.compile("\An\d\Z")
    pattern_HPN = re.compile("\An\d_\d\Z")
    pattern_HP = re.compile("\AHP_module\d\Z")

    modelList = list(set(cmds.ls(l=1, assemblies=1)) - set(cmds.listRelatives(cmds.ls(type="camera"), p=1, f=1)))

    for i in modelList:
        childrenList = cmds.listRelatives(i, c=1, ad=1, type="transform")

        statusFail = False

        HP_modules = []
        N_objects = []
        HP_type = None  # HP0 | HPN

        for j in childrenList:
            if pattern_HP0.search(j):  # type = HP0

                if HP_type == "HPN":
                    tmp = []
                    tmp.append(i + " has different types of n: n# and n#_#")
                    tmp.append(i)
                    returnList.append(tmp)
                    statusFail = True
                    break

                HP_type = "HP0"
                N_objects.append(j)

            elif pattern_HP.search(j):  # HP_module# found
                HP_modules.append(j)

            elif pattern_HPN.search(j):  # type = HPN

                # if type is already HPN - returnList append fail
                if HP_type == "HP0":
                    tmp = []
                    tmp.append(i + " has different types of n: n# and n#_#")
                    tmp.append(i)
                    returnList.append(tmp)
                    statusFail = True
                    break

                HP_type = "HPN"
                N_objects.append(j)

        if statusFail:
            continue  # go to the next model in the scene

        if not HP_type:
            continue

        elif HP_type == "HP0":
            if len(HP_modules) == 1 and HP_modules[0] == "HP_module0":
                pass
            else:
                tmp = []
                tmp.append(i + " should have only HP_module0")
                tmp.append(i)
                returnList.append(tmp)

        elif HP_type == "HPN":
            maxn = 0
            for j in N_objects:
                if int(j[-1]) > maxn:
                    maxn = int(j[-1])

            if len(HP_modules) != maxn:
                tmp = []
                tmp.append(i + " has different numbers of HP_module's and n#_#")
                tmp.append(i)
                returnList.append(tmp)

    return returnList
