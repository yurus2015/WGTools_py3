import maya.cmds as cmds
checkLabel = "Find Friction Value"


def main():
	print('<< ' + checkLabel.upper() + ' >>')
	return_list = []

	nodes = cmds.ls(type = 'hkNodeRigidBody')
	if nodes:
		for node in nodes:
			friction = cmds.getAttr(node + '.friction')
			if friction != 1.0:
				tmp = []
				tmp.append(node + ': ' + str(friction))
				tmp.append(node)
				return_list.append(tmp)

	return return_list