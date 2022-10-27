import xml.etree.ElementTree as ET
import posixpath


def settingVisual(path, mode):
    text = '''<root>
	<exportAnimation>	false	</exportAnimation>
	<exportMode>	''' + mode + '''	</exportMode>
	<boneCount>	24	</boneCount>
	<transformToOrigin>	false	</transformToOrigin>
	<allowScale>	false	</allowScale>
	<bumpMapped>	true	</bumpMapped>
	<keepExistingMaterials>	true	</keepExistingMaterials>
	<snapVertices>	false	</snapVertices>
	<stripRefPrefix>	false	</stripRefPrefix>
	<useReferenceNode>	false	</useReferenceNode>
	<referenceNodesFile />
	<disableVisualChecker>	false	</disableVisualChecker>
	<useLegacyScaling>	false	</useLegacyScaling>
	<fixCylindrical>	false	</fixCylindrical>
	<useLegacyOrientation>	false	</useLegacyOrientation>
	<sceneRootAdded>	false	</sceneRootAdded>
	<includeMeshes>	true	</includeMeshes>
	<includeEnvelopesAndBones>	false	</includeEnvelopesAndBones>
	<includeNodes>	true	</includeNodes>
	<includeMaterials>	true	</includeMaterials>
	<includeAnimations>	false	</includeAnimations>
	<useCharacterMode>	false	</useCharacterMode>
	<animationName>	anim	</animationName>
	<includePortals>	false	</includePortals>
	<worldSpaceOrigin>	false	</worldSpaceOrigin>
	<unitScale>	0.100000	</unitScale>
	<localHierarchy>	false	</localHierarchy>
	<nodeFilter>	1	</nodeFilter>
	<copyTexturesTo />
	</root>'''

    f = open(path, 'w')
    f.write(text)
    f.close()


def material_node(type_mesh, name_mesh, relativePath):
    # path_nameFile = finExp_fileName()
    # tank_path = finExp_PathCompile()
    shader = 'PBS_tank'
    id_mesh = 'lambert1'

    if name_mesh == 'hull':
        id_mesh = 'tank_hull_01'
    if name_mesh == 'Turret_01':
        id_mesh = 'tank_turret_01'
    if name_mesh == 'Turret_02':
        id_mesh = 'tank_turret_02'
    if name_mesh == 'guns':
        id_mesh = 'tank_guns'

    if type_mesh == 'skinned':
        shader = 'PBS_tank_skinned'
    if type_mesh == 'crash':
        shader = 'PBS_tank_crash'
    if type_mesh == 'collider':
        shader = 'lightonly.fx'

    if type_mesh == 'skinned':
        id_mesh = id_mesh + '_skinned'
    if type_mesh == 'collider':
        id_mesh = 'armor_1'

    if type_mesh == 'collider_track_L':
        id_mesh = 'leftTrack'
    if type_mesh == 'collider_track_R':
        id_mesh = 'rightTrack'

    if type_mesh == 'normal_track_L':
        id_mesh = 'track_mat_L_skinned'
        shader = 'PBS_tank_skinned'

    if type_mesh == 'normal_track_R':
        id_mesh = 'track_mat_R_skinned'
        shader = 'PBS_tank_skinned'

    if type_mesh == 'normal_chassis':
        id_mesh = 'tank_chassis_01_skinned'
        shader = 'PBS_tank_skinned'

    # anm = relative_path + '_temp.dds'
    # am = relative_path + '_temp.dds'
    # ao = relative_path + '_temp.dds'
    #
    # gmm_c = tank_path + '/' + path_nameFile + '_temp.dds'
    # anm_c = tank_path + '/' + path_nameFile + '_temp.dds'
    # am_c = tank_path + '/' + path_nameFile + '_temp.dds'
    # ao_c = tank_path + '/' + path_nameFile + '_temp.dds'

    # relative_path = tank_path + '/' + path_nameFile
    if relativePath:
        gmm = anm = am = ao = gmm_c = anm_c = am_c = ao_c = relativePath + '_temp.dds'
        split_relpath = relativePath.split('vehicles')
        relative_path = 'vehicles' + split_relpath[1]

    # print 'NAME MESH:', name_mesh
    if name_mesh:
        if name_mesh == 'chassis':
            gmm = relative_path + '_chassis_01_GMM.dds'
            anm = relative_path + '_chassis_01_ANM.dds'
            am = relative_path + '_chassis_01_AM.dds'
            ao = relative_path + '_chassis_01_AO.dds'

        if 'Turret_01' in name_mesh:
            gmm = relative_path + '_turret_01_GMM.dds'
            anm = relative_path + '_turret_01_ANM.dds'
            am = relative_path + '_turret_01_AM.dds'
            ao = relative_path + '_turret_01_AO.dds'

        if 'Turret_02' in name_mesh:
            gmm = relative_path + '_turret_02_GMM.dds'
            anm = relative_path + '_turret_02_ANM.dds'
            am = relative_path + '_turret_02_AM.dds'
            ao = relative_path + '_turret_02_AO.dds'

        if name_mesh == 'guns':
            gmm = relative_path + '_guns_GMM.dds'
            anm = relative_path + '_guns_ANM.dds'
            am = relative_path + '_guns_AM.dds'
            ao = relative_path + '_guns_AO.dds'

        if name_mesh == 'hull':
            gmm = relative_path + '_hull_01_GMM.dds'
            anm = relative_path + '_hull_01_ANM.dds'
            am = relative_path + '_hull_01_AM.dds'
            ao = relative_path + '_hull_01_AO.dds'

        if name_mesh == 'hull_crash':
            gmm = relative_path + '_hull_01_GMM.dds'
            anm = relative_path + '_hull_01_ANM.dds'
            am = relative_path + '_hull_01_AM.dds'
            ao = relative_path + '_hull_01_AO.dds'

            gmm_c = relative_path + '_chassis_01_GMM.dds'
            anm_c = relative_path + '_chassis_01_ANM.dds'
            am_c = relative_path + '_chassis_01_AM.dds'
            ao_c = relative_path + '_chassis_01_AO.dds'

    node = '''<material>
					<identifier>	''' + id_mesh + '''	</identifier>
					<fx>	shaders/std_effects/''' + shader + '''.fx	</fx>
					<collisionFlags>	0	</collisionFlags>
					<materialKind>	0	</materialKind>
					<property>	g_detailUVTiling
						<Vector4>	3.50685 3.50685 0.000000 0.000000	</Vector4>
					</property>
					<property>	g_detailPowerGloss
						<Float>	0.35	</Float>
					</property>
					<property>	g_detailPowerAlbedo
						<Float>	0.11	</Float>
					</property>
					<property>	g_maskBias
						<Float>	0.18	</Float>
					</property>
					<property>	g_detailPower
						<Float>	5	</Float>
					</property>
					<property>	metallicDetailMap
						<Texture>	vehicles/russian/Tank_detail/Details_map.dds	</Texture>
					</property>
					<property>	g_useDetailMetallic
						<Bool>	true	</Bool>
					</property>
					<property>	g_useNormalPackDXT1
						<Bool>	false	</Bool>
					</property>
					<property>	metallicGlossMap
						<Texture>	''' + gmm + '''	</Texture>
					</property>
					<property>	normalMap
						<Texture>	''' + anm + '''	</Texture>
					</property>
					<property>	diffuseMap
						<Texture>	''' + am + '''	</Texture>
					</property>
					<property>	excludeMaskAndAOMap
						<Texture>	''' + ao + '''	</Texture>
					</property>
				</material>'''

    hull_crash_node = '''<material>
					<identifier>	tank_hull_01	</identifier>
					<fx>	shaders/std_effects/PBS_tank_crash.fx	</fx>
					<collisionFlags>	0	</collisionFlags>
					<materialKind>	0	</materialKind>
					<property>	g_crashUVTiling
						<Vector4>	4 4 0.000000 0.000000	</Vector4>
					</property>
					<property>	crashTileMap
						<Texture>	vehicles/russian/Tank_detail/crash_tile.dds	</Texture>
					</property>
					<property>	g_useNormalPackDXT1
						<Bool>	false	</Bool>
					</property>
					<property>	excludeMaskAndAOMap
						<Texture>	''' + ao + '''	</Texture>
					</property>
					<property>	metallicGlossMap
						<Texture>	''' + gmm + '''	</Texture>
					</property>
					<property>	normalMap
						<Texture>	''' + anm + '''	</Texture>
					</property>
					<property>	diffuseMap
						<Texture>	''' + am + '''	</Texture>
					</property>
					<property>	alphaTestEnable
						<Bool>	false	</Bool>
					</property>
				</material>'''

    chassis_crash_node = '''<material>
					<identifier>	tank_chassis_01	</identifier>
					<fx>	shaders/std_effects/PBS_tank_crash.fx	</fx>
					<collisionFlags>	0	</collisionFlags>
					<materialKind>	0	</materialKind>
					<property>	g_crashUVTiling
						<Vector4>	2 1 0.000000 0.000000	</Vector4>
					</property>
					<property>	crashTileMap
						<Texture>	vehicles/russian/Tank_detail/crash_tile.dds	</Texture>
					</property>
					<property>	g_useNormalPackDXT1
						<Bool>	false	</Bool>
					</property>
					<property>	metallicGlossMap
						<Texture>	''' + gmm_c + '''	</Texture>
					</property>
					<property>	normalMap
						<Texture>	''' + anm_c + '''	</Texture>
					</property>
					<property>	diffuseMap
						<Texture>	''' + am_c + '''	</Texture>
					</property>
					<property>	excludeMaskAndAOMap
						<Texture>	''' + ao_c + '''	</Texture>
					</property>
					<property>	alphaTestEnable
						<Bool>	false	</Bool>
					</property>
				</material>'''

    col_node = '''<material>
					<identifier>	armor_1	</identifier>
					<fx>	shaders/std_effects/lightonly.fx	</fx>
					<collisionFlags>	0	</collisionFlags>
					<materialKind>	1	</materialKind>
					<property>	diffuseMap
						<Texture>	objects/misc/collisions_mat/armor_1.dds	</Texture>
					</property>
					<property>
						<Bool>true</Bool>doubleSided
					</property>
				</material>'''

    wheel_node = '''<material>
					<identifier>	wheel	</identifier>
					<fx>	shaders/std_effects/lightonly.fx	</fx>
					<collisionFlags>	0	</collisionFlags>
					<materialKind>	254	</materialKind>
					<property>	diffuseMap
						<Texture>	objects/misc/collisions_mat/wheel.dds	</Texture>
					</property>
					<property>
						<Bool>true</Bool>doubleSided
					</property>
				</material>'''

    track_node_L = '''<material>
					<identifier>	leftTrack	</identifier>
					<fx>	shaders/std_effects/lightonly.fx	</fx>
					<collisionFlags>	0	</collisionFlags>
					<materialKind>	23	</materialKind>
					<property>	diffuseMap
						<Texture>	objects/misc/collisions_mat/leftTrack.dds	</Texture>
					</property>
				</material>'''
    track_node_R = '''<material>
					<identifier>	rightTrack	</identifier>
					<fx>	shaders/std_effects/lightonly.fx	</fx>
					<collisionFlags>	0	</collisionFlags>
					<materialKind>	24	</materialKind>
					<property>	diffuseMap
						<Texture>	objects/misc/collisions_mat/rightTrack.dds	</Texture>
					</property>
				</material>'''

    fake_turret_node = '''<material>
					<identifier>	tank_turret_01 	</identifier>
					<collisionFlags>	0	</collisionFlags>
					<materialKind>	0	</materialKind>
				</material>'''

    if type_mesh == 'collider':
        return [col_node]
    if type_mesh == 'wheel':
        return [wheel_node]
    elif type_mesh == 'collider_track':
        return [track_node_R, track_node_L]
    elif name_mesh == 'hull_crash':
        return [hull_crash_node], [chassis_crash_node]
    elif type_mesh == 'fake_turret':
        return [fake_turret_node]
    else:
        return [node]


def material_node_main(material, textures, shader):
    node = '''<material>
					<identifier>	''' + material + '''	</identifier>
					<fx>	shaders/std_effects/''' + shader + '''.fx	</fx>
					<collisionFlags>	0	</collisionFlags>
					<materialKind>	0	</materialKind>
					<property>	g_detailUVTiling
						<Vector4>	3.50685 3.50685 0.000000 0.000000	</Vector4>
					</property>
					<property>	g_detailPowerGloss
						<Float>	0.35	</Float>
					</property>
					<property>	g_detailPowerAlbedo
						<Float>	0.11	</Float>
					</property>
					<property>	g_maskBias
						<Float>	0.18	</Float>
					</property>
					<property>	g_detailPower
						<Float>	5	</Float>
					</property>
					<property>	metallicDetailMap
						<Texture>	vehicles/russian/Tank_detail/Details_map.dds	</Texture>
					</property>
					<property>	g_useDetailMetallic
						<Bool>	true	</Bool>
					</property>
					<property>	g_useNormalPackDXT1
						<Bool>	false	</Bool>
					</property>
					<property>	metallicGlossMap
						<Texture>	''' + textures[0] + '''.dds	</Texture>
					</property>
					<property>	normalMap
						<Texture>	''' + textures[1] + '''.dds	</Texture>
					</property>
					<property>	diffuseMap
						<Texture>	''' + textures[2] + '''.dds	</Texture>
					</property>
					<property>	excludeMaskAndAOMap
						<Texture>	''' + textures[3] + '''.dds	</Texture>
					</property>
				</material>'''

    return node


def material_node_crash(material, textures, shader):
    # print 'EEEEE', textures[3]
    node = '''<material>
					<identifier>	''' + material + '''	</identifier>
					<fx>	shaders/std_effects/''' + shader + '''.fx	</fx>
					<collisionFlags>	0	</collisionFlags>
					<materialKind>	0	</materialKind>
					<property>	g_crashUVTiling
						<Vector4>	4 4 0.000000 0.000000	</Vector4>
					</property>
					<property>	crashTileMap
						<Texture>	vehicles/russian/Tank_detail/crash_tile.dds	</Texture>
					</property>
					<property>	g_useNormalPackDXT1
						<Bool>	false	</Bool>
					</property>
					<property>	metallicGlossMap
						<Texture>	''' + textures[0] + '''.dds	</Texture>
					</property>
					<property>	normalMap
						<Texture>	''' + textures[1] + '''.dds	</Texture>
					</property>
					<property>	diffuseMap
						<Texture>	''' + textures[2] + '''.dds	</Texture>
					</property>
					<property>	excludeMaskAndAOMap
						<Texture>	''' + textures[3] + '''.dds	</Texture>
					</property>
					<property>	alphaTestEnable
						<Bool>	false	</Bool>
					</property>
				</material>'''
    return node


def collision_node_main(material, matkind):
    node = '''<material>
					<identifier> ''' + material + '''	</identifier>
					<fx>	shaders/std_effects/lightonly.fx	</fx>
					<collisionFlags>	0	</collisionFlags>
					<materialKind>	''' + matkind + '''	</materialKind>
					<property>	diffuseMap
						<Texture>	objects/misc/collisions_mat/''' + material + '''.dds	</Texture>
					</property>
					<property>
						<Bool>true</Bool>doubleSided
					</property>
				</material>'''
    return node


def fake_turret_node():
    node = '''<material>
					<identifier>	tank_turret_01 	</identifier>
					<collisionFlags>	0	</collisionFlags>
					<materialKind>	0	</materialKind>
				</material>'''
    return node


def xml_edit(visual_path, text_node):
    tree = ET.parse(visual_path)
    root = tree.getroot()
    xmlEl = None
    new_node = None
    new_node_left = None

    new_node = ET.fromstring(text_node)

    # print new_node
    for child in root.iter('primitiveGroup'):
        for c in child.iter():
            if c.tag == 'primitiveGroup':
                xmlEl = c

        for c in child.iter():
            if c.tag == 'material' and xmlEl:
                xmlEl.remove(c)
                xmlEl.append(new_node)
                if new_node_left:
                    new_node = new_node_left
    tree.write(visual_path)


def xml_crash_hull_edit(visual_path, node, material):
    tree = ET.parse(visual_path)
    root = tree.getroot()
    xmlEl = None
    xml_mat = None
    new_node = None
    for child in root.iter('primitiveGroup'):
        for c in child.iter():
            if c.tag == 'primitiveGroup':
                xmlEl = c
            print
            c.text
            if c.tag == 'material':
                xml_mat = c
            if material in c.text:
                xmlEl.remove(xml_mat)
                new_node = ET.fromstring(node)
                xmlEl.append(new_node)
    tree.write(visual_path)


def xml_custom_edit(visual_path, node, material):
    new_node = ET.fromstring(node)
    tree = ET.parse(visual_path)
    root = tree.getroot()
    for child in root.iter('primitiveGroup'):
        if child.tag == 'primitiveGroup':
            for c in child.iter():
                if c.tag == 'material':
                    for z in c.iter():
                        if material in z.text:
                            child.remove(c)
                            child.append(new_node)
    tree.write(visual_path)


def xml_chassis_edit(visual_path, crash=False, textures=None):
    tree = ET.parse(visual_path)
    root = tree.getroot()
    xmlEl = None
    xml_mat = None
    new_node = None
    new_node_left = None
    new_node_right = None
    col_node = None
    for child in root.iter('primitiveGroup'):
        for c in child.iter():
            if c.tag == 'primitiveGroup':
                xmlEl = c

        for c in child.iter():
            if 'track_mat_R_skinned' in c.text or 'track_mat_L_skinned' in c.text or 'tank_chassis_01_skinned' in c.text:
                # xml_mat = normal_chassis_node(c.text, 'track')
                # new_node = ET.fromstring(xml_mat)
                pass

            if 'tank_chassis_01_skinned' in c.text:
                if crash:
                    print
                    'HERE'
                    xml_mat = material_node_main(c.text, 'PBS_tank_skinned_crash', textures)
                    new_node = ET.fromstring(xml_mat)
                else:
                    # xml_mat = normal_chassis_node(c.text, 'chassis')
                    # new_node = ET.fromstring(xml_mat)
                    pass

            if 'leftTrack' in c.text and 'leftTrack.dds' not in c.text:
                xml_mat = collision_node_main('leftTrack', '23')
                new_node_left = ET.fromstring(xml_mat)

            if 'rightTrack' in c.text and 'rightTrack.dds' not in c.text:
                xml_mat = collision_node_main('rightTrack', '24')
                new_node_right = ET.fromstring(xml_mat)

        for c in child.iter():
            # print '#####///////////##########', c.tag, c.text
            if c.tag == 'material' and xmlEl and new_node:
                print
                '#####///////////##########', xmlEl, c.text
                xmlEl.remove(c)
                xmlEl.append(new_node)

            if c.tag == 'material' and xmlEl and new_node_left and 'leftTrack' in c.text:
                xmlEl.remove(c)
                xmlEl.append(new_node_left)

            if c.tag == 'material' and xmlEl and new_node_right and 'rightTrack' in c.text:
                xmlEl.remove(c)
                xmlEl.append(new_node_right)

    tree.write(visual_path)
