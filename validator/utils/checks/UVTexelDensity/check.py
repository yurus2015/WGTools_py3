import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 58
checkLabel = "4.12 Check UVs texel density (FIX as VERY long)"


def removeList(fromList, thisList):
    resultList = [n for n in fromList if n not in thisList]
    resultList = list(resultList)
    return resultList


def universal2d_bbox(sel, type):
    bbx = cmds.polyEvaluate(bc2=True)
    xval = bbx[0]
    yval = bbx[1]
    value = [0, 0]
    if (type == "pivot"):
        value[0] = (xval[0] + xval[1]) / 2.0
        value[1] = (yval[0] + yval[1]) / 2.0
    if (type == "size"):
        value[0] = xval[1] - xval[0]  # width
        value[1] = yval[1] - yval[0]  # hight
    if (type == "u"):
        value[0] = xval[0]  # left
        value[1] = xval[1]  # right
    if (type == "v"):
        value[0] = yval[0]  # bottom
        value[1] = yval[1]  # top
    return value


def uvSlellArray(selection):
    shellData = list()
    # print 'SA begin'
    while selection:
        cmds.select(selection[0])
        # print 'SA select point'
        cmds.polySelectConstraint(m=2)
        cmds.polySelectConstraint(bo=0, sh=1, cr=0)
        # print 'SA select shell'
        shell = cmds.ls(sl=1, fl=1)
        if shell:
            shellData.append(shell)
            # print 'SA add shell'
        selection = removeList(selection, shell)
        # print 'SA remove uv shell'
        cmds.polySelectConstraint(bo=0, sh=0, cr=0);
        cmds.polySelectConstraint(m=0, t=0x0000)
    return shellData


def main():
    objList = vl_listAllTransforms()
    returnList = []

    """shapeArray = cmds.ls(type='mesh', dag=1, l = True)
    polyArray = list(set(cmds.listRelatives(shapeArray, p=1, type="transform", f = True)))

    checkerTDen = 400
    checkerThreshold = 10

    tDenMin = checkerTDen - checkerThreshold
    tDenMax = checkerTDen + checkerThreshold

    checkerStatus_1k = 0
    checkerStatus_2k = 0
    checkerStatus_4k = 0

    listWrongDens_1k = []
    listWrongDens_2k = []
    listWrongDens_4k = []

    for obj in polyArray:
        #get uv shell list
        cmds.select(obj)
        cmds.filterExpand(ex=True, sm=(34,35) )
        selList = cmds.ls(sl=1, l=1)
        #print "obj: ",obj
        #print "selList: ",selList
        if len(selList):
            uvList = cmds.polyListComponentConversion( selList, ff=True, fuv=True, tuv=True)
            #print "uvList: ", uvList
            cmds.select(uvList)
            uvList = cmds.ls( fl=True, sl=True )
            shells = uvSlellArray(uvList)
            #print shells
            for shell in shells:
                #print "shell: ", shell
                cmds.select(shell)
                sizeSel = universal2d_bbox(shell,'size')
                cmds.unfold(i=0, ss=0.001, gb=0, gmb=0.5, pub=False, ps=False, oa=0, us=True, s=1)
                newSize = universal2d_bbox(shell,'size')
                #print sizeSel
                #print newSize
                if sizeSel[0] == 0 or newSize == 0:
                    continue
                coeff = sizeSel[0]/newSize[0]
                cmds.unfold(i=0, ss=0.001, gb=0, gmb=0.5, pub=False, ps=False, oa=0, us=True, s=coeff)
                cmds.select(selList)
                texel= coeff*100

                check_1024 = texel*1024
                check_2048 = texel*2048
                check_4096 = texel*4096

                faceList = cmds.polyListComponentConversion( shell, fuv=True, tf=True)
                #print faceList

                #check 1k
                if check_1024 < tDenMin or check_1024 > tDenMax:
                    checkerStatus_1k = 1
                    listWrongDens_1k.append(faceList)

                #check 2k
                if check_2048 < tDenMin or check_2048 > tDenMax:
                    checkerStatus_2k = 1
                    listWrongDens_2k.append(faceList)

                #check 4k
                if check_4096 < tDenMin or check_4096 > tDenMax:
                    checkerStatus_4k = 1
                    listWrongDens_4k.append(faceList)
                """"""
                #print check_1024, check_2048, check_4096
                #returnList.append(shell)
                #print ('4096 -> ' + str(texel*4096) + ' 2048 -> ' + str(texel*2048))
                #print coeff

    errorMessage_1k = "===Check for 1024p==="
    errorMessage_2k = "===Check for 2048p==="
    errorMessage_4k = "===Check for 4096p==="

    if checkerStatus_1k:
        returnList.append(errorMessage_1k)
        for i in listWrongDens_1k:
            returnList.append(i[0])

    if checkerStatus_2k:
        returnList.append(errorMessage_2k)
        for i in listWrongDens_2k:
            returnList.append(i[0])

    if checkerStatus_4k:
        returnList.append(errorMessage_4k)
        for i in listWrongDens_4k:
            returnList.append(i[0])
    """

    return returnList
