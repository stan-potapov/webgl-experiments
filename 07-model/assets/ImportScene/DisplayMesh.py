"""

 Copyright (C) 2001 - 2010 Autodesk, Inc. and/or its licensors.
 All Rights Reserved.

 The coded instructions, statements, computer programs, and/or related material 
 (collectively the "Data") in these files contain unpublished information 
 proprietary to Autodesk, Inc. and/or its licensors, which is protected by 
 Canada and United States of America federal copyright law and by international 
 treaties. 
 
 The Data may not be disclosed or distributed to third parties, in whole or in
 part, without the prior written consent of Autodesk, Inc. ("Autodesk").

 THE DATA IS PROVIDED "AS IS" AND WITHOUT WARRANTY.
 ALL WARRANTIES ARE EXPRESSLY EXCLUDED AND DISCLAIMED. AUTODESK MAKES NO
 WARRANTY OF ANY KIND WITH RESPECT TO THE DATA, EXPRESS, IMPLIED OR ARISING
 BY CUSTOM OR TRADE USAGE, AND DISCLAIMS ANY IMPLIED WARRANTIES OF TITLE, 
 NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE OR USE. 
 WITHOUT LIMITING THE FOREGOING, AUTODESK DOES NOT WARRANT THAT THE OPERATION
 OF THE DATA WILL BE UNINTERRUPTED OR ERROR FREE. 
 
 IN NO EVENT SHALL AUTODESK, ITS AFFILIATES, PARENT COMPANIES, LICENSORS
 OR SUPPLIERS ("AUTODESK GROUP") BE LIABLE FOR ANY LOSSES, DAMAGES OR EXPENSES
 OF ANY KIND (INCLUDING WITHOUT LIMITATION PUNITIVE OR MULTIPLE DAMAGES OR OTHER
 SPECIAL, DIRECT, INDIRECT, EXEMPLARY, INCIDENTAL, LOSS OF PROFITS, REVENUE
 OR DATA, COST OF COVER OR CONSEQUENTIAL LOSSES OR DAMAGES OF ANY KIND),
 HOWEVER CAUSED, AND REGARDLESS OF THE THEORY OF LIABILITY, WHETHER DERIVED
 FROM CONTRACT, TORT (INCLUDING, BUT NOT LIMITED TO, NEGLIGENCE), OR OTHERWISE,
 ARISING OUT OF OR RELATING TO THE DATA OR ITS USE OR ANY OTHER PERFORMANCE,
 WHETHER OR NOT AUTODESK HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH LOSS
 OR DAMAGE. 
 
"""

from DisplayCommon import *
from fbx import KFbxLayerElement
from fbx import KFbxSurfaceMaterial
from fbx import KFbxLayeredTexture
from fbx import KFbxTexture
from DisplayMaterial import DisplayMaterial
from DisplayTexture  import DisplayTexture
from DisplayLink     import DisplayLink
from DisplayShape    import DisplayShape


def DisplayMesh(pNode):
    lMesh = pNode.GetNodeAttribute ()

    # DisplayString("Mesh Name: ", pNode.GetName())
    # DisplayControlsPoints(lMesh)
    DisplayPolygons(lMesh)
    # DisplayMaterialMapping(lMesh)
    DisplayMaterial(lMesh)
    # DisplayTexture(lMesh)
    # DisplayMaterialConnections(lMesh)
    # DisplayLink(lMesh)
    # DisplayShape(lMesh)


def DisplayControlsPoints(pMesh):
    lControlPointsCount = pMesh.GetControlPointsCount()
    lControlPoints = pMesh.GetControlPoints()

    DisplayString("    Control Points")

    for i in range(lControlPointsCount):
        DisplayInt("        Control Point ", i)
        Display3DVector("            Coordinates: ", lControlPoints[i])

        for j in range(pMesh.GetLayerCount()):
            leNormals = pMesh.GetLayer(j).GetNormals()
            if leNormals:
                if leNormals.GetMappingMode() == KFbxLayerElement.eBY_CONTROL_POINT:
                    header = "            Normal Vector (on layer %d): " % j 
                    if leNormals.GetReferenceMode() == KFbxLayerElement.eDIRECT:
                        Display3DVector(header, leNormals.GetDirectArray().GetAt(i))

    DisplayString("")


def DisplayPolygons(pMesh):
    lPolygonCount = pMesh.GetPolygonCount()
    lControlPoints = pMesh.GetControlPoints() 

    DisplayString("    Polygons")

    vertexId = 0
    for i in range(lPolygonCount):
        DisplayInt("        Polygon ", i)

        for l in range(pMesh.GetLayerCount()):
            lePolgrp = pMesh.GetLayer(l).GetPolygonGroups()
            if lePolgrp:
                if lePolgrp.GetMappingMode() == KFbxLayerElement.eBY_POLYGON:
                    if lePolgrp.GetReferenceMode() == KFbxLayerElement.eINDEX:
                        header = "        Assigned to group (on layer %d): " % l 
                        polyGroupId = lePolgrp.GetIndexArray().GetAt(i)
                        DisplayInt(header, polyGroupId)
                else:
                    # any other mapping modes don't make sense
                    DisplayString("        \"unsupported group assignment\"")

        lPolygonSize = pMesh.GetPolygonSize(i)

        for j in range(lPolygonSize):
            lControlPointIndex = pMesh.GetPolygonVertex(i, j)

            Display3DVector("            Coordinates: ", lControlPoints[lControlPointIndex])

            for l in range(pMesh.GetLayerCount()):
                leVtxc = pMesh.GetLayer(l).GetVertexColors()
                if leVtxc:
                    header = "            Color vertex (on layer %d): " % l 

                    if leVtxc.GetMappingMode() == KFbxLayerElement.eBY_CONTROL_POINT:
                        if leVtxc.GetReferenceMode() == KFbxLayerElement.eDIRECT:
                            DisplayColor(header, leVtxc.GetDirectArray().GetAt(lControlPointIndex))
                        elif leVtxc.GetReferenceMode() == KFbxLayerElement.eINDEX_TO_DIRECT:
                                id = leVtxc.GetIndexArray().GetAt(lControlPointIndex)
                                DisplayColor(header, leVtxc.GetDirectArray().GetAt(id))
                    elif leVtxc.GetMappingMode() == KFbxLayerElement.eBY_POLYGON_VERTEX:
                            if leVtxc.GetReferenceMode() == KFbxLayerElement.eDIRECT:
                                DisplayColor(header, leVtxc.GetDirectArray().GetAt(vertexId))
                            elif leVtxc.GetReferenceMode() == KFbxLayerElement.eINDEX_TO_DIRECT:
                                id = leVtxc.GetIndexArray().GetAt(vertexId)
                                DisplayColor(header, leVtxc.GetDirectArray().GetAt(id))
                    elif leVtxc.GetMappingMode() == KFbxLayerElement.eBY_POLYGON or \
                         leVtxc.GetMappingMode() ==  KFbxLayerElement.eALL_SAME or \
                         leVtxc.GetMappingMode() ==  KFbxLayerElement.eNONE:       
                         # doesn't make much sense for UVs
                        pass

                leUV = pMesh.GetLayer(l).GetUVs()
                if leUV:
                    header = "            Texture UV (on layer %d): " % l 

                    if leUV.GetMappingMode() == KFbxLayerElement.eBY_CONTROL_POINT:
                        if leUV.GetReferenceMode() == KFbxLayerElement.eDIRECT:
                            Display2DVector(header, leUV.GetDirectArray().GetAt(lControlPointIndex))
                        elif leUV.GetReferenceMode() == KFbxLayerElement.eINDEX_TO_DIRECT:
                            id = leUV.GetIndexArray().GetAt(lControlPointIndex)
                            Display2DVector(header, leUV.GetDirectArray().GetAt(id))
                    elif leUV.GetMappingMode() ==  KFbxLayerElement.eBY_POLYGON_VERTEX:
                        lTextureUVIndex = pMesh.GetTextureUVIndex(i, j)
                        if leUV.GetReferenceMode() == KFbxLayerElement.eDIRECT or \
                           leUV.GetReferenceMode() == KFbxLayerElement.eINDEX_TO_DIRECT:
                            Display2DVector(header, leUV.GetDirectArray().GetAt(lTextureUVIndex))
                    elif leUV.GetMappingMode() == KFbxLayerElement.eBY_POLYGON or \
                         leUV.GetMappingMode() == KFbxLayerElement.eALL_SAME or \
                         leUV.GetMappingMode() ==  KFbxLayerElement.eNONE:
                         # doesn't make much sense for UVs
                        pass
            # # end for layer
            vertexId += 1
        # # end for polygonSize
    # # end for polygonCount


    # check visibility for the edges of the mesh
    for l in range(pMesh.GetLayerCount()):
        leVisibility=pMesh.GetLayer(0).GetVisibility()
        if leVisibility:
            header = "    Edge Visibilty (on layer %d): " % l
            DisplayString(header)
            # should be eBY_EDGE
            if leVisibility.GetMappingMode() == KFbxLayerElement.eBY_EDGE:
                # should be eDIRECT
                for j in range(pMesh.GetMeshEdgeCount()):
                    DisplayInt("        Edge ", j)
                    DisplayBool("              Edge visibilty: ", leVisibility.GetDirectArray().GetAt(j))

    DisplayString("")


def DisplayTextureNames(pProperty):
    lTextureName = ""
    
    lLayeredTextureCount = pProperty.GetSrcObjectCount(KFbxLayeredTexture.ClassId)
    if lLayeredTextureCount > 0:
        for j in range(lLayeredTextureCount):
            lLayeredTexture = pProperty.GetSrcObject(KFbxLayeredTexture.ClassId, j)
            lNbTextures = lLayeredTexture.GetSrcObjectCount(KFbxTexture.ClassId)
            lTextureName = " Texture "

            for k in range(lNbTextures):
                lTextureName += "\""
                lTextureName += lLayeredTexture.GetName()
                lTextureName += "\""
                lTextureName += " "
            lTextureName += "of "
            lTextureName += pProperty.GetName().Buffer()
            lTextureName += " on layer "
            lTextureName += j
        lTextureName += " |"
    else:
        #no layered texture simply get on the property
        lNbTextures = pProperty.GetSrcObjectCount(KFbxTexture.ClassId)

        if lNbTextures > 0:
            lTextureName = " Texture "
            lTextureName += " "

            for j in range(lNbTextures):
                lTexture = pProperty.GetSrcObject(KFbxTexture.ClassId,j)
                if lTexture:
                    lTextureName += "\""
                    lTextureName += lTexture.GetName()
                    lTextureName += "\""
                    lTextureName += " "
            lTextureName += "of "
            lTextureName += pProperty.GetName().Buffer()
            lTextureName += " |"
            
    return lTextureName

def DisplayMaterialTextureConnections(pMaterial, pMatId, l ):
    lConnectionString = "            Material " + str(pMatId) + " (on layer " + str(l) +") -- "
    #Show all the textures

    #Diffuse Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sDiffuse)
    lConnectionString += DisplayTextureNames(lProperty)

    #DiffuseFactor Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sDiffuseFactor)
    lConnectionString += DisplayTextureNames(lProperty)

    #Emissive Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sEmissive)
    lConnectionString += DisplayTextureNames(lProperty)

    #EmissiveFactor Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sEmissiveFactor)
    lConnectionString += DisplayTextureNames(lProperty)


    #Ambient Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sAmbient)
    lConnectionString += DisplayTextureNames(lProperty)

    #AmbientFactor Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sAmbientFactor)
    lConnectionString += DisplayTextureNames(lProperty)     

    #Specular Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sSpecular)
    lConnectionString += DisplayTextureNames(lProperty)

    #SpecularFactor Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sSpecularFactor)
    lConnectionString += DisplayTextureNames(lProperty)

    #Shininess Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sShininess)
    lConnectionString += DisplayTextureNames(lProperty)

    #Bump Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sBump)
    lConnectionString += DisplayTextureNames(lProperty)

    #Normal Map Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sNormalMap)
    lConnectionString += DisplayTextureNames(lProperty)

    #Transparent Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sTransparentColor)
    lConnectionString += DisplayTextureNames(lProperty)

    #TransparencyFactor Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sTransparencyFactor)
    lConnectionString += DisplayTextureNames(lProperty)

    #Reflection Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sReflection)
    lConnectionString += DisplayTextureNames(lProperty)

    #ReflectionFactor Textures
    lProperty = pMaterial.FindProperty(KFbxSurfaceMaterial.sReflectionFactor)
    lConnectionString += DisplayTextureNames(lProperty)

    #if(lMaterial != NULL)
    DisplayString(lConnectionString)

def DisplayMaterialConnections(pMesh):
    lPolygonCount = pMesh.GetPolygonCount()

    DisplayString("    Polygons Material Connections")

    #check whether the material maps with only one mesh
    lIsAllSame = True
    for l in range(pMesh.GetLayerCount()):
        lLayerMaterial = pMesh.GetLayer(l).GetMaterials()
        if lLayerMaterial:
            if lLayerMaterial.GetMappingMode() == KFbxLayerElement.eBY_POLYGON:
                lIsAllSame = False
                break

    #For eALL_SAME mapping type, just out the material and texture mapping info once
    if lIsAllSame:
        for l in range(pMesh.GetLayerCount()):
            lLayerMaterial = pMesh.GetLayer(l).GetMaterials()
            if lLayerMaterial:
                if lLayerMaterial.GetMappingMode() == KFbxLayerElement.eALL_SAME:
                    lMaterial = pMesh.GetNode().GetMaterial(lLayerMaterial.GetIndexArray().GetAt(0))    
                    lMatId = lLayerMaterial.GetIndexArray().GetAt(0)
                    if lMatId >=0:
                        DisplayInt("        All polygons share the same material on layer ", l)
                        DisplayMaterialTextureConnections(lMaterial, lMatId, l)
            else:
                #layer 0 has no material
                if l == 0:
                    DisplayString("        no material applied")

    #For eBY_POLYGON mapping type, just out the material and texture mapping info once
    else:
        for i in range(lPolygonCount):
            DisplayInt("        Polygon ", i)

            for l in range(pMesh.GetLayerCount()):
                lLayerMaterial = pMesh.GetLayer(l).GetMaterials()
                if lLayerMaterial:
                    lMatId = -1
                    lMaterial = pMesh.GetNode().GetMaterial(lLayerMaterial.GetIndexArray().GetAt(i))
                    lMatId = lLayerMaterial.GetIndexArray().GetAt(i)

                    if lMatId >= 0:
                        DisplayMaterialTextureConnections(lMaterial, lMatId, l)


def DisplayMaterialMapping(pMesh):
    lMappingTypes = [ "None", "By Control Point", "By Polygon Vertex", "By Polygon", "By Edge", "All Same" ]
    lReferenceMode = [ "Direct", "Index", "Index to Direct"]

    lMtrlCount = 0
    lNode = None
    if pMesh:
        lNode = pMesh.GetNode()
        if lNode:
            lMtrlCount = lNode.GetMaterialCount()

    for l in range(pMesh.GetLayerCount()):
        leMat = pMesh.GetLayer(l).GetMaterials()
        if leMat:
            header = "    Material layer %d: " % l
            DisplayString(header)

            DisplayString("           Mapping: ", lMappingTypes[leMat.GetMappingMode()])
            DisplayString("           ReferenceMode: ", lReferenceMode[leMat.GetReferenceMode()])

            lMaterialCount = 0

            if leMat.GetReferenceMode() == KFbxLayerElement.eDIRECT or \
                leMat.GetReferenceMode() == KFbxLayerElement.eINDEX_TO_DIRECT:
                lMaterialCount = lMtrlCount

            if leMat.GetReferenceMode() == KFbxLayerElement.eINDEX or \
                leMat.GetReferenceMode() == KFbxLayerElement.eINDEX_TO_DIRECT:
                lString = "           Indices: "

                lIndexArrayCount = leMat.GetIndexArray().GetCount() 
                for i in range(lIndexArrayCount):
                    lString += str(leMat.GetIndexArray().GetAt(i))

                    if i < lIndexArrayCount - 1:
                        lString += ", "

                DisplayString(lString)

    DisplayString("")
