
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.mel as mel
import math
import re
from validator2019.utils.validator_API import *
checkId = 51
checkLabel = "4.4 Check hard UVs inside uv mesh (too long)"


def main():
    print('<< ' + checkLabel.upper() + ' >>')
    objList = vl_listAllTransforms()
    returnList = []

    """shapeArray = cmds.ls(type='mesh', dag=1, l = True)
    polyArray = list(set(cmds.listRelatives(shapeArray, p=1, type="transform", f = True)))

    for obj in polyArray:
        tmp = obj+".map[*]"
        cmds.select(tmp)
        allEdgesList = []
        borderEdgesList = []
        innerEdges = []
        innerHardEdges = []
        splitedList = []

        #Get all edges
        mel.eval("PolySelectConvert 20;")
        allEdgesList = cmds.ls(sl=1, fl=1, l=True)

        #Get border edges
        potentialEdges = cmds.filterExpand(ex=1, sm=32)
        removeEdges = []
        for edge in potentialEdges:
            uvs = cmds.polyListComponentConversion(edge, fe=1, tuv=1)
            uvs = cmds.ls(uvs, fl=1, l=True)
            if len(uvs)<=2:
                removeEdges.append(edge) #put the edge in the list
        cmds.select(removeEdges, d=1) #deselect non-border edges
        borderEdgesList = cmds.ls(sl=1, fl=1, l=True)

        #Get all inneallEdgesListr edges
        for i in allEdgesList:
            if i not in borderEdgesList:
                innerEdges.append(i)
        #print len(innerEdges)
        cmds.select(innerEdges)

        #Get all inner hard Edges
        cmds.polySelectConstraint(m=2, t=0x8000, sm=1)
        innerHardEdges = cmds.ls(sl=1, fl=1, l=True)
        cmds.polySelectConstraint(m=0)
        #cmds.select(innerHardEdges)

        #Get All faces which are contained in the edges
        for edge in innerHardEdges:
            print "==========="
            facesAround = cmds.polyInfo(edge, ef=1)
            print facesAround

            #Split the array until the first digit
            tmp = re.findall('\d+', str(facesAround))
            print tmp

            #splitedList = tmpArray[0][tmp:-2].split("    ")
            #print "faceAround", splitedList
            #create list information about material in the scene. Described above ^^^.
            #list.reverse(splitedList)
            #print splitedList
            #print facesAround
            face_a = tmp[0]
            #face_a = face_a.replace(":","")

            face_b = tmp[1]
            #face_b = face_b.replace(":","")

            print "Face a ", face_a
            print "Face b ", face_b
            #print face_a
            #print face_b
            face_a_normal = cmds.polyInfo(obj+".f[" + str(face_a) + "]", fn=1)
            face_b_normal = cmds.polyInfo(obj+".f[" + str(face_b) + "]", fn=1)

            #print face_a_normal
            splitedVectorList = face_a_normal[0][:-2].split(" ")
            list.reverse(splitedVectorList)
            #print splitedVectorList
            face_a_normal_vec_x = float(splitedVectorList[2])
            face_a_normal_vec_y = float(splitedVectorList[1])
            face_a_normal_vec_z = float(splitedVectorList[0])


            #print face_b_normal
            splitedVectorList = face_b_normal[0][:-2].split(" ")
            list.reverse(splitedVectorList)
            #print splitedVectorList
            face_b_normal_vec_x = float(splitedVectorList[2])
            face_b_normal_vec_y = float(splitedVectorList[1])
            face_b_normal_vec_z = float(splitedVectorList[0])

            #Get the angle between two faces
            upperNum = face_a_normal_vec_x * face_b_normal_vec_x + face_a_normal_vec_y * face_b_normal_vec_y + face_a_normal_vec_z * face_b_normal_vec_z
            lowerNum = math.sqrt(face_a_normal_vec_x * face_a_normal_vec_x + face_a_normal_vec_y * face_a_normal_vec_y + face_a_normal_vec_z * face_a_normal_vec_z) * math.sqrt(face_b_normal_vec_x * face_b_normal_vec_x + face_b_normal_vec_y * face_b_normal_vec_y + face_b_normal_vec_z * face_b_normal_vec_z)
            cosAngle = upperNum/lowerNum
            #radians = math.acos(math.fabs(cosAngle))
            #angle = math.degrees(radians)
            #print cosAngle
            #print angle
            if cosAngle < 120:
                returnList.append(edge)"""




    #errorMessage = "Next objects still have a construction history:"
    #returnList.append(errorMessage)


    return  returnList

