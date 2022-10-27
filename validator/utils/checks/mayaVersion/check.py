import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 30
checkLabel = "1.1 Check Maya Version"


def main():
    objList = vl_listAllTransforms()
    returnList = []

    errorMessage = "You are using different from 2014 version maya"
    currentVersion = cmds.about(v=1)
    # A esli servis pack stoit, Ili versia mayki 32 bitna9. Y men9 naprimer prosto "2014"

    search = currentVersion.find("2014")

    if search != -1:
        pass
    else:
        tmp = []
        tmp.append(errorMessage)
        tmp.append("")
        returnList.append(tmp)

    return returnList
