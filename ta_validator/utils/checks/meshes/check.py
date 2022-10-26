import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 31
checkLabel = "8.5 Check for empty shapes"

def main():
    print('<< ' + checkLabel.upper() + ' >>')
    listTransforms = vl_listAllTransforms()
    returnList = []

    for x in range(len(listTransforms)):
        shapes = cmds.listRelatives(listTransforms[x], shapes=True, f=True)
        if len(shapes) > 2:
            #if there is two or more connections, its means, transform have another empty shape(bug)
            errorMessage = listTransforms[x]
            tmp = []
            tmp.append(errorMessage)
            tmp.append("")
            returnList.append(tmp)

        if len(shapes) == 2 :
            origName = None
            for y in shapes:
                check = y.find("Orig")
                if check != -1:
                    origName = 1

            if origName != 1:
                #if there is two or more connections, its means, transform have another empty shape(bug)
                errorMessage = listTransforms[x]
                tmp = []
                tmp.append(errorMessage)
                tmp.append("")
                returnList.append(tmp)



    return  returnList
