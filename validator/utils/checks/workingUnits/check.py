import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 61
checkLabel = "1.3 Check Working Units"


def main():
    objList = vl_listAllTransforms()
    returnList = []

    currentWorkingUnits = cmds.currentUnit(q=1, l=1)
    workingUnits = currentWorkingUnits

    if (currentWorkingUnits == "cm"):
        workingUnits = "centimetres"
    elif (currentWorkingUnits == "in"):
        workingUnits = "inches"
    elif (currentWorkingUnits == "mm"):
        workingUnits = "millimetres"
    elif (currentWorkingUnits == "ft"):
        workingUnits = "feets"
    elif (currentWorkingUnits == "yd"):
        workingUnits = "yards"

    errorMessage = "You are using " + workingUnits + " as working units. Change it to meters."

    if (currentWorkingUnits != "m"):
        tmp = []
        tmp.append(errorMessage)
        tmp.append(errorMessage)
        returnList.append(tmp)

    return returnList
