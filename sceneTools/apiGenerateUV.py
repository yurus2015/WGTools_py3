#-----------------------------------------------------------------------------------
#   SCRIPT      apiGenerateUV.py
#   AUTHOR      Evgen Zaitsev
#               ev.zaitsev@gmail.com
#
#   DESCRIPTION:
#    
#   copy map1 to map2, generate random uv's for map2
#   NO undo support
#   works only with no construction history 
#
#-----------------------------------------------------------------------------------
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya 
import random

def main():
    runOnSelected( )

def runOnSelected( ):
    m_list = OpenMaya.MSelectionList() 
    OpenMaya.MGlobal.getActiveSelectionList( m_list )
    m_listIt = OpenMaya.MItSelectionList( m_list ) 
    while not m_listIt.isDone():
        m_path        = OpenMaya.MDagPath()   # will hold a path to the selected object 
        m_component   = OpenMaya.MObject()    # will hold a list of selected components
        # we retrieve a dag path to a transform or shape, and an MObject
        # to any components that are selected on that object (if any).
        if (OpenMaya.MItSelectionList.kDagSelectionItem == m_listIt.itemType()):
            m_listIt.getDagPath( m_path )
            if ( m_path.hasFn( OpenMaya.MFn.kMesh )):
                runItem( m_path )
        # if the component is list is valid
        next(m_listIt)

def runItem( m_path ):
    # works only if object has no construction history
    cmds.bakePartialHistory( m_path.fullPathName() ,prePostDeformers=True )
    #OpenMaya.MGlobal.executeCommand('doBakeNonDefHistory( 1, {"prePost" });')
    # copy map1 to map2
    m_uvSetStr = cleanupUVSets( m_path )
    # get function set to the m_path
    m_fnMesh    = OpenMaya.MFnMesh( m_path )
    m_fnMesh.setCurrentUVSetName(m_uvSetStr)
    # generate uv id's
    m_uvIds    = OpenMaya.MIntArray(m_fnMesh.numFaceVertices())
    m_uvCounts = OpenMaya.MIntArray(m_fnMesh.numPolygons())
    m_uvIndex  = 0
    m_uvCountsIndex  = 0
    m_itPoly = OpenMaya.MItMeshPolygon(m_path)
    while not m_itPoly.isDone():
        m_polygonIndex = m_itPoly.index()
        m_polygonVertices = OpenMaya.MIntArray()
        m_itPoly.getVertices( m_polygonVertices )
        m_uvCounts[m_uvCountsIndex] = m_itPoly.polygonVertexCount()
        m_uvCountsIndex += 1
        m_curIndex = m_uvIndex
        m_localVertId = 0
        for m_polyVertex in m_polygonVertices:
            m_uvIds[m_uvIndex] = m_curIndex + m_localVertId
            m_uvIndex += 1
            m_localVertId +=1
        next(m_itPoly)
    # generate random uv's
    # per face per vertex
    m_uvIndex = 0
    m_itPoly = OpenMaya.MItMeshPolygon( m_path )
    while not m_itPoly.isDone():
        m_polygonIndex = m_itPoly.index()
        m_polygonVertices = OpenMaya.MIntArray()
        m_itPoly.getVertices( m_polygonVertices )
        m_localVertId = 0
        for m_polyVertex in m_polygonVertices:
            # first setUV(uvId,u,v,uvSetStr)
            m_fnMesh.setUV( m_uvIds[m_uvIndex], random.random(), random.random(), m_uvSetStr )
            # second assignUV(polygonId,vertexIndex,uvId,uvSetStr)
            m_fnMesh.assignUV( m_polygonIndex, m_localVertId, m_uvIds[m_uvIndex], m_uvSetStr )
            # ----------
            m_uvIndex += 1
            m_localVertId +=1
        next(m_itPoly)
    m_fnMesh.updateSurface()
    
def cleanupUVSets( m_path ):
    # keep only 1st uvSet
    m_fnMesh = OpenMaya.MFnMesh( m_path )
    m_list = []
    m_fnMesh.getUVSetNames(m_list)
    if (len(m_list) > 1):
        for i in range(1,len(m_list)):
            m_fnMesh.deleteUVSet(m_list[i])
    # create empty uvSet
    #m_uvSetStr = m_fnMesh.createUVSetWithName("map2")
    m_uvSetStr = m_fnMesh.copyUVSetWithName(m_list[0],'map2')
    return m_uvSetStr

main()