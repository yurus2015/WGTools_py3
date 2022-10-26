
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.mel as mel
from validator2019.utils.validator_API import *
checkId = 50
checkLabel = "4.4 Check UV border for edges (too long)"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    objList = vl_listAllTransforms()
    returnList = []

    """
    shapeArray = cmds.ls(type='mesh', dag=1, l = True)
    polyArray = list(set(cmds.listRelatives(shapeArray, p=1, type="transform", f = True)))



    for obj in polyArray:
        tmp = obj+".map[*]"
        #print tmp
        cmds.select(tmp)
        mel.eval("polySelectBorderShell 1;")
        mel.eval("PolySelectConvert 20;")
        potentialEdges = cmds.filterExpand(ex=1, sm=32)
        removeEdges = []
        for edge in potentialEdges:
            uvs = cmds.polyListComponentConversion(edge, fe=1, tuv=1)
            uvs = cmds.ls(uvs, fl=1)
            if len(uvs)<=2:
                #print len(removeEdges)
                removeEdges.append(edge) #put the edge in the list
        cmds.select(removeEdges, d=1) #deselect non-border edges
        selectedEdges = cmds.ls(sl=1)
        #print selectedEdges
        #check for a soft edges
        #polySelectConstraint -m 2 -t 0x8000 -sm 1;
        cmds.polySelectConstraint(m=2, t=0x8000, sm=2)
        selectedSoftEdges = cmds.ls(sl=1)
        #print selectedSoftEdges
        #cmds.select(selectedSoftEdges, add=1)

        for edge in selectedSoftEdges:
            facesAround = cmds.polyInfo(edge, ef=1)
            tmp = re.findall('\d+', str(facesAround))
            #splitedList = facesAround[0][:-2].split("    ")
            #create list information about material in the scene. Described above ^^^.
            #ist.reverse(splitedList)
            #print splitedList
            #print facesAround
            #splitedList[0].replace(" ","")
            #splitedList[1].replace(" ","")
            #print splitedList[0]
            #print splitedList[1]
            face_a = obj + ".f[" + tmp[0] + "]"
            face_b = obj + ".f[" + tmp[1] + "]"
            print face_a
            print face_b
            #check if face_a and face_b are sharing the same UV Shell
            #get the shell

            cmds.select(face_a)
            uvs = cmds.polyListComponentConversion(face_a, tuv=True )
            cmds.select(uvs)
            face_a_uvs = cmds.ls(sl=1, fl=1)
            #print face_a_uvs
            mel.eval("polySelectBorderShell 0;")
            uvShell_a = cmds.ls(sl=1,fl=1)
            #print uvShell_a


            cmds.select(face_b)
            uvs = cmds.polyListComponentConversion(face_b, tuv=True )
            cmds.select(uvs)
            face_b_uvs = cmds.ls(sl=1, fl=1)
            #print face_b_uvs
            mel.eval("polySelectBorderShell 0;")
            uvShell_b = cmds.ls(sl=1,fl=1)
            #print uvShell_b

            checkStatus = 0
            for i in face_b_uvs:
                if i not in uvShell_a:
                    returnList.append(edge)
                    break

            cmds.polySelectConstraint(bo = 0, sh=0, cr=0);
            cmds.polySelectConstraint( m=0, t=0x0000)



    cmds.selectMode( object=True )
    cmds.select(cl=1)"""




    #errorMessage = "Next objects still have a construction history:"
    #returnList.append(errorMessage)


    return  returnList
