import maya.cmds as cmds
from validator2019.utils.validator_API import *
checkId = 28
checkLabel = "3.1 Check names of track`s materials"


def all_tracks():
	pattern_track = re.compile('track_[LR]\d*$')
	tracks_in_lod = []
	# for lod in lods:
	transforms = cmds.listRelatives('lod0', ad=1, type = 'transform', f=1)
	for transform in transforms:
		if pattern_track.findall(transform):
			tracks_in_lod.append(transform)

	# if len(tracks_in_lod) < 3:
	#     return None
	# else:
	return tracks_in_lod


def get_track_material(track):
	shapes = cmds.listRelatives(track, shapes=True, f=True)
	print('SHAPES:', shapes)
	engine = cmds.listConnections(shapes , type = 'shadingEngine')
	print('ENGINE:', engine)
	materials = cmds.ls(cmds.listConnections(engine), materials = True)
	materials = list(set(materials))
	return materials


def check_crash_scene():
	file_name = cmds.file(q=True, sn=True, shn=True)
	if 'crash' in file_name.lower():
		return True
	else:
		return False


def all_track_material():
	pattern_mat = re.compile('track_mat_[LR]\d*$')
	all_mats = cmds.ls(mat = True)
	track_mats = []
	for mat in all_mats:
		if pattern_mat.findall(mat):
			track_mats.append(mat)
	return track_mats


def main():
	tracks = all_tracks()
	print('ALL TRACKS:', tracks)
	print(check_crash_scene())
	scene_track_mats = all_track_material()
	print('MAT IN SCENE:', scene_track_mats)
	for track in tracks:
		materials = get_track_material(track)
		print('MATS:', materials)


def main_():
	print('<< ' + checkLabel.upper() + ' >>')

	validNamesList = vl_tanksMatValidNames()

	matData = listAllMat()
	returnList = []

	#dom didom dom dom - KOSTIL'
	rawFilePath = cmds.file (q=True, exn=True)
	if "G_Tiger" in rawFilePath or "G45_G_Tiger" in rawFilePath:
		return returnList


	for x in range(len(matData)):
		valid = 0
		for y in validNamesList:
			temp = y.search(matData[x])
			if temp != None:
				valid = 1
		if valid == 0:
			tmp = []
			tmp.append(matData[x])
			tmp.append(matData[x])
			returnList.append(tmp)




	for x in validNamesList:
		pattern =  x.pattern
		try:
			pattern = pattern.replace('\d','#')
		except:
			pass
		try:
			pattern = pattern.replace('\Z','')
		except:
			pass
		try:
			pattern = pattern.replace('^','')
		except:
			pass
		# helpStringList.append(pattern)

	track_mat = []
	for i in matData:
		if i.find("track_mat") != -1:
			track_mat.append(i)
	if  track_mat:
		if not len(track_mat) == 2:
			tmp = []
			tmp.append("The scene has more or less then 2 track_mat materials")
			tmp.append("")
			returnList.append(tmp)
		else:
			if (track_mat[0].find("_L") != -1 and track_mat[1].find("_L") != -1):
				tmp = []
				tmp.append("Both of track_mats have postfix '_L'")
				tmp.append("")
				returnList.append(tmp)

			elif (track_mat[0].find("_R") != -1 and track_mat[1].find("_R") != -1):
				tmp = []
				tmp.append("Both of track_mats have postfix '_R'")
				tmp.append("")
				returnList.append(tmp)

			else:
				pass
	else:
		tmp = []
		tmp.append("There are no track_mat materials in the scene")
		tmp.append("")
		returnList.append(tmp)

	return  returnList
