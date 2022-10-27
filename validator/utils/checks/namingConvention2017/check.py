import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 10001

checkLabel = "Project/File/SceneObjects names 2017"


def matchPattern(pattern=None, a=None):
    if a in pattern:
        return True
    else:
        return False


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    returnList = []

    path = cmds.file(q=1, sn=1)
    pathSegments = path.split("/")[:-1]

    '''1st stage - folder name'''

    # hd_bld_SU _001 _ RichHouse

    # patterns
    objPrefix = ["hd"]
    objType = ["bld", "dec", "env", "gaf", "mle", "rw", "out"]
    objNation = ["SU", "EU", "EUGB", "EUNW", "EUIT", "AS", "ASKR", "ASCN", "ASJP", "SU", "AM", "AF", "UNI"]
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                "v", "w", "x", "y", "z"]

    valid = True
    message = None

    projectFolderName = None

    for i in pathSegments:
        if "hd_" in i:
            projectFolderName = i

    if not projectFolderName:
        valid = False
        message = "There is no project folder named HD_TYPE_NATION_NUM_NAME"

    partial_name = []
    try:
        partial_name = projectFolderName.split("_")
    except:
        pass

    if len(partial_name) < 5:
        # error
        valid = False
        message = "The name of the project folder name is not valid (not enough words separated by '_')"

    elif len(partial_name) == 5:
        # object
        if valid:
            valid = matchPattern(objPrefix, partial_name[0])
            message = "Project folder name is not started with 'hd'"
            if valid:
                valid = matchPattern(objType, partial_name[1])
                message = "Project folder name has unknown type of object - " + str(partial_name[1])
                if valid:
                    valid = matchPattern(objNation, partial_name[2])
                    message = "Project folder name has unknown nation - " + str(partial_name[2])
                    if valid:
                        try:
                            xx = int(partial_name[3])
                            valid = True
                        except:
                            valid = False
                            message = "Project folder name doesn't have a valid number"
                        if valid:
                            if len(partial_name[3]) != 3:
                                valid = False
                                message = "Project folder name doesn't have a valid number"
                            if valid:
                                valid = partial_name[4].isalpha()
                                message = "Project folder name has a not valid object name - " + str(partial_name[4])
                                if valid:
                                    valid = partial_name[4][0].istitle()
                                    message = "Project folder name has not valid object name  - " + str(partial_name[4])
                                    if valid:
                                        message = "Good Job"

    elif len(partial_name) == 4:
        # hangar
        if valid:
            valid = matchPattern(objPrefix, partial_name[0])
            message = "Project folder name is not started with 'hd'"
            if valid:
                if partial_name[1][0] == "h" and matchPattern(digits, partial_name[1][1]):
                    valid = True
                else:
                    valid = False
                    message = "Hangar name is not valid"
                if valid:
                    try:
                        xx = int(partial_name[2])
                        valid = True
                    except:
                        valid = False
                        message = "Project folder name doesn't have a valid number"
                    if valid:
                        if partial_name[3].isalpha() and partial_name[3][0].istitle():
                            valid = True
                        else:
                            valid = False
                        message = "Project folder name has not valid object name"
                        if valid:
                            message = "Good Job"

    '''2nd stage - scene name'''

    fileName = cmds.file(q=True, sn=1, shn=1).split(".")[0]

    valid2 = True
    message2 = ""

    if projectFolderName and fileName != projectFolderName:
        valid2 = False
        message2 = "This scene file name is not valid. The project folder name and the file name are different."

    '''3d stage - groups name'''

    topLevelDAG = cmds.ls(assemblies=1)
    cameras = cmds.listRelatives(cmds.ls(cameras=1), f=1, p=1)

    objects = []
    for i in topLevelDAG:
        if "|" + i not in cameras:
            objects.append(i)

    wrongObjects = []

    fileNameLength = len(fileName.split("_"))

    if objects:
        for ii in objects:

            ii_len = len(ii.split("_"))
            ii_parts = ii.split("_")
            # print 'TTT', ii_parts

            if ii_len == fileNameLength and ii != fileName:
                wrongObjects.append(["Object name and file name are different: " + str(ii), ii])

            elif ii_len > fileNameLength:

                if ii_len > 7:
                    wrongObjects.append(["Undescore '_' count in object name is not valid: " + str(ii), ii])

                elif ii_len == 7:
                    if ii_parts[-1][0] not in digits or ii_parts[-2][0].lower() not in alphabet:
                        wrongObjects.append(
                            ["Wrong object name. In extra name digits should come last: " + str(ii), ii])

                    if len(ii_parts[-1]) != 2:
                        wrongObjects.append(["Postfix number must have only two digits: " + str(ii), ii])

                    if ii_parts[-2][0].islower() and 'crash' not in ii_parts[-2]:
                        wrongObjects.append(["Postfix name should start with a capital character: " + str(ii), ii])

                elif ii_len == 6:
                    if ii_parts[-1][0] in alphabet:
                        if not ii_parts[-1][0].isupper():
                            wrongObjects.append(["Postfix name should start with a capital character: " + str(ii), ii])
                    elif ii_parts[-1][0] in digits:
                        if len(ii_parts[-1]) != 2:
                            wrongObjects.append(["Postfix number must have only two digits: " + str(ii), ii])

                else:
                    if fileName not in ii:
                        wrongObjects.append(["Object name and the file name are different: " + str(ii), ii])

            elif ii_len < fileNameLength:

                wrongObjects.append(["Object name and the file name are different: " + str(ii), ii])

    ''' Compose '''
    if valid == False:
        returnList.append([message, ""])

    if valid2 == False:
        returnList.append([message2, ""])

    if wrongObjects:
        for i in wrongObjects:
            returnList.append(i)

    return returnList
